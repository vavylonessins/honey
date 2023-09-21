#include <stdio.h>
#include <stdlib.h>

void stacktrace(int exit_code, char* string, char* filename, int error_position) {
    // todo switch with codes and colors
    // printf(string);
    // 10 is exit code for not implemented error messages
    exit(exit_code);
}

// #define STACK_TYPE Token

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

typedef struct StackCh { 
    char* data;
    struct StackCh * next;
} stack;

stack * new_stackCh(char* data_t, stack* stack_t) {
    stack * S = (stack *) malloc(sizeof(stack));
    S->data = data_t;
    S->next = stack_t;
    return S;
}

stack * empty_stackCh() {
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

typedef struct TokenStack { 
    Token* data;
    struct TokenStack * next;
} Tstack;

Tstack * new_stackT(Token* data_t, Tstack* stack_t) {
    Tstack * S = (Tstack *) malloc(sizeof(Tstack));
    S->data = data_t;
    S->next = stack_t;
    return S;
}

Tstack * empty_stackT() {
    return new_stack(NULL, NULL);
}

char is_emptyT(Tstack* S) {
    return (S->data == NULL);
}

/* pushT(&S, token);
 */
void pushT(Tstack** S, Token* token) {
    *S = new_stack(token, *S);
}

/* Token data = *popT(S);
 */
Token* popT(Tstack* S) {
    Token* K = S->data;
    *S = S->next;
    return K;
}

Token* readT(Tstack* S) {
    return S->data;
}

char strin(char c, char* str) {
    char i, out = 0;
    for (i = 0; str[i] == "\0"; i++) 
        if (str[i] == c) out = 1; 
    return out;
}

??? lex(char* code) {
    int i, strnum = 0;

    for (i = 0;i < strlen(code);i++) {
        if strin(code[i], ALPHA) {
            temp = code[i];
            i++;
            while code[i] in ALNUM and len(temp) < 63:
                temp += code[i]
                i++;
            else:
                i--;
                self.tokens.append(Token(NAME, temp, Pos(i-len(temp), i)))
        }
        elif code[i] in DIGIT and (code[i] != "0" or code[i+1] not in DIGIT):
            temp = code[i]
            i+=1
            while code[i] in DIGIT and len(temp) < 20:
                temp += code[i]
                i+=1
            else:
                i-=1
                self.tokens.append(Token(INT, temp, Pos(i-len(temp), i)))
        
        elif code[i] == '"':
            i+=1
            temp = ""
            while code[i] != '"':
                if code[i] == "\\":
                    if code[i+1] == '"':
                        i+=1
                        temp += '"'
                    else:
                        temp += "\\"
                else:
                    temp += code[i]
                i+=1
            self.tokens.append(Token(STRING, eval('"'+temp+'"'), Pos(i-len(temp), i)))
        
        elif code[i] == ",":
            self.tokens.append(Token(COMMA, ",", Pos(i, i)))
        
        elif code[i] == "<":
            if code[i+1] == "-":
                self.tokens.append(Token(ARL, "<-", Pos(i, i:=i+1)))
            elif code[i+1] == "=":
                self.tokens.append(Token(LE, "<=", Pos(i, i:=i+1)))
            elif code[i+1] == "<":
                self.tokens.append(Token(SHL, "<<", Pos(i, i:=i+1)))
            elif code[i+1] == "~":
                self.tokens.append(Token(RESERVED, "<-", Pos(i, i:=i+1)))
            elif code[i+1] == ">":
                self.tokens.append(Token(ARRAYTYPE, "<-", Pos(i, i:=i+1)))
            else:
                self.tokens.append(Token(LT, "<", Pos(i, i)))
        
        elif code[i] == ">":
            if code[i+1] == "=":
                self.tokens.append(Token(GE, ">=", Pos(i, i:=i+1)))
            elif code[i+1] == ">":
                self.tokens.append(Token(SHR, ">>", Pos(i, i:=i+1)))
            else:
                self.tokens.append(Token(GT, ">", Pos(i, i)))
        
        elif code[i] == "=":
            if code[i+1] == ">":
                self.tokens.append(Token(SO, "=>", Pos(i, i:=i+1)))
            elif code[i+1] == "=":
                self.tokens.append(Token(EQUAL, "==", Pos(i, i:=i+1)))
            else:
                self.tokens.append(Token(ASSIGN, "=", Pos(i, i)))
        
        elif code[i] == ".":
            if code[i+1] == ".":
                self.tokens.append(Token(RANGE, "..", Pos(i, i:=i+1)))
            elif code[i+1]+code[i+2] == "..":
                self.tokens.append(Token(ELLIPSE, "...", Pos(i, i:=i+2)))
            else:
                self.tokens.append(Token(DOT, ".", Pos(i, i)))
        
        elif code[i] == "!":
            if code[i+1] == "=":
                self.tokens.append(Token(NE, "!=", Pos(i, i:=i+1)))
            else:
                self.tokens.append(Token(NOT, "!", Pos(i, i)))
        
        elif code[i] == ":":
            self.tokens.append(Token(COLON, ":", Pos(i, i)))
        
        elif code[i] == "-":
            if code[i+1] == ">":
                self.tokens.append(Token(ARR, "->", Pos(i, i:=i+1)))
            if code[i+1] == "=":
                self.tokens.append(Token(MINUSASSIGN, "-=", Pos(i, i:=i+1)))
            if code[i+1] == "-":
                self.tokens.append(DEC, "--", Pos(i, i:=i+1))
            else:
                self.tokens.append(Token(MINUS, "-", Pos(i, i)))
        
        elif code[i] == "+":
            if code[i+1] == "=":
                self.tokens.append(Token(PLUSASSIGN, "+=", Pos(i, i:=i+1)))
            if code[i+1] == "-":
                self.tokens.append(INC, "++", Pos(i, i:=i+1))
            else:
                self.tokens.append(Token(PLUS, "+", Pos(i, i)))
        
        elif code[i] == "~":
            if code[i+1] == "~":
                self.tokens.append(Token(NEGASSIGN, "~~", Pos(i, i:=i+1)))
            else:
                self.tokens.append(Token(NEG, "~", Pos(i, i)))
        
        elif code[i] == "$":
            self.tokens.append(Token(SYSTAG, "$", Pos(i, i)))
        
        elif code[i] == "*":
            if code[i+1] == "*":
                if code[i+2] == "=":
                    self.tokens.append(Token(POWASSIGN, "**=", Pos(i, i:=i+2)))
                else:
                    self.tokens.append(Token(POW, "**", Pos(i, i:=i+1)))
            elif code[i+1] == "=":
                self.tokens.append(Token(MULASSIGN, "*=", Pos(i, i:=i+1)))
            else:
                self.tokens.append(Token(MUL, "*", Pos(i, i)))
        
        elif code[i] == "/":
            if code[i+1] == "/":
                if code[i+2] == "=":
                    self.tokens.append(Token(IDIVASSIGN, "//=", Pos(i, i:=i+2)))
                else:
                    self.tokens.append(Token(IDIV, "//", Pos(i, i:=i+1)))
            elif code[i+1] == "=":
                self.tokens.append(Token(DIVASSIGN, "/=", Pos(i, i:=i+1)))
            else:
                self.tokens.append(Token(DIV, "/", Pos(i, i)))
        
        elif code[i] == "%":
            if code[i+1] == "%":
                self.tokens.append(Token(MODAPPLY, f"%%", Pos(i, i:=i+1)))
            elif code[i+1] == "=":
                self.tokens.append(Token(MODASSIGN, "%=", Pos(i, i:=i+1)))
            else:
                self.tokens.append(Token(MOD, "%", Pos(i, i)))
        
        elif code[i] == "|":
            if code[i+1] == "|":
                self.tokens.append(Token(BOOLOR, "||", Pos(i, i:=i+1)))
            elif code[i+1] == "=":
                self.tokens.append(Token(ORASSIGN, "|=", Pos(i, i:=i+1)))
            else:
                self.tokens.append(Token(OR, "|", Pos(i, i)))
        
        elif code[i] == "^":
            if code[i+1] == "^":
                self.tokens.append(Token(BOOLXOR, "^^", Pos(i, i:=i+1)))
            elif code[i+1] == "=":
                self.tokens.append(Token(XORASSIGN, "^=", Pos(i, i:=i+1)))
            else:
                self.tokens.append(Token(XOR, "^", Pos(i, i)))
        
        elif code[i] == "&":
            if code[i+1] == "&":
                self.tokens.append(Token(BOOLAND, "&&", Pos(i, i:=i+1)))
            elif code[i+1] == "=":
                self.tokens.append(Token(ANDASSIGN, "&=", Pos(i, i:=i+1)))
            else:
                self.tokens.append(Token(AND, "&", Pos(i, i)))
        
        elif code[i] in "()[]{}":
            self.tokens.append(Token("PAL PAR BLL BLR CUL CUR".split()["()[]{}".index(code[i])], code[i], Pos(i, i)))

        if (code[i] == '\n') strnum++;
