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
                        #"\\mathbb R^{2}", \
                        "\\mathbb{R}", \
                        "\\mathbb{R}^2", \
                        "A \\cup A", \
                        "(A \\cap B) \\cup C ", \
                        "(S \\times B) \\cup C^G", \
                        "S \\cup S \\cup S", \
                        "(A \\cup B) \\times (D \\cap C)", \
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
                        "(b+ c \cdot b) \cdot (a + b \cdot x)"
                    ]   
        answer_strs = [TYPE for i in range(len(test_strs))]

        for st in test_strs:
            pars = FormulaType(st)
            pars.determine_formula_type()
            type_strs.append(pars.get_math_type())
        self.assertEqual(type_strs, answer_strs)


if __name__ == "__main__":
    unittest.main()