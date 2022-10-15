import latex2mathml.converter
from latex2sympy2 import latex2sympy, latex2latex
import spacy 
import json




# 1. absolute type: \mathbb{R} -> real number set
# 2. possible type candidates: f, n 
# 3. ...

functions_ex  = [   #"f", \
                    #"f = g \\circ g", \
                    #"F\\colon A\\times A\\to A", \
                    #"f : \\mathbb{Q} \\rightarrow \\{1,2,3\}", \
                    #"f(A)=B", \g(Y-B) # X - A
                    "f,g:A\\to A" ]               
                    #"f: X \\to 2^Y", \
                    #"f(x) = (x^2, \\sin x)", \
                    #"f:A^{B\\;\\cup\\; C}\\to A^B\\times A^C", \
                    #"f,g:A\\to A"]

"""
set = [  "\cal P^n(\Bbb N)", \
         "\mathbb{N}", \
         "S", \
         "S \\times S", \
         "\mathbb R^{2}", \
         "Z", "W", "A", "X", "Y", \
         "S", "\mathbb{R}", "\mathbb{R}^2", \
         "E", "", "", "", "", ""]


scal = [ "n", \
         "(2n+1)", \
         "\\frac{n!}{(n-k)!}", \
         ]

BOOL = ["", 
        ""]

UNK = [ "\left \{ 0,1 \right \}^{\mathbb{N}}\sim \left \{ 0,1,2,3 \right \}^{\mathbb{N}}", \
        "(x,y)\in l", \
        "x, y \in \mathbb Q", \
        "A \subseteq X", \
        "B\subseteq Y", \
        "f(A)=B", \
        "g(Y-B)=X-A",  \
        "Z\cup W\sim W", \
        "\#A = n", \
        "\omega", \
        "|X|=|Y|=|X-Y|=\kappa", \
        "\omega^*", \
        "", \
        ""]

"""

def get_math_ml(tex_str):
    mathml_output = latex2mathml.converter.convert(tex_str)
    return mathml_output


class FormulaType:

    def __init__(self, latex_str):

        self._latex_str = latex_str
        self._math_type = "UNK"
        self._math_type_candidates = []


    def get_math_type(self):
        return self._math_type

    
class FormulaContextType:

    _spacy_model = spacy.load("en_core_web_sm")
    
    def __init__(self, type_keywords_path, context_tokens, sel_formula_token, formula_dict, window_size = 3):
        
        self._math_type = "UNK"
        self._window_size = window_size

        self._context_tokens = context_tokens
        self._sel_formula_token = sel_formula_token
        self._formula_tokens = formula_dict.keys()
        self._formula_dict = formula_dict
        self._selected_pos_elems = {}
        
        self._context_doc = self._generate_doc()

        self._type_keywords = self._read_keywords(type_keywords_path) 

    
    def has_pos_in_window(self, pos_tag, interval):

        if interval == "left":
            left = self._window_size 
            right = 1
        elif interval == "right":
            right = self._window_size
            left = 1
        else:
            right = self._window_size 
            left = self._window_size

        has_pos = False
        count = self._context_tokens.index(self._sel_formula_token)
        for i in range(count-left, count+right, 1):
            if i == count or i < 0:
                continue
            sel_token = self._context_doc[i] 
            if sel_token.pos_ == pos_tag and not sel_token.text in self._formula_tokens:
                has_pos = True 
                self._selected_pos_elems[pos_tag] = (sel_token, i)
                break

        return has_pos

    # pos_tag: this POS:PREP         other_tag: previos POS:NOUN
    def has_pos_between_formula_and_other(self, pos_tag, other_tag):
        
        has_prep_between = False 
        other_token, other_index = self._selected_pos_elems[other_tag]
        formula_index = self._context_tokens.index(self._sel_formula_token)

        if other_index > formula_index:
            for j in range(formula_index+1,other_index):
                if self._context_doc[j].pos_ == "PREP" or self._context_doc[j].dep_ == "prep":
                    has_prep_between = True
        elif other_index < formula_index:
            for j in range(other_index+1,formula_index):
                elem = self._context_doc[j]
                if self._context_doc[j].pos_ == "PREP" or self._context_doc[j].dep_ == "prep":
                    has_prep_between = True

        return has_prep_between



    def print_context(self, with_tags = True):

        print("----------------------------------------------------------------------------------------------------")
        print("formula: " + str(self._formula_dict[self._sel_formula_token]))
        print("noun: ", str(self._selected_pos_elems["NOUN"][0].text))
        print("MATH-TYPE: ", str(self.get_math_type()))
        for tok in self._context_doc:
            print("\t" + "sel_token: " + str(tok.text) + ": " + str(tok.pos_) + ": " + str(tok.dep_))



    def get_math_type(self, evaluate=True):
        if evaluate == True:
            for keyword in self._type_keywords.keys():
                if keyword in str(self._selected_pos_elems["NOUN"][0].text):
                    self._math_type = self._type_keywords[keyword]
                    return self._math_type
            return self._math_type
        elif evaluate == False:
            return self._math_type
        
    
    def _generate_doc(self):
        context_str = "" 
        for token in self._context_tokens:
            context_str += (token + " ")
        return FormulaContextType._spacy_model(context_str)

    def _read_keywords(self, keywords_path):
        with open(keywords_path, "r") as f:
            data = json.load(f)
        f.close() 
        return data


if __name__ == "__main__":
    
    print(get_math_ml("\mathbb{N}"))
   
    for elem_expr in functions_ex:
        if elem_expr == "f = g \\circ g":
            continue

        expr = latex2sympy(elem_expr)
        print(expr)