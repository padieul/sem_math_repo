from .math_types import FormulaType, FormulaContextType


class Comparer:

    def __init__(self, f_c_type: FormulaContextType, f_type: FormulaType) -> None:
        
        self._f_c_type = f_c_type 
        self._f_type = f_type
        self._same_formula_str = self._same_formula()

    def _same_formula(self) -> bool:
        form_str1 = self._f_c_type.get_formula_str() 
        form_str2 = self._f_type.get_formula_str() 
        if form_str1 == form_str2:
            return True 
        else:
            return False
        

    """ 
    both - only if both components return the same type
    formula - only if formula or both components determine a type
    context - only if context or both components determine a type
    """
    def decide_type(self, priority: str = None) -> (str,str):

        assert self._same_formula_str, "FormulaType and FormulaContextType objects do not" + \
                                       "describe the same formula"

        f_c_type_str = self._f_c_type.get_math_type() 
        f_type_str = self._f_type.get_math_type()

        match priority:

            case "both":
                if f_c_type_str == f_type_str:
                    return (f_c_type_str, "both")
                else:
                    return ("UNK", "undecided")
            case "formula":
                if f_c_type_str == f_type_str:
                    return (f_c_type_str, "both")
                elif not f_type_str == "UNK":
                    return (f_type_str, "formula")
                else:
                    return ("UNK", "undecided")
            case "context":
                if f_c_type_str == f_type_str:
                    return (f_c_type_str, "both")
                elif not f_c_type_str == "UNK":
                    return (f_c_type_str, "context")
                else:
                    return ("UNK", "undecided")

    def print_out(self, decision_str):
        self._f_c_type.print_context()
        self._f_type.print_type()
        print("COMPARER decision: ", decision_str)

    
    