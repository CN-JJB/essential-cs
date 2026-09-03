/*
 * M05 Static Type Checking Fixture
 *
 * Demonstrates a type mismatch diagnostic: assigning a string literal pointer
 * (const char *) to an integer variable (int).
 *
 * GCC diagnostic behavior:
 * - Default flags (gcc -c type_check.c): emits a warning (incompatible pointer to integer conversion).
 * - Promoted flags (gcc -c -Werror type_check.c): compiler diagnostic is promoted to an error,
 *   causing compilation to fail before producing object code.
 */

int main(void) {
    const char *text = "5";
    int number = text;
    return number;
}
