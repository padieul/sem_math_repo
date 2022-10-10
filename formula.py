import latex2mathml.converter
from latex2sympy2 import latex2sympy, latex2latex




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


class Formula:

    def __init__(self, latex_str):

        self._latex_str = latex_str
        self._math_type = ""
        self._math_type_candidates = []


    def get_math_type(self):
        return self._math_type

    




if __name__ == "__main__":
    
    print(get_math_ml("\mathbb{N}"))
   
    for elem_expr in functions_ex:
        if elem_expr == "f = g \\circ g":
            continue

        expr = latex2sympy(elem_expr)
        print(expr)