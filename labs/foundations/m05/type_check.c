/*
 * M05 Static Type Checking Fixture
 *
 * Demonstrates a type mismatch diagnostic: assigning a string literal pointer
 * (const char *) to an integer variable (int).
 *
 * GCC diagnostic behavior is version/flag dependent.
 * - GCC 14 treats this int-conversion diagnostic as an error by default.
 * - GCC 14 -fpermissive can downgrade it to a warning.
 * - -Werror promotes diagnostics that are warnings under the selected compiler/options.
 * Record the actual compiler version, flags, exit code, and diagnostic; do not teach one severity
 * as a universal C-language rule.
 */

int main(void) {
    const char *text = "5";
    int number = text;
    return number;
}
