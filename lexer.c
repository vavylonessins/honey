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
    char* data
    struct Stack * next;
} stack;

stack new_stack() {
    stack S;
    S.data = NULL;
    S.next = NULL;
    return S;
}

char is_emptyCh(stack* S) {
    return !(S->data == 0);
}

void pushCh(stack )
{
    
}

void popCh()
{
    
}

void showCh()
{
    
}
