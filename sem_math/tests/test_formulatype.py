import unittest
import os
from sem_math.math_types import FormulaType


class Test_FormulaType(unittest.TestCase):
    
    def test_for_set_type(self):

        type_strs = []
        set_strs = [
                        #"\\cal P^n(\Bbb N)", \
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
                        #"(-1/n,1/n)", \
                        #"\{\; R\;\; | \\quad R \;\\subset\; V \\times N \}", \
                        #"\{(a,c),(a,d),(b,c),(b,d)\}", \
                        #"\{ n + \\frac{(-1)^n}{n} : n \\in \\mathbb{N}\}", \
                        "\{1,2,3\}", \
                   ]   
        answer_strs = ["SET" for i in range(len(set_strs))]

        for st in set_strs:
            pars = FormulaType(st)
            pars.determine_formula_type()
            type_strs.append(pars.get_math_type())
        self.assertEqual(type_strs, answer_strs)


    def test_for_func_type(self):
        type_strs = []
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
        answer_strs = ["FUNC" for i in range(len(func_strs))]

        for st in func_strs:
            pars = FormulaType(st)
            
            pars.determine_formula_type()
            type_strs.append(pars.get_math_type())
        self.assertEqual(type_strs, answer_strs)


    def test_for_unk_type(self):
        TYPE = "UNK"
        type_strs = []
        test_strs = [
                        "\left \{ 0,1 \right \}^{\mathbb{N}}\sim \left \{ 0,1,2,3 \right \}^{\mathbb{N}}", \
                        "(x,y)\in l", \
                        "x, y \in \mathbb Q", \
                        "A \subseteq X", \
                        "B\subseteq Y", \
                        "f(A)=B", \
                        "g(Y-B)=X-A",  \
                        "Z\cup W\sim W", \
                        "\#A = n", \
                        "|X|=|Y|=|X-Y|=\kappa", \
                        "\omega^*", \
                        "(\omega + \omega) \setminus \omega", \
                        "13 = 1101_2", \
                        "1101_{\mathbb{Q}} = (N \circ N \circ D \circ N) 1 = 8/3", \
                        "\\alpha +1", \
                        "x=yr", \
                        "(x,y), x \in X, y \in Y", \
                        "S\subseteq T\subseteq\mathbb{Q}", \
                        "P\subseteq Q", \
                        "\sup(A) &gt; \inf(B)", \
                        "A_n=\\lbrace n,n+1,n+2,\\dotsc\\rbrace", \
                        "n\not\in A_{n+1}", \
                        "P(A \cap B) = P(A) + P(B) - P(A \cup B)", \
                        "R = \{(1,2), (1,3), (1,4), (2,1), (2,3), (2,4), (3,1), (3,2), (3,4), (4,1), (4,1), (4,3)\}", \
                        "\exists S (\varnothing\in S\land (\\forall x \in S)x\cup \{x\}\in S)", \
                        "A+B)+C=A+(B+C)", \
                        "a \\in S_{\Omega} - X_O", \
                        "A(n)\subseteq A(m)", \
                        "(a,b)\\in R", \
                        "\\forall x(\\lnot(x&lt;x))\\land\\forall x\\forall y\\forall z(z&lt;x\\land x&lt;y\\rightarrow z&lt;y)\\land\\forall x\\forall y(x=y\\lor x&lt;y\\lor y&lt;x)", \
                    ]   
        answer_strs = [TYPE for i in range(len(test_strs))]

        for st in test_strs:
            pars = FormulaType(st)
            pars.determine_formula_type()
            type_strs.append(pars.get_math_type())
        self.assertEqual(type_strs, answer_strs)


    def test_for_scal_type(self):
        TYPE = "SCAL"
        type_strs = []
        test_strs = [   
                        "(2n+1)", \
                        "\\frac{n!}{(n-k)!}", \
                        "(b + 2 \cdot a + d \cdot g + 3^{8})", \
                        "\\binom{k+3}{n-1}", \
                        "(b+ c \cdot b) \cdot (a + b \cdot x)", \
                        "2n - 1", \
                    ]   
        answer_strs = [TYPE for i in range(len(test_strs))]

        for st in test_strs:
            pars = FormulaType(st)
            pars.determine_formula_type()
            type_strs.append(pars.get_math_type())
        self.assertEqual(type_strs, answer_strs)


if __name__ == "__main__":
    unittest.main()