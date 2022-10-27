import spacy 
from spacy.symbols import attr, NOUN
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

        self._type_keywords = self._read_keywords(type_keywords_path) 
        self._math_type = "UNK"
        self._window_size = window_size

        self._context_tokens = context_tokens
        self._sel_formula_token = sel_formula_token
        self._formula_tokens = formula_dict.keys()
        self._formula_dict = formula_dict

        self._textual_type_descriptors = []

        self._context_doc = self._generate_doc()

    def determine_formula_type(self, priority: int) -> None: 
        assert priority > -1 and priority < 2
        
        determined_types = []
        for candidate in self._textual_type_descriptors:
            for keyword in self._type_keywords.keys():
                if keyword in candidate["text"]:
                    determined_types.append(self._type_keywords[keyword])
                    break
                
        if len(determined_types) == 0:
            self._math_type = "UNK"
        elif len(determined_types) == 1:
            self._math_type = determined_types[0] 
        elif len(determined_types) == 2:
            self._math_type = determined_types[priority]


    def find_type_descriptors(self, matching_rules: list) -> None:
        #rule_verdicts
        for m_rule in matching_rules:
            m_keys = m_rule.keys() 

            if "descriptor_pos" in m_keys and "formula_dep" in m_keys:
                formula_dep_list = m_rule["formula_dep"].split(" ")
                if len(formula_dep_list) > 1:
                    if formula_dep_list[0] == "not":
                        formula_should_have_dep = False 
                        formula_dep = formula_dep_list[1] 
                else:
                    formula_should_have_dep = True 
                    formula_dep = formula_dep_list[0] 
                d_pos_tag, d_pos_position = m_rule["descriptor_pos"]
                self._extract_type_descriptor_rule_one(formula_should_have_dep, 
                                                       formula_dep, 
                                                       d_pos_tag, 
                                                       d_pos_position)
                    
            if "descriptor_dep" in m_keys and "formula_dep" in m_keys:
                d_dep = m_rule["descriptor_dep"] 
                f_dep = m_rule["formula_dep"]
                self._extract_type_descriptor_rule_two( d_dep, f_dep)



    def _extract_type_descriptor_rule_one(self, f_dep_bool: bool, f_dep: str, 
                                                d_pos_tag: str, d_pos_position: str) -> None:
        
        count = self._context_tokens.index(self._sel_formula_token)
        if (self._context_doc[count].dep_ == f_dep and f_dep_bool == True) or \
           (not self._context_doc[count].dep_ == f_dep and f_dep_bool == False):
            
            descriptor_dict = self._get_pos_in_window(d_pos_tag, d_pos_position)
            if not descriptor_dict == {}:
                descriptor_dict["rule"] = "one"
                self._textual_type_descriptors.append(descriptor_dict)

        else:
            ...
        
        


    def _extract_type_descriptor_rule_two(self, d_dep: str, f_dep: str) -> None:
        
        descriptor_dict = {} 

        count = self._context_tokens.index(self._sel_formula_token)
        interval_size = len(self._context_tokens) // 2
        if self._context_doc[count].dep_ == f_dep:
            attr_count = 0
            for possible_attr in self._context_doc:
                if possible_attr.dep_ == d_dep and self._context_doc[count] in possible_attr.head.children:
                    if not possible_attr.text in self._formula_tokens:
                        descriptor_dict["text"] = self._get_noun_chunk(possible_attr.text, attr_count)
                        descriptor_dict["dep"] = possible_attr.dep_ 
                        descriptor_dict["pos"] = possible_attr.pos_
                        descriptor_dict["rule"] = "two"
                        self._textual_type_descriptors.append(descriptor_dict)
                attr_count += 1
        else:
            ...

        

    def _get_pos_in_window(self, pos_tag: str, interval: str) -> dict:

        descriptor_dict = {}
        if interval == "left":
            left = self._window_size 
            right = 1
        elif interval == "right":
            right = self._window_size
            left = 1
        else:
            right = self._window_size 
            left = self._window_size

        count = self._context_tokens.index(self._sel_formula_token)
        for i in range(count-left, count+right, 1):
            if i == count or i < 0:
                continue
            sel_token = self._context_doc[i] 
            if sel_token.pos_ == pos_tag and not sel_token.text in self._formula_tokens:
                descriptor_dict = {}
                n_text, n_dep = self._get_noun_chunk(sel_token.text, sel_token.dep_, i)
                descriptor_dict["text"] = n_text
                descriptor_dict["dep"] = n_dep
                descriptor_dict["pos"] = sel_token.pos_
                break
            
        return descriptor_dict
    

    def _get_noun_chunk(self, noun_text, noun_dep, noun_idx):
        for chunk in self._context_doc.noun_chunks:
            if noun_text in chunk.text:
                return chunk.text, chunk.root.dep_ 
        return noun_text, noun_dep

    def print_context(self):

        print("----------------------------------------------------------------------------------------------------")
        print("formula: " + str(self._formula_dict[self._sel_formula_token]))
        print("textual descriptors: ")
        for tex_d in self._textual_type_descriptors:
            print(tex_d)
        for tok in self._context_doc:
            print("\t" + "sel_token: " + str(tok.text) + ": " + str(tok.pos_) + ": " + str(tok.dep_))
        print("MATH-TYPE (context): ", str(self.get_math_type()))
        
    def get_type_descriptors(self) -> dict:
        return list(self._textual_type_descriptors)

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