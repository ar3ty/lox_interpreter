#ifndef test_clox_h
#define test_clox_h

#include <stdio.h>

#define RED     "\x1B[31m"
#define GREEN   "\x1B[32;1m"
#define BLUE  "\x1B[36;1m"
#define RESET   "\x1B[0m"

#define RUNTEST(name) printf(BLUE "[TEST] %30s\n" RESET, #name); \
                      name(); \
                      if (testFailureFlag == 0) { \
                        printf(GREEN "|||||||||||||||||||||||||||||||||[OK]\n" RESET "\n\n"); \
                      } else { \
                        testFailureFlag = 0; \
                        printf("\n"); \
                      }

#define ASSERT(expr) \
    do { \
        if (!(expr)) { \
            printf(RED "[ASSERT FAIL]" RESET " %s:%d\n", __FILE__, __LINE__); \
            testsFailed++; \
            testFailureFlag = 1; \
        } else { \
            testsPassed++; \
        } \
    } while (false)

extern int testsPassed;
extern int testsFailed;
extern int testFailureFlag;
    
#endif