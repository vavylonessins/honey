#include <stdio.h>
#include <stdlib.h>

struct Token {
    char* type;
    char* value;
    int x;
    int y;

    // line len(code[:self.pos.start].splitlines())    
    // column len(code[:self.pos.start].splitlines()[-1])    
    // str self.type + "<" + repr(self.value) + " at " + str(self.pos) + ">"    
    // repr "Token(" + repr(self.type) + ", " + repr(self.value) + ", " + "Pos(" + repr(self.pos.start) + ", " + repr(self.pos.end) + "))"
}

// #define STACK_SIZE 1000

typedef struct Stack { 
    char* data;
    struct Stack * next;
} stack;

stack * new_stack(char* data_t, stack* stack_t) {
    stack * S = (stack *) malloc(sizeof(stack));
    S->data = data_t;
    S->next = stack_t;
    return S;
}

stack * empty_stack() {
    return new_stack(NULL, NULL);
}

char is_emptyCh(stack* S) {
    return (S->data == NULL);
}

/* pushCh(&S, "string");
 */
void pushCh(stack** S, char* str) {
    *S = new_stack(str, *S);
}

/* char* data = popCh(S);
 */
char* popCh(stack* S) {
    char* K = S->data;
    *S = S->next;
    return K;
}

char* readCh(stack* S) {
    return S->data;
}
