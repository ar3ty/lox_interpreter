#include "test.h"
#include "test_compiler.h"

void runAllTests() {
    RUNTEST(compilatorCheck);
    RUNTEST(operatorPrecedenceCheck);
}


int main() {
    printf("\n=========== Running tests ===========\n\n");
    runAllTests();
    if (testsPassed == 0) {
        printf(RED);
    } else {
        printf(GREEN);
    }
    printf("======= Passed: %d; ", testsPassed); 
    if (testsFailed > 0) printf(RED);
    printf("Failed: %d ======= \n\n" RESET, testsFailed);
}