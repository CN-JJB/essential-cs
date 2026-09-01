#include <stdio.h>

struct Item {
    long value;
};

__attribute__((noinline))
long helper(long a, long b, struct Item *item) {
    long local = a + b;
    return local + item->value;
}

int main(void) {
    struct Item *item = NULL;
    puts("about to call helper with item=NULL");
    fflush(stdout);
    return (int)helper(10, 20, item);
}
