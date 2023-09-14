import os, sys
from const import *
from sysfuncs import *


os.system("clear cls".split()[os.name=='nt'])

handle_args()

if params.debug_mode:
    print("[*] Debug mode enabled\n")
    params.main_file = main_file = "dummy.hny"
    with open("dummy.hny", "rt") as f:
        params.code = code = f.read()
else:
    print("not implemented.")


class Pos:
    start: int
    end: int

    def __init__(self, s: int = None, e: int = None):
        if not s:
            self.start = 0
        else:
            self.start = s
        if not e:
            self.end = 0
        else:
            self.end = e
    
    def __getitem__(self, k):
        if k in (0, "x"):
            return self.start
        elif k in (1, "y"):
            return self.end
        else:
            if isinstance(k, str):
                panic(KeyError("Unknown key: "+str(k)))
            elif isinstance(k, int):
                panic(IndexError("Unknown index: "+str(k)))
            else:
                panic(TypeError("unsupported type for k: "+str(type(k).__name__)+"; use "+str(int.__name__)+" or "+str(str.__name__)))
    
    def __str__(self) -> str:
        return f"({self.start}, {self.end})"


class Token:
    type: str
    value: str
    pos: Pos

    def __init__(self, type: str = None, value: str = None, pos: Pos = None):
        if not type:
            self.type = "NONE"
        else:
            self.type = type
        if not value:
            self.value = ""
        else:
            self.value = value
        if not pos:
            self.pos = Pos()
        else:
            self.pos = pos
    
    def line(self, code: str) -> int:
        return len(code[:self.pos.start].splitlines())
    
    def column(self, code: str) -> int:
        return len(code[:self.pos.start].splitlines()[-1])
    
    def __str__(self) -> str:
        return self.type + "<" + repr(self.value) + " at " + str(self.pos) + ">"
    
    def __repr__(self) -> str:
        return "Token(" + repr(self.type) + ", " + repr(self.value) + ", " + "Pos(" + repr(self.pos.start) + ", " + repr(self.pos.end) + "))"


class Lexer:
    code: str
    tokens: list[Token]

    def __init__(self, code):
        self.code = code
        self.tokens = []
    
    def lex(self):
        code = self.code

        i: int = 0

        while i < len(code):

            if code[i] in ALPHA:
                temp = code[i]
                i+=1
                while code[i] in ALNUM and len(temp) < 63:
                    temp += code[i]
                    i+=1
                else:
                    i-=1
                    self.tokens.append(Token(NAME, temp, Pos(i-len(temp), i)))
            
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
            
            i+=1


class Node:
    type: str
    value: Token
    children: list[Token]

    def __init__(self, type: str, value: Token, children: list[Token] = None):
        self.type = type
        self.value = value
        self.children = children or []
    
    def __str__(self) -> str:
        pre = "╭" if self.children else "─"
        rval = pre+"───Node───[type: " + self.type + "; value: \"" + self.value.value + "\"; pos: " + str(self.value.pos) + "]\n│   \n"

        for number, child in enumerate(self.children):
            if isinstance(child, Node):
                rval += ("├───" if number < len(self.children) - 1 else "╰───") + \
                    str(child).replace("\n", "\n│   " if number < len(self.children) - 1 else "\n    ")+"\n│   \n"
            elif isinstance(child, Token):
                rval += ("├───" if number < len(self.children) - 1 else "╰───") + \
                    f"Token───[type: {child.type}; value: \"{child.value}\"; pos: {child.pos}]\n│   \n"
        
        return rval[:-5].replace("─╭", "─┬").removesuffix("\n")


class RootNode(Node):
    ...


class Stack:
    arr: list[object]

    def __init__(self):
        self.arr = []
    
    def __str__(self):
        return str(self.arr)
    
    def __repr__(self):
        return repr(self.arr)
    
    def push(self, *value):
        self.arr += list(value)
    
    def pop(self):
        if not self.arr:
            panic(ValueError("stack is empty"))
        return self.arr.pop()
    
    def read(self, ind = 0):
        if not self.arr:
            panic(ValueError("stack is empty"))
        return self.arr[-1-ind]

    def write(self, v):
        if not self.arr:
            panic(ValueError("stack is empty"))
        self.arr[-1] = v
    
    def is_empty(self):
        return not self.arr
    
    def shift(self, *v):
        self.pop()
        self.push(*v)

    def __repr__(self) -> str:
        return repr(self.arr[::-1])


class Parser:
    tokens: list[Token]
    tree: RootNode
    stack: Stack

    def __init__(self, tokens: list[Token] = None):
        self.tokens = tokens or ()
        self.tree = Node(ROOT, Token(NONE, "", Pos(0, 0)))
    
    def memorize(self):
        tokens = self.tokens
        tree = self.tree

        self.stack = stack = Stack()
        i = 0

        while i < len(tokens) and i < 24:
            tkn = tokens[i]

            if params.debug_mode:
                print("Parser:")
                print("├───Stack:", self.stack)
                print("├───Token:", tkn)
                # print("├───Tree:", str(self.tree).replace("\n", "\n│   "))
                print("╰───Tokens passed:", i)
                print()

            if stack.is_empty():
                if tkn.value == "class":
                    log("Class definition")
                    stack.push(CLASS_NAME)
                i += 1
                continue
                
            match stack.read():
                case CLASS_NAME:
                    if tkn.type != NAME:
                        error("Syntax error", tkn, "Expected identifier")
                    log("Class name:", repr(tkn.value))
                    stack.shift(tkn.value, CLASS_BODY_OR_SUPER)
                case CLASS_BODY_OR_SUPER:
                    if tkn.type == ARL:
                        log("Super-class definition")
                        stack.write(CLASS_SUPER)
                    if tkn.type == CUL:
                        stack.write(CLASS_BODY)
                case CLASS_SUPER:
                    if tkn.type != NAME:
                        error("Syntax error", tkn)
                    log("Super-class name:", repr(tkn.value))
                    stack.shift(tkn.value, CLASS_OPEN_BODY)
                case CLASS_OPEN_BODY:
                    if tkn.type != CUL:
                        error("Syntax error", tkn, "Expected '{'")
                    log("Opening class body")
                    stack.write(CLASS_BODY)
                case CLASS_BODY:
                    if tkn.value == "fn":
                        log("Method definition")
                        stack.push(FN_NAME)
                case FN_NAME:
                    if tkn.type not in (NAME, SYSTAG):
                        error("Syntax error", tkn, "Expected identifier or '$'")
                    if tkn.type == SYSTAG:
                        log("System method definition")
                        stack.push(SYSTAG)
                    if tkn.type == NAME:
                        log("Function name:", tkn.value)
                        stack.shift(tkn.value, FN, FN_OPEN_ARGS)
                case SYSTAG:
                    if tkn.type != NAME:
                        error("Syntax error", tkn, "Expected identifier")
                    log("Function name:", tkn.value)
                    stack.pop()
                    stack.shift("$"+tkn.value, FN, FN_OPEN_ARGS)
                case FN_OPEN_ARGS:
                    if tkn.type != PAL:
                        error("Syntax error", tkn, "Expected '('")
                    stack.write(FN_ARG_NAME_OR_ARGS_CLOSE)
                case FN_ARG_NAME_OR_ARGS_CLOSE:
                    if tkn.type not in (NAME, PAR):
                        error("Syntax error", tkn, "Expected identifier")
                    if tkn.type == NAME:
                        log("Argument name:", tkn.value)
                        stack.shift(tkn.value, FN_ARG_COLON)
                    elif tkn.name == PAR:
                        log("End of args list")
                        ...
                case FN_ARG_COLON:
                    if tkn.type != COLON:
                        error("Syntax error", tkn, "Expected ':'")
                    stack.write(FN_ARG_TYPE)
                case FN_ARG_TYPE:
                    if tkn.type != NAME:
                        error("Syntax error", tkn, "Expected identifier")
                    stack.shift({"type": tkn.value, "array": False, "len": -1}, FN_ARG_COMMA_OR_ARRAY_OR_CLOSE)
                case FN_ARG_COMMA_OR_ARRAY_OR_CLOSE:
                    if tkn.type == LT:
                        stack.pop()
                        log("Arg type is array of", stack.read())
                        stack.read["array"] = True
                        stack.push(FN_ARG_INT_OR_CLOSE_ARRAY)
                    elif tkn.type == COMMA:
                        stack.pop()
                        log("Arg type is", stack.read())
                        stack.push(FN_ARG_COMMA_OR_CLOSE)
                    elif tkn.type == PAR:
                        log("No more args")
                        stack.write(FN_BODY_OPEN_OR_ARR)
                    else:
                        error("Syntax error", tkn, "Expected ',' or ')' or '<'")
                case FN_ARG_COMMA_OR_CLOSE:
                    if tkn.type == COMMA:
                        log("More args was provided")
                        stack.write(FN_BODY_OPEN_OR_ARR)
                    elif tkn.type == PAR:
                        log("No more args")
                    else:
                        error("Syntax error", tkn, "Expected ',' or ')'")
                case FN_ARG_INT_OR_CLOSE_ARRAY:
                    if tkn.type == INT:
                        log("Array len =", tkn.value)
                        stack.read()["len"] = eval(tkn.value)
                        stack.shift(tkn.value, FN_ARG_CLOSE_ARRAY)
                    elif tkn.type == GT:
                        log("Array len was not provided")
                        stack.shift("-1", FN_ARG_COMMA_OR_CLOSE)
                    else:
                        error("Syntax error", tkn, "Expected positive integer or '>'")
                case FN_ARG_CLOSE_ARRAY:
                    if tkn.type == GT:
                        stack.shift(tkn.value, FN_ARG_COMMA_OR_CLOSE)
                    else:
                        error("Syntax error", tkn, "Expected '>'")
                case FN_BODY_OPEN_OR_ARR:
                    if tkn.type == CUL:
                        stack.shift(FN_BEGIN, FN_BODY)
                    elif tkn.type == ARR:
                        stack.write(FN_RTYPE)
                    else:
                        error("Syntax error", tkn, "Expected '->' or '{'")
                case FN_RTYPE:
                    if tkn.type == NAME:
                        stack.shift(tkn.value, FN_OPEN_BODY)
                    else:
                        error("Syntax error", tkn, "Expected '->' or '{'")
                case FN_BODY:
                    if tkn.type == NAME:
                        if tkn.value == "if":
                            stack.push(IF_COND)
                        elif tkn.value == "free":
                            stack.push(FREE_NAME)
                        elif tkn.value == "unlink":
                            stack.push(UNLINK_NAME)
                        elif tkn.value == "return":
                            stack.push(RETURN_VALUE)
                        elif tkn.value == "while":
                            stack.push(WHILE_VALUE)
                        else:
                            stack.shift(tkn.value, CALL_OR_DEFINE_OR_ASSIGN)
                case CALL_OR_DEFINE_OR_ASSIGN:
                    if tkn.type == DOT:
                        stack.pop()
                        stack.write(stack.read()+"."+tokens[i+1].value)
                        stack.push(CALL_OR_DEFINE_OR_ASSIGN)
                        i+=1
                    elif tkn.type == ASSIGN:
                        stack.write(ASSIGN)
                    elif tkn.type == COLON:
                        stack.write(DEFINITION)
                    elif tkn.type == PAL:
                        stack.shift(CALL_ARGS, EXPR)
                    else:
                        error("Syntax error", tkn, "Expected '.' or '?=' or '=' or '??' or '('")
                case EXPR:
                    if tkn.type == STRING:
                        stack.pop()
                        stack.shift({"class": LITERAL, "type": STRING, "value": tkn.value}, stack.pop(), EXPR_OP)
                    elif tkn.type == INT:
                        stack.shift({"class": LITERAL, "type": INT, "value": tkn.value}, stack.pop(), EXPR_OP)
                    elif tkn.type == ELLIPSE:
                        stack.shift({"class": LITERAL, "type": ELLIPSE, "value": tkn.value}, stack.pop(), EXPR_OP)
                    elif tkn.type == NAME:
                        stack.shift({"class": LITERAL, "type": ELLIPSE, "value": tkn.value}, stack.pop(), EXPR_CALL_OR_OP)
                    else:
                        stack.pop()
                case EXPR_OP:
                    if tkn.type == PLUS:
                        log("Plus")
                    else:
                        stack.pop()
                        i-=1
                case CALL_ARGS:
                    if tkn.type == COMMA:
                        stack.push(EXPR)
                case PAR:
                    stack.shift(CALL_END, FN_BODY)
                case _:
                    error("Syntax error", tkn, "Expected ',' or ')'")
            i += 1


lexer = Lexer(code)

lexer.lex()

parser = Parser(lexer.tokens)

parser.memorize()

sys.exit(params.exit_status)
