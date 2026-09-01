#define _POSIX_C_SOURCE 200809L
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef ROWS
#define ROWS 4096u
#endif
#ifndef COLS
#define COLS 4096u
#endif
#define WARMUPS 2u
#define TRIALS_PER_PATTERN 15u

typedef enum { ROW_MAJOR = 0, COLUMN_MAJOR = 1 } pattern_t;

static uint64_t elapsed_ns(struct timespec a, struct timespec b) {
    if (b.tv_nsec >= a.tv_nsec) {
        return (uint64_t)(b.tv_sec - a.tv_sec) * UINT64_C(1000000000)
             + (uint64_t)(b.tv_nsec - a.tv_nsec);
    }
    return (uint64_t)(b.tv_sec - a.tv_sec - 1) * UINT64_C(1000000000)
         + (uint64_t)(UINT64_C(1000000000) + (uint64_t)b.tv_nsec - (uint64_t)a.tv_nsec);
}

__attribute__((noinline)) static uint64_t traverse(const uint32_t *data, size_t rows, size_t cols, pattern_t p) {
    uint64_t sum = 0;
    if (p == ROW_MAJOR) {
        for (size_t r = 0; r < rows; ++r)
            for (size_t c = 0; c < cols; ++c)
                sum += data[r * cols + c];
    } else {
        for (size_t c = 0; c < cols; ++c)
            for (size_t r = 0; r < rows; ++r)
                sum += data[r * cols + c];
    }
    return sum;
}

static const char *pname(pattern_t p) { return p == ROW_MAJOR ? "row" : "column"; }
static void die(const char *msg) { perror(msg); exit(EXIT_FAILURE); }

int main(int argc, char **argv) {
    const char *out_path = argc > 1 ? argv[1] : "out/raw-trials.csv";
    const size_t rows = ROWS, cols = COLS;
    if (rows == 0 || cols == 0 || rows > SIZE_MAX / cols) { fprintf(stderr, "invalid dimensions\n"); return 2; }
    const size_t count = rows * cols;
    if (count > SIZE_MAX / sizeof(uint32_t)) { fprintf(stderr, "dataset too large\n"); return 2; }
    uint32_t *data = malloc(count * sizeof(*data));
    if (!data) die("malloc");
    for (size_t i = 0; i < count; ++i) data[i] = (uint32_t)(i % 251u);

    const uint64_t expected = traverse(data, rows, cols, ROW_MAJOR);
    if (traverse(data, rows, cols, COLUMN_MAJOR) != expected) { fprintf(stderr, "checksum mismatch before timing\n"); free(data); return 3; }

    for (unsigned i = 0; i < WARMUPS; ++i) {
        if (traverse(data, rows, cols, ROW_MAJOR) != expected) return 4;
        if (traverse(data, rows, cols, COLUMN_MAJOR) != expected) return 5;
    }

    FILE *f = fopen(out_path, "w");
    if (!f) die("fopen");
    fprintf(f, "pattern,trial_number,execution_order,elapsed_ns,rows,cols,total_elements,total_bytes,checksum\n");
    unsigned row_trial = 0, col_trial = 0, order = 0;
    for (unsigned pair = 0; pair < TRIALS_PER_PATTERN; ++pair) {
        pattern_t seq[2];
        seq[0] = (pair % 2u == 0u) ? ROW_MAJOR : COLUMN_MAJOR;
        seq[1] = seq[0] == ROW_MAJOR ? COLUMN_MAJOR : ROW_MAJOR;
        for (unsigned k = 0; k < 2; ++k) {
            const pattern_t p = seq[k];
            struct timespec t0, t1;
            if (clock_gettime(CLOCK_MONOTONIC, &t0) != 0) die("clock_gettime start");
            const uint64_t sum = traverse(data, rows, cols, p);
            if (clock_gettime(CLOCK_MONOTONIC, &t1) != 0) die("clock_gettime end");
            if (sum != expected) { fprintf(stderr, "checksum mismatch during timing\n"); return 6; }
            ++order;
            const unsigned trial = p == ROW_MAJOR ? ++row_trial : ++col_trial;
            fprintf(f, "%s,%u,%u,%" PRIu64 ",%zu,%zu,%zu,%zu,%" PRIu64 "\n",
                    pname(p), trial, order, elapsed_ns(t0, t1), rows, cols, count,
                    count * sizeof(*data), sum);
        }
    }
    if (fclose(f) != 0) die("fclose");

    struct timespec res;
    if (clock_getres(CLOCK_MONOTONIC, &res) != 0) die("clock_getres");
    printf("rows=%zu cols=%zu bytes=%zu checksum=%" PRIu64 " warmups=%u trials_per_pattern=%u timer=CLOCK_MONOTONIC timer_resolution_ns=%" PRIu64 "\n",
           rows, cols, count * sizeof(*data), expected, WARMUPS, TRIALS_PER_PATTERN,
           (uint64_t)res.tv_sec * UINT64_C(1000000000) + (uint64_t)res.tv_nsec);
    free(data);
    return 0;
}
