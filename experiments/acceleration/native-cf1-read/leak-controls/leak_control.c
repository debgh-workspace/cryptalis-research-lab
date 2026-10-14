/* Offline detector controls only. No CF1, provider, Python, fork or secrets.
 * An intentionally unfreed allocation is made unreachable before normal exit.
 * 'leak' must be detected; 'free' must not report that allocation as leaked.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ALLOCATION_BYTES ((size_t)131071)

#if !defined(__GNUC__)
#error This frozen control requires the reviewed GCC toolchain.
#endif

__attribute__((noinline))
static int allocation_control(int release) {
    unsigned char *p = (unsigned char *)malloc(ALLOCATION_BYTES);
    if (p == NULL) return 0;
    /* Volatile stores preserve a real, touched allocation under optimization. */
    volatile unsigned char *touch = p;
    touch[0] = 0x31;
    touch[ALLOCATION_BYTES - 1] = 0x71;
    if (release) free(p);
    /* Neither pointer escapes to a global, caller, stream, or receipt. */
    return 1;
}

int main(int argc, char **argv) {
    if (argc != 2 || (strcmp(argv[1], "clean") != 0 &&
                     strcmp(argv[1], "free") != 0 &&
                     strcmp(argv[1], "leak") != 0)) {
        fputs("CONTROL invalid-mode\n", stderr);
        return 64;
    }
    if (strcmp(argv[1], "clean") != 0 &&
        !allocation_control(strcmp(argv[1], "free") == 0)) {
        fputs("CONTROL allocation-failed\n", stderr);
        return 65;
    }
    if (printf("CONTROL completed mode=%s bytes=%zu normal-return\n", argv[1],
               strcmp(argv[1], "clean") == 0 ? (size_t)0 : ALLOCATION_BYTES) < 0 ||
        fflush(stdout) != 0) return 66;
    /* Return from main, invoking ordinary sanitizer exit-time handlers. */
    return 0;
}
