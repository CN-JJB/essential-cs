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
    struct Item item = {.value = 7};
    long result = helper(10, 20, &item);
    printf("result=%ld\n", result);
    return result == 37 ? 0 : 1;
}
