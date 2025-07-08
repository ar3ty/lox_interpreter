#include "test.h"
#include "chunk.h"
#include "compiler.h"

void compilatorCheck() { 
    Chunk chunk;
    initChunk(&chunk);

    const char* source = "43";
    bool success = compile(source, &chunk);
    ASSERT(success);
    ASSERT(chunk.code[0] == OP_CONSTANT);
    ASSERT(chunk.constants.values[0].as.number == 43);

    freeChunk(&chunk);
}

void operatorPrecedenceCheck() {
    Chunk chunk;
    initChunk(&chunk);

    const char* source = "1 + 2 * 3";
    bool success = compile(source, &chunk);
    ASSERT(success);
    ASSERT(chunk.code[0] == OP_CONSTANT);
    ASSERT(chunk.constants.values[chunk.code[1]].as.number == 1);
    ASSERT(chunk.code[2] == OP_CONSTANT);
    ASSERT(chunk.constants.values[chunk.code[3]].as.number == 2);
    ASSERT(chunk.code[4] == OP_CONSTANT);
    ASSERT(chunk.constants.values[chunk.code[5]].as.number == 3);
    ASSERT(chunk.code[6] == OP_MULTIPLY);
    ASSERT(chunk.code[7] == OP_ADD);

    freeChunk(&chunk);
}