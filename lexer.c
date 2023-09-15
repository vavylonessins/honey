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
