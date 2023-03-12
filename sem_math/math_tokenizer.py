#from .math_types import FormulaType 
#import math_types.FormulaType as FormulaType
from lark import Visitor
from rich import print as r_print
from rich.tree import Tree as RTree


if not __name__ == "__main__":
    from .math_types import FormulaType
    from .ft_transformer import FormulaTreeTransformer

class SemMathTokenizer:

    def __init__(self, parsed_structure, no_subtypes=True):
        
        self._parsed_formula_tree = parsed_structure
        self._tokenizer = FormulaTreeTransformer(no_subtypes)
        self._no_subtypes = no_subtypes

        self._tokenization = None

    def get_tokens(self):
        self._tokenization = self._tokenize()
        if self._no_subtypes:
            return self._tokenization
        elif not self._no_subtypes:
            return self._serialize(self._tokenization)

    def _print_token_list(self, token_list):
        if isinstance(token_list, str):
            print("[ " + token_list + " ]")
        elif isinstance(token_list, list):
            for token in token_list:
                print("[ " + token + " ]")

    def display_tokens(self, retokenize=False):
        if self._tokenization == None or retokenize:
            self._tokenization = self._tokenize()

        if self._no_subtypes:
            #print(self._tokenization)
            token_list = self._tokenization
            self._print_token_list(token_list)
        elif not self._no_subtypes:
            #print(self._serialize(self._tokenization))
            token_list = self._serialize(self._tokenization)
            self._print_token_list(token_list)

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

    def _tokenize(self):
        try:
            tokenization = self._tokenizer.transform(self._parsed_formula_tree)
            if self._no_subtypes:
                tokenization = self._merge_special_tokens(tokenization)
        except Exception as e:
            print(e)
        return tokenization

    def _merge_special_tokens(self, arg_list):
        if isinstance(arg_list, list):
            return self._merge_numeric_tokens(arg_list)
        elif isinstance(arg_list, str):
            return [arg_list]

    def _merge_numeric_tokens(self, arg_list):
        new_arg_list = []
        numeric_str = ""
        for token in arg_list:
            if token.isnumeric():
                numeric_str += token
            else:
                if not numeric_str == "":
                    new_arg_list.append(numeric_str)
                    numeric_str = ""
                else:
                    ...
                new_arg_list.append(token)      

        if not numeric_str == "":
            new_arg_list.append(numeric_str)
        return new_arg_list

    def _serialize(self, arg):
        def serialize_recur(arg):
            if isinstance(arg, str):
                return arg
            elif isinstance(arg, tuple):
                if len(arg) == 2:
                    return self._reduce_nested_list([arg[1], serialize_recur(arg[0])])
                else:
                    ...
            elif isinstance(arg, list):
                if len(arg) == 1:
                    return arg[0]
                elif len(arg) > 1:
                    return self._reduce_nested_list([serialize_recur(elem) for elem in arg])

        def clean_recur(arg):
            if isinstance(arg, str):
                return None
            elif isinstance(arg, tuple):
                m_tokens, m_type = arg
                temp_m_tokens = clean_recur(m_tokens)
                if temp_m_tokens == None:
                    return m_type
                else:
                    return (temp_m_tokens, m_type)
            elif isinstance(arg, list):
                if len(arg) == 1:
                    return clean_recur(arg[0])
                else:
                    return [clean_recur(elem) for elem in arg]

        # TODO: do something to serialize
        arg = clean_recur(arg)
        arg = serialize_recur(arg)
        return arg



class TreeToTok(Visitor):
    def __init__(self):
        self._some_list = []
        
    def set_empty(self, arg):
        print(arg)
        self._some_list.append(arg)

    def SET_BASIC(self, arg):
        print(arg)
        self._some_list.append(arg)

        """
        def set_expr(self, arg):
            for elem in arg.children:
                if not elem == None:
                    token_type = elem.type 
                    token_val = elem.value
                    if not token_type == "RULE":
                        self._some_list.append(token_val)
        """
        
    def set_constant(self, arg):
        print(arg)
        for elem in arg.children:
            if not elem == None:
                token_type = elem.type 
                token_val = elem.value
                if not token_type == "RULE":
                    self._some_list.append(token_val)

    #self._some_list.append(arg)
    def set_operator_set(self,arg):
        print(arg)
        for elem in arg.children:
            if not elem == None:
                token_type = elem.type 
                token_val = elem.value
                if not token_type == "RULE":
                    self._some_list.append(token_val)
        
    def set_constant_custom(self, arg):
        print(arg)
        for elem in arg.children:
            if not elem == None:
                token_type = elem.type 
                token_val = elem.value
                if not token_type == "RULE":
                    self._some_list.append(token_val)

    def cmd_times(self, arg):
        print(arg)
        self._some_list.append(arg)

    def get_some_list(self, arg):
        print(arg)
        return self._some_list
    
    def __default__(self, arg):
        print(arg)




if __name__ == "__main__":
    from math_types import FormulaType
    from ft_transformer import FormulaTreeTransformer
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
    """
    set_strs = [
                   "234",
                   "234 + f", 
                   "145-7124",
                   "256 * 4135 + f(134)"
               ]
    """

    func_strs = [   "f : X \\times X \\to X", \
                    "f : X \\to X", \
                    "f", \
                    "f : X \\to 2^Y", \
                    "f : X \\to \{1,2,3\}", \
                    "f : \\mathbb{Q} \\rightarrow \\{1,2,3\\}", \
                    "F\\colon A\\times A\\to A",  \
                    "f,g:A\\to A", \
                    "k: \omega + \omega \rightarrow \mathbb{R}", \
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
                    "(2n+1)", \
                    "\\frac{n!}{(n-k)!}", \
                    "(b + 2 \cdot a + d \cdot g + 3^{8})", \
                    "\\binom{k+3}{n-1}", \
                    "(b+ c \cdot b) \cdot (a + b \cdot x)", \
                    "(((((a + b)) + (a + (a + (b - a))))))", \
                    "2n - 1", \
                ]  

    sample_strs = [
                    "f : X \\to \{1,2,3\}", \
                    "a^2 + b^2 - 234 * 6", \
                    "A \\cup A", \
                    "f(x) = sin(x)", \
                    "\sinh(x) = (e^x-e^{-x})/2", \
                    "f:S \rightarrow \mathbb{R}", \
                    "g(x) = \sin( x ) + \cos( x )", \
                    "(-1/n,1/n)", \
                    "S \\times S", \
                    "\\mathbb{R}^2", \
                    "f : X \\times X \\to X", \
                    #"\\frac{n!}{(n-k)!}", \
                  ]

    print("*******************************************************")
    print("*******************************************************")
    print("*******************************************************")
    for st in sample_strs: #+ set_strs + func_strs:
        parsed_structure = FormulaType(st).determine_formula_type()
        #print("STANDARD: ")
        if parsed_structure == None:
            continue
        #print(parsed_structure.pretty())
        
        print("========================================================")
        print("========================================================")
        print("Formula: ", st)
        
        if parsed_structure == None:
            print("Could not parse")
            continue

        #print("Parsed structure: ")
        print(parsed_structure.pretty())
        

        try:
            #some_visitor = TreeToTok()
            some_style = "encircle"
            r_tree = parsed_structure.__rich__()
            r_tree = RTree(label=r_tree, style=some_style, guide_style=some_style)

            r_print(r_tree)
            #some_visitor.visit(parsed_structure)
            sem_tok_no_subtypes = SemMathTokenizer(parsed_structure, True)
            sem_tok_with_subtypes = SemMathTokenizer(parsed_structure, False)
            
            #print("Tokenization: **********************************************************")
            print("Bare tokens: ")
    
            sem_tok_no_subtypes.display_tokens()
            print("Tokens with subtypes: ")
        
            sem_tok_with_subtypes.display_tokens()
            #print("*************************************************************************")
        except Exception as e:
            print(e)
            print("Could not transform parsed structure")