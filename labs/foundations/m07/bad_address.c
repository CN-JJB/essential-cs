/*
 * bad_address.c - Essential CS M07 Safe Memory Fault Observation
 *
 * IMPORTANT CONCEPTUAL BOUNDARY:
 * At the C language specification layer (ISO/IEC 9899), dereferencing an
 * invalid or null pointer is UNDEFINED BEHAVIOR (UB). The C standard itself
 * does NOT define or guarantee signals, hardware traps, or termination.
 *
 * At the hosted execution layer on Linux/POSIX/x86-64:
 * 1. CPU MMU attempts address translation for address 0x0.
 * 2. Address 0x0 is unmapped in the process page table, causing a hardware page fault exception.
 * 3. Linux kernel page fault handler checks the VMA list and determines address 0x0 is invalid.
 * 4. Kernel delivers SIGSEGV (signal 11) to the process, terminating it if unhandled.
 *
 * This fixture is executed ONLY inside a bounded child process by fault_runner.py.
 */

#include <stdio.h>
#include <stdlib.h>

int main(void) {
    /*
     * Use volatile pointer to prevent compiler dead-code elimination / optimization
     * under aggressive -O2/-O3 flags.
     */
    volatile int *bad_ptr = (volatile int *)0x0;

    /* Intentional invalid write: triggers hardware MMU fault on hosted system */
    *bad_ptr = 42;

    /* Normal return should never be reached on this hosted environment */
    return 0;
}
