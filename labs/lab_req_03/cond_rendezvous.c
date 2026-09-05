#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include <stdbool.h>

/*
 * LAB-REQ-03 Checkpoint 4: Condition-Variable Rendezvous & Predicate Recheck
 *
 * Implements a condition variable event rendezvous between producer and consumer.
 * Demonstrates the mandatory pattern: re-evaluating the shared predicate in a loop
 * (`while (!predicate) pthread_cond_wait(...)`) under the associated mutex.
 * Explains that POSIX permits spurious wakeups and awakening does not guarantee predicate truth.
 */

static pthread_mutex_t g_rendezvous_mutex = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t g_rendezvous_cond = PTHREAD_COND_INITIALIZER;

static int g_data_buffer = 0;
static bool g_buffer_ready = false;
static int g_predicate_eval_count = 0;

static void* consumer_thread(void* arg) {
    (void)arg;

    pthread_mutex_lock(&g_rendezvous_mutex);

    /* Mandatory predicate recheck guard loop */
    while (!g_buffer_ready) {
        g_predicate_eval_count++;
        printf("{\"event\": \"COND_WAIT_ENTER\", \"predicate_ready\": false, \"eval_count\": %d}\n",
               g_predicate_eval_count);
        fflush(stdout);

        /* Atomically releases associated mutex and suspends thread */
        pthread_cond_wait(&g_rendezvous_cond, &g_rendezvous_mutex);

        printf("{\"event\": \"COND_WAIT_RETURN\", \"predicate_ready\": %s}\n",
               g_buffer_ready ? "true" : "false");
        fflush(stdout);
    }

    g_predicate_eval_count++;
    int consumed = g_data_buffer;
    pthread_mutex_unlock(&g_rendezvous_mutex);

    printf("{\"event\": \"COND_CONSUMED\", \"consumed_value\": %d, \"predicate_recheck_passed\": true}\n",
           consumed);
    fflush(stdout);
    return NULL;
}

static void* producer_thread(void* arg) {
    (void)arg;

    /* Bounded delay to guarantee consumer enters wait before production */
    struct timespec req = {.tv_sec = 0, .tv_nsec = 20000000L}; /* 20ms */
    nanosleep(&req, NULL);

    pthread_mutex_lock(&g_rendezvous_mutex);

    g_data_buffer = 42;
    g_buffer_ready = true;

    printf("{\"event\": \"PRODUCER_READY\", \"produced_value\": 42}\n");
    fflush(stdout);

    /* Signal waiting thread */
    pthread_cond_signal(&g_rendezvous_cond);

    pthread_mutex_unlock(&g_rendezvous_mutex);
    return NULL;
}

int main(void) {
    pthread_t t_cons, t_prod;

    pthread_create(&t_cons, NULL, consumer_thread, NULL);
    pthread_create(&t_prod, NULL, producer_thread, NULL);

    pthread_join(t_cons, NULL);
    pthread_join(t_prod, NULL);

    bool success = (g_data_buffer == 42 && g_buffer_ready && g_predicate_eval_count >= 2);

    printf("{\"event\": \"RENDEZVOUS_RESULT\", \"final_data\": %d, \"predicate_eval_count\": %d, \"success\": %s}\n",
           g_data_buffer, g_predicate_eval_count, success ? "true" : "false");
    fflush(stdout);

    pthread_mutex_destroy(&g_rendezvous_mutex);
    pthread_cond_destroy(&g_rendezvous_cond);

    return success ? 0 : 1;
}
