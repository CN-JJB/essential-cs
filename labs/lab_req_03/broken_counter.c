#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdatomic.h>
#include <pthread.h>
#include <sched.h>
#include <stdbool.h>

/*
 * LAB-REQ-03 Checkpoint 1 & 2: UB-Free Compound Update Demonstration
 *
 * Demonstrates that atomic loads and stores prevent C data-race Undefined Behavior (UB),
 * but individual atomicity does NOT make multi-step state transitions atomic.
 *
 * Mode 1 (Default): Deterministic phase/barrier coordination producing real lost updates.
 * Mode 2 (--natural): Supplemental natural scheduler observation with sched_yield().
 */

typedef struct {
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    int count;
    int trip_count;
    int phase;
} simple_barrier_t;

static void barrier_init(simple_barrier_t *b, int trip_count) {
    pthread_mutex_init(&b->mutex, NULL);
    pthread_cond_init(&b->cond, NULL);
    b->count = 0;
    b->trip_count = trip_count;
    b->phase = 0;
}

static void barrier_destroy(simple_barrier_t *b) {
    pthread_mutex_destroy(&b->mutex);
    pthread_cond_destroy(&b->cond);
}

static void barrier_wait(simple_barrier_t *b) {
    pthread_mutex_lock(&b->mutex);
    int p = b->phase;
    b->count++;
    if (b->count == b->trip_count) {
        b->count = 0;
        b->phase = !b->phase;
        pthread_cond_broadcast(&b->cond);
    } else {
        while (b->phase == p) {
            pthread_cond_wait(&b->cond, &b->mutex);
        }
    }
    pthread_mutex_unlock(&b->mutex);
}

/* Shared atomic counter - all concurrent accesses are legal C11 atomic operations */
static atomic_int g_shared_counter = 0;

/* Barriers for deterministic interleaving */
static simple_barrier_t g_barrier_read;
static simple_barrier_t g_barrier_store;
static simple_barrier_t g_barrier_round_end;

#define DETERMINISTIC_ROUNDS 5

typedef struct {
    int thread_id;
    int rounds;
} worker_arg_t;

static void* deterministic_worker(void* arg) {
    worker_arg_t* w = (worker_arg_t*)arg;
    for (int r = 0; r < w->rounds; r++) {
        /* Phase 1: Synchronize before reading so both observe identical state */
        barrier_wait(&g_barrier_read);

        /* Legal atomic load with relaxed memory order */
        int observed = atomic_load_explicit(&g_shared_counter, memory_order_relaxed);
        int computed = observed + 1;

        printf("{\"event\": \"PHASE_READ\", \"round\": %d, \"thread\": %d, \"observed\": %d, \"computed\": %d}\n",
               r, w->thread_id, observed, computed);
        fflush(stdout);

        /* Phase 2: Synchronize before storing to guarantee neither stores before both have read */
        barrier_wait(&g_barrier_store);

        /* Legal atomic store with relaxed memory order */
        atomic_store_explicit(&g_shared_counter, computed, memory_order_relaxed);

        /* Phase 3: Synchronize at round end */
        barrier_wait(&g_barrier_round_end);
    }
    return NULL;
}

static void* natural_worker(void* arg) {
    worker_arg_t* w = (worker_arg_t*)arg;
    for (int i = 0; i < w->rounds; i++) {
        int observed = atomic_load_explicit(&g_shared_counter, memory_order_relaxed);
        sched_yield();
        atomic_store_explicit(&g_shared_counter, observed + 1, memory_order_relaxed);
    }
    return NULL;
}

int main(int argc, char** argv) {
    bool natural_mode = false;
    int natural_iterations = 10000;

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--natural") == 0) {
            natural_mode = true;
            if (i + 1 < argc && argv[i + 1][0] != '-') {
                natural_iterations = atoi(argv[++i]);
                if (natural_iterations <= 0) natural_iterations = 10000;
            }
        }
    }

    if (!natural_mode) {
        /* Deterministic Coordinated Lost-Update Interleaving */
        atomic_store_explicit(&g_shared_counter, 0, memory_order_relaxed);
        barrier_init(&g_barrier_read, 2);
        barrier_init(&g_barrier_store, 2);
        barrier_init(&g_barrier_round_end, 2);

        pthread_t t1, t2;
        worker_arg_t w1 = {.thread_id = 1, .rounds = DETERMINISTIC_ROUNDS};
        worker_arg_t w2 = {.thread_id = 2, .rounds = DETERMINISTIC_ROUNDS};

        pthread_create(&t1, NULL, deterministic_worker, &w1);
        pthread_create(&t2, NULL, deterministic_worker, &w2);

        pthread_join(t1, NULL);
        pthread_join(t2, NULL);

        int final_val = atomic_load_explicit(&g_shared_counter, memory_order_relaxed);
        int expected_serial = DETERMINISTIC_ROUNDS * 2;
        int lost = expected_serial - final_val;

        printf("{\"event\": \"DETERMINISTIC_RESULT\", \"rounds\": %d, \"expected_serial\": %d, \"actual_value\": %d, \"lost_updates\": %d, \"ub_present\": false}\n",
               DETERMINISTIC_ROUNDS, expected_serial, final_val, lost);
        fflush(stdout);

        barrier_destroy(&g_barrier_read);
        barrier_destroy(&g_barrier_store);
        barrier_destroy(&g_barrier_round_end);
    } else {
        /* Supplemental Natural Scheduler Observation */
        atomic_store_explicit(&g_shared_counter, 0, memory_order_relaxed);
        pthread_t t1, t2;
        worker_arg_t w1 = {.thread_id = 1, .rounds = natural_iterations};
        worker_arg_t w2 = {.thread_id = 2, .rounds = natural_iterations};

        pthread_create(&t1, NULL, natural_worker, &w1);
        pthread_create(&t2, NULL, natural_worker, &w2);

        pthread_join(t1, NULL);
        pthread_join(t2, NULL);

        int final_val = atomic_load_explicit(&g_shared_counter, memory_order_relaxed);
        int expected_serial = natural_iterations * 2;
        int lost = expected_serial - final_val;
        bool manifested = (lost > 0);

        printf("{\"event\": \"NATURAL_RESULT\", \"iterations_per_thread\": %d, \"expected_serial\": %d, \"actual_value\": %d, \"lost_updates\": %d, \"manifested\": %s}\n",
               natural_iterations, expected_serial, final_val, lost, manifested ? "true" : "false");
        fflush(stdout);
    }

    return 0;
}
