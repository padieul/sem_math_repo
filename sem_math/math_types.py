import spacy 
import json
from lark import Lark
import os


class FormulaType:
    type_parser = None

    def __init__(self, latex_str, sel_formula_token = None, formula_dict = None) -> None:

        self._sel_formula_token = "" 
        self._formula_dict = None

        if not sel_formula_token == None and \
           not formula_dict == None:
            self._latex_str = formula_dict[sel_formula_token]
            self._sel_formula_token = sel_formula_token 
            self._formula_dict = formula_dict
        else:
            self._latex_str = latex_str 
        
        self._grammar_file = "sem_math/grammar/type_grammar.lark"
        self._parsed_structure = None
        FormulaType.read_parser_grammar(self._grammar_file)
        self._math_type = "UNK"

    def print_parsed_formula(self):
        print("--------------------------------------------")
        print("Tree data: ", self._parsed_structure.data)
        print("Tree data children: ", self._parsed_structure.children)
        print(self._parsed_structure.pretty())

    def determine_formula_type(self):
        try:
            self._parsed_structure = FormulaType.type_parser.parse(self._latex_str)
            if self._parsed_structure.data == "func":
                self._math_type = "FUNC"
            elif self._parsed_structure.data == "set":
                self._math_type = "SET"
            elif self._parsed_structure.data == "scal":
                self._math_type = "SCAL" 
        except Exception as e:
            some_val = e
            self._math_type = "UNK"

    def print_type(self):
        print("MATH-TYPE (formula): ", self._math_type)

    @classmethod
    def read_parser_grammar(cls, file_path):
        grammar_str = "" 
        file = open(file_path, mode="r") 
        grammar_str = file.read() 
        file.close()
        cls.type_parser = Lark(grammar_str, start="value", source_path = "C:\\Users\\prdie\\OneDrive\\Sources\\sem_math_repo\\sem_math", 
                                                           import_paths = ["C:\\Users\\prdie\\OneDrive\\Sources\\sem_math_repo\\sem_math\\grammar\\"])
    def get_parsed_structure(self, text):
        self._parsed_structure = FormulaType.type_parser.parse(text)

    def get_math_type(self):
        return self._math_type

    def get_formula_str(self):
        return self._latex_str

    
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

    def determine_formula_type(self, conditions: dict) -> None: 
        pos1_tag, pos1_position = conditions["has_pos"]
        pos2_tag, other_tag = conditions["has_pos_between"] 
        type_keyword_pos = conditions["type_keyword_pos"]

        if self.has_pos_in_window(pos1_tag, pos1_position):
            if not self.has_pos_between_formula_and_other(pos2_tag, other_tag):
                self._math_type = self.evaluate_math_type(type_keyword_pos, True)
        else:
            self._math_type = "UNK"


    def print_context(self):

        print("----------------------------------------------------------------------------------------------------")
        print("formula: " + str(self._formula_dict[self._sel_formula_token]))
        if not self._selected_pos_elems == {} and "NOUN" in self._selected_pos_elems.keys():
            print("noun: ", str(self._selected_pos_elems["NOUN"][0].text))
        else:
            print("NOUN: not found")
        for tok in self._context_doc:
            print("\t" + "sel_token: " + str(tok.text) + ": " + str(tok.pos_) + ": " + str(tok.dep_))
        print("MATH-TYPE (context): ", str(self.get_math_type()))

    def evaluate_math_type(self, keyword_pos, evaluate=True):
        if evaluate == True:
            for keyword in self._type_keywords.keys():
                if keyword in str(self._selected_pos_elems[keyword_pos][0].text):
                    self._math_type = self._type_keywords[keyword]
                    return self._math_type
            return self._math_type
        elif evaluate == False:
            return self._math_type
    
    def get_math_type(self):
        return self._math_type
        
    def get_formula_str(self):
        return self._formula_dict[self._sel_formula_token]

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
    print(func_strs)
    print(type_strs) 
    print(answer_strs)