#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <stdbool.h>

/*
 * LAB-REQ-03 Checkpoint 5: Controlled Deadlock Preconditions Demonstration
 *
 * Runs inside an owned child process.
 * Demonstrates circular wait preconditions:
 * - Thread 1 acquires Lock A, then attempts to acquire Lock B.
 * - Thread 2 acquires Lock B, then attempts to acquire Lock A.
 *
 * Emits structured events to stdout:
 * 1. FIRST_LOCK_ACQUIRED for Lock A (Thread 1) and Lock B (Thread 2)
 * 2. Handshake barrier synchronizes both workers
 * 3. ATTEMPTING_SECOND_LOCK for Lock B (Thread 1) and Lock A (Thread 2)
 * 4. Process stalls indefinitely in circular wait
 *
 * The parent watchdog interprets the timeout ONLY after both preconditions are proven.
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

static pthread_mutex_t g_lock_a = PTHREAD_MUTEX_INITIALIZER;
static pthread_mutex_t g_lock_b = PTHREAD_MUTEX_INITIALIZER;
static simple_barrier_t g_start_barrier;

static void* worker_1(void* arg) {
    (void)arg;

    /* Acquire first lock: Lock A */
    pthread_mutex_lock(&g_lock_a);
    printf("{\"event\": \"FIRST_LOCK_ACQUIRED\", \"thread\": 1, \"lock\": \"A\"}\n");
    fflush(stdout);

    /* Synchronize with Worker 2 so both hold their first lock */
    barrier_wait(&g_start_barrier);

    /* Attempt second lock: Lock B (held by Worker 2) */
    printf("{\"event\": \"ATTEMPTING_SECOND_LOCK\", \"thread\": 1, \"lock\": \"B\"}\n");
    fflush(stdout);

    pthread_mutex_lock(&g_lock_b);

    /* Unreachable under deadlock */
    printf("{\"event\": \"UNEXPECTED_PROGRESS\", \"thread\": 1}\n");
    fflush(stdout);
    pthread_mutex_unlock(&g_lock_b);
    pthread_mutex_unlock(&g_lock_a);
    return NULL;
}

static void* worker_2(void* arg) {
    (void)arg;

    /* Acquire first lock: Lock B */
    pthread_mutex_lock(&g_lock_b);
    printf("{\"event\": \"FIRST_LOCK_ACQUIRED\", \"thread\": 2, \"lock\": \"B\"}\n");
    fflush(stdout);

    /* Synchronize with Worker 1 so both hold their first lock */
    barrier_wait(&g_start_barrier);

    /* Attempt second lock: Lock A (held by Worker 1) */
    printf("{\"event\": \"ATTEMPTING_SECOND_LOCK\", \"thread\": 2, \"lock\": \"A\"}\n");
    fflush(stdout);

    pthread_mutex_lock(&g_lock_a);

    /* Unreachable under deadlock */
    printf("{\"event\": \"UNEXPECTED_PROGRESS\", \"thread\": 2}\n");
    fflush(stdout);
    pthread_mutex_unlock(&g_lock_a);
    pthread_mutex_unlock(&g_lock_b);
    return NULL;
}

int main(void) {
    barrier_init(&g_start_barrier, 2);

    pthread_t t1, t2;
    pthread_create(&t1, NULL, worker_1, NULL);
    pthread_create(&t2, NULL, worker_2, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    return 0;
}
