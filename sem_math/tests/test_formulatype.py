import unittest
import os
from sem_math.math_types import FormulaType


class Test_FormulaType(unittest.TestCase):
    
    def test_for_set_type(self):
          
       #self.assertEqual(first, second)
       ...

    def test_for_func_type(self):
        print("fun")
        print(os.getcwd())
        #os.chdir("C:\\Users\\prdie\\OneDrive\\Sources\\sem_math_repo\\sem_math")
        print(os.getcwd())

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

    def test_for_scal_type(self):
        ...

    def test_for_unk_type(self):
        ...


if __name__ == "__main__":
    unittest.main()