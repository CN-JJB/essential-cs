#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdatomic.h>
#include <pthread.h>
#include <stdbool.h>

/*
 * LAB-REQ-03 Checkpoint 3: POSIX Mutex Repair
 *
 * Repairs the compound read-modify-write state transition using pthread_mutex_t.
 * Verifies that the declared invariant (expected_serial == actual_value) holds across
 * all runs when critical sections are properly mutually exclusive.
 */

static atomic_int g_shared_counter = 0;
static pthread_mutex_t g_counter_mutex = PTHREAD_MUTEX_INITIALIZER;

typedef struct {
    int thread_id;
    int iterations;
} worker_arg_t;

static void* mutex_worker(void* arg) {
    worker_arg_t* w = (worker_arg_t*)arg;
    for (int i = 0; i < w->iterations; i++) {
        pthread_mutex_lock(&g_counter_mutex);

        /* Protected critical section: Read -> Compute -> Store */
        int observed = atomic_load_explicit(&g_shared_counter, memory_order_relaxed);
        atomic_store_explicit(&g_shared_counter, observed + 1, memory_order_relaxed);

        pthread_mutex_unlock(&g_counter_mutex);
    }
    return NULL;
}

int main(int argc, char** argv) {
    int iterations_per_thread = 10000;
    if (argc > 1 && argv[1][0] != '-') {
        iterations_per_thread = atoi(argv[1]);
        if (iterations_per_thread <= 0) iterations_per_thread = 10000;
    }

    atomic_store_explicit(&g_shared_counter, 0, memory_order_relaxed);

    pthread_t t1, t2;
    worker_arg_t w1 = {.thread_id = 1, .iterations = iterations_per_thread};
    worker_arg_t w2 = {.thread_id = 2, .iterations = iterations_per_thread};

    pthread_create(&t1, NULL, mutex_worker, &w1);
    pthread_create(&t2, NULL, mutex_worker, &w2);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    int final_val = atomic_load_explicit(&g_shared_counter, memory_order_relaxed);
    int expected = iterations_per_thread * 2;
    bool invariant_preserved = (final_val == expected);

    printf("{\"event\": \"MUTEX_REPAIR_RESULT\", \"iterations_per_thread\": %d, \"expected\": %d, \"actual\": %d, \"lost_updates\": %d, \"invariant_preserved\": %s}\n",
           iterations_per_thread, expected, final_val, expected - final_val, invariant_preserved ? "true" : "false");
    fflush(stdout);

    pthread_mutex_destroy(&g_counter_mutex);
    return invariant_preserved ? 0 : 1;
}
