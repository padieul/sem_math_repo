from .math_types import FormulaType 
from lark import Transformer

class TokenizeTransformer(Transformer):

    # helper function that reduces nested lists 
    # to lists of strings recursively
    def _reduce_nested_list(self, n_list):
        return_list = []
        for elem in n_list:
            if isinstance(elem, str):
                return_list.append(elem)
            elif isinstance(elem, list):
                temp_list = self._reduce_nested_list(elem)
                for t_elem in temp_list:
                    return_list.append(t_elem)
        return list(return_list)

    def _reduce(self, arg):
        if isinstance(arg, list):
            if len(arg) == 1:
                if arg[0].__class__.__name__ == "Tree":
                    return arg[0].children
                elif arg[0].__class__.__name__ == "Token":
                    return arg[0].value
                elif isinstance(arg[0], list):
                    if len(arg[0]) == 1:
                        return arg[0][0]
                    elif len(arg[0]) > 1:
                        return self._reduce_nested_list(arg[0])
                elif isinstance(arg[0], str):
                    return arg[0]
            elif len(arg) > 1:
                return self._reduce_nested_list(arg)
        return arg[0]

    ###------------------------------------------------------
    # Main rules
    ###------------------------------------------------------

    def set(self,arg):
        if isinstance(arg, list):
            """
            if len(arg) == 1 and isinstance(arg[0], str):
                return arg
            return arg[0]
            """

            if len(arg) == 1:
                return arg[0]
                #if isinstance(arg[0], str):
                    #return arg[0]
            elif len(arg) > 1:
                return self._reduce_nested_list(arg)
                """
                return_list
                for elem in arg:
                    if isinstance(elem, str):
                        return_list.append(elem)
                """
        else:
            return arg

    def scal(self,arg):
        if isinstance(arg, list):
            if len(arg) == 1:
                return arg[0]
            elif len(arg) > 1:
                return self._reduce_nested_list(arg)   
        else:
            return arg

    def func(self,arg):
        if isinstance(arg, list):
            if len(arg) == 1:
                return arg[0]
            elif len(arg) > 1:
                return self._reduce_nested_list(arg)   
        else:
            return arg

    def set_expr(self, arg):
        return self._reduce(arg)
    
    def explset(self, arg):
        return self._reduce(arg)

    def set_constant_custom(self, arg):
        if isinstance(arg, list):
            temp_list = [i for i in arg if i != None]
            if len(temp_list) == 1:
                return temp_list[0]
            else:
                return temp_list

    def func_def(self, arg):
        return self._reduce(arg)

    def func_expr(self, arg):
        return self._reduce(arg)

    def mapping(self, arg):
        return self._reduce(arg)

    def func_name(self, arg):
        return self._reduce(arg)
    
    def func_name_arg(self, arg):
        return self._reduce(arg)

    def func_composed(self, arg):
        return self._reduce(arg)

    def func_names(self, arg):
        return self._reduce(arg)

    def func_enumeration(self, arg):
        return self._reduce(arg)

    def func_composed(self, arg):
        return self._reduce(arg)

    def func_arg(self, arg):
        return self._reduce(arg)

    def set_enumeration(self, arg):
        return self._reduce(arg)

    # set_constant: set_empty | SET_BASIC
    def set_constant(self, arg):
        return self._reduce(arg)

    def enumuration(self, arg):
        return self._reduce(arg)

    def item(self, arg):
        return self._reduce(arg)

    def interval(self, arg):
        return self._reduce(arg)

    def expr(self, arg):
        return self._reduce(arg)

    def additive(self, arg):
        return self._reduce(arg)

    def mp(self, arg):
        return self._reduce(arg)

    def unary(self, arg):
        return self._reduce(arg)

    # set_atom: upper_letter | set_constant
    def set_atom(self, arg):
        return self._reduce(arg)

    def postfix(self, arg):
        return self._reduce(arg)
    
    def exp(self, arg):
        return self._reduce(arg)

    def comp(self, arg):
        return self._reduce(arg)

    def group(self, arg):
        return self._reduce(arg)

    def expr_atom(self, arg):
        return self._reduce(arg)

    ###----------------------------------------
    #  simple rules
    ###----------------------------------------
    def postfix_op(self, arg):
        return arg[0]

    def singed_number(self, arg):
        return arg[0]

    def number(self, arg):
        return arg[0]

    # integer: digit+
    def integer(self, arg):
        return arg[0]

    # digit: "0".."9"
    def digit(self, arg):
        # arg[0].value == "anon"
        return arg[0].value

    def op_to_set_pow(self, arg):
        # arg[0].type == "CARET"
        if isinstance(arg[0], str):
            return arg[0]
        else:
            return arg[0].value
        
    def set_operator_set(self, arg):
        # 
        return arg[0].value

    def upper_letter(self, arg):
        return arg[0].value

    def lower_letter(self, arg):
        return arg[0].value

    ###----------------------------------------
    #  terminals
    ###----------------------------------------
    def CMD_TIMES(self, arg):
        return arg[0].value

    def L_PAREN(self, arg):
        return arg.value
    
    def R_PAREN(self, arg):
        return arg.value 

    def L_BRACE(self, arg):
        return arg.value 

    def R_BRACE(self, arg):
        return arg.value

    def L_BRACE_LITERAL(self, arg):
        return arg.value

    def R_BRACE_LITERAL(self, arg):
        return arg.value

    def L_BRACKET(self, arg):
        return arg.value 
    
    def R_BRACKET(self, arg):
        return arg.value

    def SET_FAT(self, arg):
        # arg.type == set_fat
        return arg.value

    def ADD(self, arg):
        #arg.type == add
        return arg.value 

    def SUB(self, arg):
        #arg.type == sub 
        return arg.value 

    def MUL(self, arg):
        #arg.type == sub 
        return arg.value 
    
    def DIV(self, arg):
        #arg.type == sub 
        return arg.value 

    def BANG(self, arg):
        #arg.type == sub 
        return arg.value

    def BAR(self, arg):
        #arg.type == sub 
        return arg.value 

    def CARET(self, arg):
        #arg.type == sub 
        return arg.value 

    def UNDERSCORE(self, arg):
        #arg.type == sub 
        return arg.value  

    def COMMA(self, arg):
        return arg.value 

    def EQUAL(self, arg):
        return arg.value 

    def COLON(self, arg):
        return arg.value

    def CMD_CDOT(self, arg):
        return arg.value
    
    def CMD_DIV(self, arg):
        return arg.value
    
    def CMD_FRAC(self, arg):
        return arg.value
    
    def CMD_BINOM(self, arg):
        return arg.value

    def CMD_DBINOM(self, arg):
        return arg.value

    def CMD_TBINOM(self, arg):
        return arg.value
    
    def FUNC_NORMAL(self, arg):
        return arg.value

    def OP_FUNC_COMP(self, arg):
        return arg.value

    def TO(self, arg):
        return arg.value



if __name__ == "__main__":
    """
    formulas_dict = {"f_1_0": "A \\subset B", "f_1_1": "C + D"}
    formula_token = "f_1_0"
    token_list = ["introduce", "new", "autonomous", "cars", "Let", "f_1_0", "be", "a", "function", ".", "That"]
    formula_c_type = FormulaContextType("kb/type_context_keywords.json", token_list, formula_token, formulas_dict, 3)
    #formula_c_type.determine_formula_type(conditions = {"has_pos": ("NOUN", "left"), "has_pos_between": ("PREP", "NOUN"), "type_keyword_pos": "NOUN"})
    matching_rules = [ {"descriptor_pos": ("NOUN", "left"), "formula_dep": "not pobj"},  ### RULE 1
                       {"descriptor_dep": "attr", "formula_dep": "nsubj"} ]              ### RULE 2
    formula_c_type.find_type_descriptors(matching_rules)
    #formula_c_type.determine_formula_type(priority = 1)  # 0 - rule1, 1 - rule2
    print(formula_c_type.get_type_descriptors())
    """

    
    set_strs = [
                    #c"\\cal P^n(\Bbb N)", \
                    "\\mathbb{N}", \
                    "S \\times S", \
                    "\\mathbb{R}", \
                    "\\mathbb{R}^2", \
                    "A \\cup A", \
                    "(A \\cap B) \\cup C ", \
                    "(S \\times B) \\cup C^G", \
                    "S \\cup S \\cup S", \
                    "(A \\cup B) \\times (D \\cap C)", \
                    "\\mathbb R^{2}", \
                    "\\mathbb R^N", \
                    "[0,1]", \
                    "[0,1/2]", \
                    "\\mathbb N", \
                    "(-1, 1)", \
                    "(a, b)", \
                    "(-1/n,1/n)", \
                    #c"\{\; R\;\; | \\quad R \;\\subset\; V \\times N \}", \
                    "\{(a,c),(a,d),(b,c),(b,d)\}", \
                    #c"\{ n + \\frac{(-1)^n}{n} : n \\in \\mathbb{N}\}", \
                    "\{1,2,3\}", \
                ]   

    func_strs = [   "f", \
                    "f : X \\to 2^Y", \
                    "f : X \\to \{1,2,3\}", \
                    "f : \\mathbb{Q} \\rightarrow \\{1,2,3\\}", \
                    "F\\colon A\\times A\\to A",  \
                    "f,g:A\\to A", \
                    #"k: \omega + \omega \rightarrow \mathbb{R}", \
                    "\\tan", \
                    "f(x) = x+10", \
                    "g(x) = 3x", \
                    "f: \mathbb R \\to \mathbb R", \
                    "N(q) = 1+q", \
                    #"f\colon P(X)\\to X", \
                    "f(x) = \{ x \}", \
                    "g \circ f", \
                    "g \\circ f \\circ h", \
                    "f(x,y) = \\frac{(x + y - 2)(x + y - 1)}{2}" , \
                    #"f_n(x) = \sum_{i=0}^{n-1} 1_{[\\frac{i}{2n},\\frac{2i+1}{4n})} - 1_{[\\frac{2i+1}{4n},\\frac{i+1}{2n})}", \
                ] 

    scal_strs = [   
                    #"(2n+1)", \
                    #"\\frac{n!}{(n-k)!}", \
                    #"(b + 2 \cdot a + d \cdot g + 3^{8})", \
                    #"\\binom{k+3}{n-1}", \
                    #"(b+ c \cdot b) \cdot (a + b \cdot x)", \
                    #"(((((a + b)) + (a + (a + (b - a))))))", \
                    #"2n - 1", \
                ]  

    print("*******************************************************")
    print("*******************************************************")
    print("*******************************************************")
    for st in func_strs: #+ set_strs + func_strs:
        parsed_structure = FormulaType(st).determine_formula_type()
        print("========================================================")
        print("Formula: ", st)
        
        if parsed_structure == None:
            print("Could not parse")
            continue
        #print("Parsed structure: ")
        #print(parsed_structure.pretty())
        try:
            print("Tokenization: ", TokenizeTransformer().transform(parsed_structure))
        except:
            print("Could not transform parsed structure")