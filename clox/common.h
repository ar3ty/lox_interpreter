#ifndef clox_common_h
#define clox_common_h

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

//this wrapper around wrapper i built for my testing enviroment
#ifndef TEST_MAKE
#define DEBUG_PRINT_CODE
#define DEBUG_TRACE_EXECUTION
#define DEBUG_STRESS_GC
#define DEBUG_LOG_GC
#endif

#define UINT8_COUNT (UINT8_MAX + 1)

#endif