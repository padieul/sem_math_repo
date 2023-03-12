
from lark import Transformer, Token

class FormulaTreeTransformer(Transformer):

    def __init__(self, no_subtypes=True):
        Transformer.__init__(self)
        self._no_subtypes = no_subtypes

    # helper function that reduces nested lists 
    # to lists of strings recursively
    def _reduce_nested_list(self, n_list):
        return_list = []
        for elem in n_list:
            if isinstance(elem, str):
                return_list.append(elem)
            elif isinstance(elem, tuple):
                return_list.append(elem)
            elif isinstance(elem, list):
                temp_list = self._reduce_nested_list(elem)
                for t_elem in temp_list:
                    return_list.append(t_elem)
        return list(return_list)

    def _reduce(self, arg, current_type):
        if isinstance(arg, list):
            if len(arg) == 1:
                if arg[0].__class__.__name__ == "Tree":
                    if self._no_subtypes:
                        return arg[0].children
                    else:
                        return (arg[0].children, current_type)
                elif arg[0].__class__.__name__ == "Token":
                    if self._no_subtypes:
                        return arg[0].value
                    else:
                        return ((arg[0].value, arg[0].type), current_type)
                elif isinstance(arg[0], list):
                    if len(arg[0]) == 1:
                        return arg[0][0]
                    elif len(arg[0]) > 1:
                        return self._reduce_nested_list(arg[0])
                elif isinstance(arg[0], str):
                    return arg[0]
                elif isinstance(arg[0], tuple):
                    
                    if self._no_subtypes:
                        return arg[0]
                    else:
                        return (arg[0], current_type)
                    
                    #return arg[0]
            elif len(arg) > 1:
                if self._no_subtypes:
                    return self._reduce_nested_list(arg)
                else:
                    return (self._reduce_nested_list(arg), current_type)
        return arg[0]

    def _reduce_b_to_tuple(self, arg):
        if self._no_subtypes:
            return arg.value
        else:
            return (arg.value, arg.type)

    def _reduce_composed_to_tuple(self, arg):
        if self._no_subtypes:
            return arg[0].value 
        else:
            return (arg[0].value, arg[0].type)


    ###------------------------------------------------------
    # Main rules
    ###------------------------------------------------------

    def set(self,arg):
        # TODO give set type
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
                return (self._reduce_nested_list(arg), "set")

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
        if isinstance(arg, tuple):
            return (arg, "func")
        if isinstance(arg, list):
            if len(arg) == 1:
                return arg[0]
            elif len(arg) > 1:
                return (self._reduce_nested_list(arg), "func")
        else:
            return arg

    def set_expr(self, arg):
        return self._reduce(arg, "set_expr")
    
    def explset(self, arg):
        return self._reduce(arg, "explset")

    def set_constant_custom(self, arg):
        if isinstance(arg, list):
            temp_list = [i for i in arg if i != None]
            if len(temp_list) == 1:
                return temp_list[0]
            else:
                return temp_list

    def func_def(self, arg):
        return self._reduce(arg, "func_def")

    def func_expr(self, arg):
        return self._reduce(arg, "func_expr")

    def mapping(self, arg):
        return self._reduce(arg, "mapping")

    def func_name(self, arg):
        return self._reduce(arg, "func_name")
    
    def func_name_arg(self, arg):
        return self._reduce(arg, "func_name_arg")

    def func_composed(self, arg):
        return self._reduce(arg, "func_composed")

    def func_names(self, arg):
        return self._reduce(arg, "func_names")

    def func_enumeration(self, arg):
        return self._reduce(arg, "func_enumeration")

    def func_composed(self, arg):
        return self._reduce(arg, "func_composed")

    def func_arg(self, arg):
        return self._reduce(arg, "func_arg")

    def set_enumeration(self, arg):
        return self._reduce(arg, "set_enumeration")

    # set_constant: set_empty | SET_BASIC
    def set_constant(self, arg):
        return self._reduce(arg, "set_constant")

    def enumuration(self, arg):
        return self._reduce(arg, "enumeration")

    def item(self, arg):
        return self._reduce(arg, "item")

    def interval(self, arg):
        return self._reduce(arg, "interval")

    def expr(self, arg):
        return self._reduce(arg, "expr")

    def additive(self, arg):
        return self._reduce(arg, "additive")

    def mp(self, arg):
        return self._reduce(arg, "mp")

    def unary(self, arg):
        return self._reduce(arg, "unary")

    # set_atom: upper_letter | set_constant
    def set_atom(self, arg):
        return self._reduce(arg, "set_atom")

    def postfix(self, arg):
        return self._reduce(arg, "postfix")
    
    def exp(self, arg):
        return self._reduce(arg, "exp")

    def comp(self, arg):
        return self._reduce(arg, "comp")

    def group(self, arg):
        return self._reduce(arg, "group")

    def expr_atom(self, arg):
        return self._reduce(arg, "expr_atom")

    def integer(self, arg):
        return self._reduce(arg, "integer")

    def op_to_set_pow(self, arg):
        return self._reduce(arg, "op_to_set_pow")

    def number(self, arg):
        return self._reduce(arg, "number")

    def singed_number(self, arg):
        return self._reduce(arg, "singed_number")

    def postfix_op(self, arg):
        return self._reduce(arg, "postfix_op")

    def op_to_set_pow(self, arg):
        return self._reduce(arg, "op_to_set_pow")


    ###----------------------------------------
    #  simple rules
    ###----------------------------------------
    """
    def postfix_op(self, arg):
        return self._reduce_composed_to_tuple(arg)

    def singed_number(self, arg):
        return self._reduce_composed_to_tuple(arg)

    def number(self, arg):
        return self._reduce_composed_to_tuple(arg)


    # integer: digit+
    def integer(self, arg):
        return self._reduce_composed_to_tuple(arg)
    

    # digit: "0".."9"
    def digit(self, arg):
        return self._reduce_composed_to_tuple(arg)

    
    def op_to_set_pow(self, arg):
        return self._reduce_composed_to_tuple(arg)
    """
        
    # digit: "0".."9"
    def digit(self, arg):
        return self._reduce_composed_to_tuple(arg)

    def set_operator_set(self, arg):
        return self._reduce_composed_to_tuple(arg)

    def upper_letter(self, arg):
        return self._reduce_composed_to_tuple(arg)

    def lower_letter(self, arg):
        return self._reduce_composed_to_tuple(arg)

    ###----------------------------------------
    #  terminals
    ###----------------------------------------
    def CMD_TIMES(self, arg):
        return self._reduce_b_to_tuple(arg)

    def L_PAREN(self, arg):
        return self._reduce_b_to_tuple(arg)
    
    def R_PAREN(self, arg):
        return self._reduce_b_to_tuple(arg) 

    def L_BRACE(self, arg):
        return self._reduce_b_to_tuple(arg) 

    def R_BRACE(self, arg):
        return self._reduce_b_to_tuple(arg) 

    def L_BRACE_LITERAL(self, arg):
        return self._reduce_b_to_tuple(arg) 

    def R_BRACE_LITERAL(self, arg):
        return self._reduce_b_to_tuple(arg) 

    def L_BRACKET(self, arg):
        return self._reduce_b_to_tuple(arg)  
    
    def R_BRACKET(self, arg):
        return self._reduce_b_to_tuple(arg) 

    def SET_FAT(self, arg):
        # arg.type == set_fat
        return self._reduce_b_to_tuple(arg) 

    def ADD(self, arg):
        #arg.type == add
        return self._reduce_b_to_tuple(arg) 

    def SUB(self, arg):
        #arg.type == sub 
        return self._reduce_b_to_tuple(arg) 

    def MUL(self, arg):
        #arg.type == sub 
        return self._reduce_b_to_tuple(arg) 
    
    def DIV(self, arg):
        #arg.type == sub 
        return self._reduce_b_to_tuple(arg)

    def BANG(self, arg):
        #arg.type == sub 
        return self._reduce_b_to_tuple(arg)

    def BAR(self, arg):
        #arg.type == sub 
        return self._reduce_b_to_tuple(arg) 

    def CARET(self, arg):
        #arg.type == sub 
        return self._reduce_b_to_tuple(arg)

    def UNDERSCORE(self, arg):
        #arg.type == sub 
        return self._reduce_b_to_tuple(arg) 

    def COMMA(self, arg):
        return self._reduce_b_to_tuple(arg)

    def EQUAL(self, arg):
        return self._reduce_b_to_tuple(arg)

    def COLON(self, arg):
        return self._reduce_b_to_tuple(arg)

    def CMD_CDOT(self, arg):
        return self._reduce_b_to_tuple(arg)
    
    def CMD_DIV(self, arg):
        return self._reduce_b_to_tuple(arg)
    
    def CMD_FRAC(self, arg):
        return self._reduce_b_to_tuple(arg)
    
    def CMD_BINOM(self, arg):
        return self._reduce_b_to_tuple(arg)

    def CMD_DBINOM(self, arg):
        return self._reduce_b_to_tuple(arg)

    def CMD_TBINOM(self, arg):
        return self._reduce_b_to_tuple(arg)
    
    def FUNC_NORMAL(self, arg):
        return self._reduce_b_to_tuple(arg)

    def OP_FUNC_COMP(self, arg):
        return self._reduce_b_to_tuple(arg)

    def TO(self, arg):
        return self._reduce_b_to_tuple(arg)