#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <stdbool.h>

/*
 * LAB-REQ-03 Controlled Break: 'if' Instead of Predicate Loop
 *
 * Demonstrates the classic concurrency bug of evaluating a condition
 * variable predicate with `if` instead of a `while` loop:
 *
 *   if (!g_buffer_ready) {
 *       pthread_cond_wait(&g_rendezvous_cond, &g_rendezvous_mutex);
 *   }
 *
 * POSIX explicitly permits spurious wakeups (IEEE 1003.1). Furthermore,
 * in multi-threaded environments another thread may alter the predicate
 * before the awakened thread re-acquires the associated mutex. If `if`
 * is used, the awakened thread proceeds directly to consume state without
 * re-evaluating the predicate, resulting in premature consumption of
 * uninitialized or stale data.
 */

static pthread_mutex_t g_mutex = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t g_cond = PTHREAD_COND_INITIALIZER;
static pthread_cond_t g_consumer_waiting_cond = PTHREAD_COND_INITIALIZER;

static int g_data_buffer = 0;
static bool g_buffer_ready = false;
static bool g_consumer_waiting = false;
static int g_predicate_eval_count = 0;

static void* broken_consumer(void* arg) {
    (void)arg;

    pthread_mutex_lock(&g_mutex);

    /* BUG: Flawed pattern using `if` instead of `while`.
     * If awakened spuriously or before the producer sets g_buffer_ready,
     * the thread will NOT re-evaluate the predicate and will consume unready data! */
    if (!g_buffer_ready) {
        g_predicate_eval_count++;
        g_consumer_waiting = true;
        printf("{\"event\": \"COND_WAIT_ENTER\", \"predicate_ready\": false, \"eval_count\": %d}\n",
               g_predicate_eval_count);
        fflush(stdout);

        pthread_cond_signal(&g_consumer_waiting_cond);

        /* Wait on condition variable */
        pthread_cond_wait(&g_cond, &g_mutex);

        printf("{\"event\": \"COND_WAIT_RETURN\", \"predicate_ready\": %s}\n",
               g_buffer_ready ? "true" : "false");
        fflush(stdout);
    }

    /* Premature consumption without re-evaluating predicate! */
    int consumed = g_data_buffer;
    bool valid = g_buffer_ready;
    pthread_mutex_unlock(&g_mutex);

    printf("{\"event\": \"COND_CONSUMED\", \"consumed_value\": %d, \"predicate_recheck_passed\": %s}\n",
           consumed, valid ? "true" : "false");
    if (!valid) {
        printf("{\"event\": \"PREDICATE_BREAK_DETECTED\", \"bug\": \"if_instead_of_while\", \"unready_consumption\": true}\n");
    }
    fflush(stdout);
    return NULL;
}

static void* spurious_waker_and_producer(void* arg) {
    (void)arg;

    pthread_mutex_lock(&g_mutex);

    /* Wait until consumer is waiting */
    while (!g_consumer_waiting) {
        pthread_cond_wait(&g_consumer_waiting_cond, &g_mutex);
    }

    printf("{\"event\": \"PRODUCER_OBSERVED_CONSUMER_WAITING\"}\n");
    fflush(stdout);

    /* Spurious wakeup injection: signal condition variable BEFORE
     * placing data or setting g_buffer_ready = true */
    printf("{\"event\": \"SPURIOUS_SIGNAL_INJECTED\", \"buffer_ready\": false}\n");
    fflush(stdout);
    pthread_cond_signal(&g_cond);

    pthread_mutex_unlock(&g_mutex);
    return NULL;
}

int main(void) {
    pthread_t t_cons, t_prod;

    pthread_create(&t_cons, NULL, broken_consumer, NULL);
    pthread_create(&t_prod, NULL, spurious_waker_and_producer, NULL);

    pthread_join(t_cons, NULL);
    pthread_join(t_prod, NULL);

    /* Under `if`, consumer consumed unready data (g_buffer_ready was false).
     * The break is successfully demonstrated if predicate_recheck failed! */
    bool break_manifested = (!g_buffer_ready && g_predicate_eval_count == 1);

    printf("{\"event\": \"PREDICATE_BREAK_RESULT\", \"break_manifested\": %s, \"predicate_eval_count\": %d}\n",
           break_manifested ? "true" : "false", g_predicate_eval_count);
    fflush(stdout);

    return break_manifested ? 0 : 1;
}
