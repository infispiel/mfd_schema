from typing import Dict, List, Tuple, Union
from lark import Transformer

class MinorDefinition :
    minor_definition: str
    is_required: bool
    minor_type: str

    def __init__(self, minor_definition: str, is_required: bool, minor_type: str) :
        self.minor_definition = minor_definition
        self.is_required = is_required
        self.minor_type = minor_type

    def validate_semantics(self) -> None :
        # TODO : is this needed?
        return

    def __str__(self) -> str:
        res = "Minor: {minor_def} ({req}) of type {type}".format(minor_def = self.minor_definition, req = "req" if self.is_required else "opt", type = self.minor_type)
        return res

class Rule:
    # TODO: make more powerful.
    #   test_type -> an Enum
    #   second_exists -> will need to adjust if we allow for rules to say more than \e or \dne
    first_minor: str
    test_type: str
    test_content: str
    second_exists: bool
    second_minor: str

    def __init__(self, first_minor, test_type, test_content, res_type, second_minor) :
        self.first_minor = first_minor
        self.test_type = test_type
        self.test_content = test_content
        self.res_type = res_type
        self.second_minor = second_minor

        if res_type == "!" :
            self.second_exists = False
        elif res_type is None :
            self.second_exists = True
        else :
            raise ValueError("Unexpected value passed as result type to Rule.")
    
    def get_minor_tokens(self) -> Tuple[str, str] :
        return (self.first_minor, self.second_minor)
    
    def validate_semantics(self) -> None :
        # check for logical fallicies :(

        if not self.second_exists : # "if result is Does Not Exist") :
            if self.first_minor == self.second_minor :
                raise ValueError("Cannot require that a token does not exist if the token exists.")
        return
        
    def __str__(self) -> str :
        res = "Rule : {m1} {test} {cont} implies {m2} {res}.".format(m1 = self.first_minor, 
                                                                    test = self.test_type,
                                                                    cont = self.test_content,
                                                                    m2 = self.second_minor,
                                                                    res = "exists" if self.second_exists else "does not exist")
        return res

class MajorDefinition :
    major_def: str
    is_required: bool
    minor_defs: List[MinorDefinition]
    rules: List[Rule]

    def __init__(self, major_def: str, is_required: bool, content: Union[MinorDefinition, List[Union[MinorDefinition, Rule]]]) :
        self.major_def = major_def
        self.is_required = is_required
        
        if isinstance(content,MinorDefinition) :
            self.minor_defs = [content]
            self.rules = []
        elif isinstance(content, Rule) :
            raise TypeError("Cannot have Rules without MinorDefinition in a MajorDefinition.")
        elif isinstance(content, List) :
            self.minor_defs = []
            self.rules = []
            for c in content :
                if isinstance(c,MinorDefinition) :
                    self.minor_defs.append(c)
                elif isinstance(c,Rule) :
                    self.rules.append(c)
                elif c is None :
                    break
                else :
                    raise TypeError("Unexpected type passed as content to MajorDefinition in a List.")
        elif content is None :
            self.minor_defs = []
            self.rules = []
        else :
            raise TypeError("Unexpected type passed to MajorDefinition.")

    def _defined_minor_tokens(self) -> List[str] :
        defined_minors: List[str] = []
        for minor in self.minor_defs :
            defined_minors.append(minor.minor_definition)

        return defined_minors
    
    def _referenced_minor_tokens(self) -> List[str] :
        referenced_minors: List[str] = []
        for r in self.rules :
            referenced_minors.extend(r.get_minor_tokens())
        
        referenced_minors = list(set(referenced_minors)) # remove dupes
        return referenced_minors

    def validate_semantics(self) -> None :
        # Ensure all rules have all minor tokens present in current major
        if not set(self._referenced_minor_tokens()) <= set(self._defined_minor_tokens()) :
            raise ValueError("Not all referenced minor tokens have been defined.")
            # TODO : find missing minor tokens.
        
        for r in self.rules :
            r.validate_semantics()
        
        for m in self.minor_defs :
            m.validate_semantics()

        return
                
    def __str__(self) -> str:
        res = "Major: {major_token} ({req})".format(major_token = self.major_def, req = "req" if self.is_required else "opt")
        if len(self.minor_defs) > 0 or len(self.rules) > 0 :
            for m in self.minor_defs :
                res += "\n       " + m.__str__()
            for r in self.rules :
                res += "\n       " + r.__str__()
        return res

class SchemaImport :
    # TODO : make more functional
    #   e.g. defined major tokens
    major_defs: List[MajorDefinition]
    def __init__(self, content) :
        self.major_defs = content

    def __str__(self) -> str :
        res = "Schema Import: "
        for m in self.major_defs: 
            res += "\n       "
            res += "       ".join(m.__str__().splitlines(True))
        return res
    
    def validate_semantics(self) -> None :
        # Ensure no repeated major tokens
        major_tokens = self.get_defined_major_tokens()
        if len(major_tokens) != len(list(set(major_tokens))) :
            raise ValueError("Duplicated major definitions.")

        # tell major definition to validate themselves
        for major in self.major_defs :
            major.validate_semantics()

        return

    def get_defined_major_tokens(self) -> List[str] :
        defined_major_tokens: List[str] = []
        for c in self.major_defs: 
            defined_major_tokens.append(c.major_def)

        return defined_major_tokens
    
    def get_defined_major_minor_pairs(self) -> List[Tuple[str, str]] :
        defined_pairs: List[Tuple[str, str,]] = []
        for c in self.major_defs :
            major = c.major_def
            for minor in c.minor_defs :
                defined_pairs.append((major, minor))

        return defined_pairs

    def get_dict_major_minor(self) -> Dict[str, List[str]] :
        major_minor_dict: Dict[str, List[str]] = {}
        for c in self.major_defs :
            major:str = c.major_def
            minors: List[str] = []
            for minor in c.minor_defs :
                minors.append(minor)
            major_minor_dict[major] = minors
        
        return major_minor_dict



class TreeToSchemaObjs(Transformer):
    WORD = str

    def REQ(self, value) :
        if value == "!" :
            return True
        else :
            return False
    
    def minor_token_def(self, items) :
        name, required, minortype = items
        return MinorDefinition(name, required, minortype)
    
    def major_token_def(self, items) :
        #name, required, [minor_tokens/rules](opt)
        name, required, *content = items
        return MajorDefinition(name, required, content)
    
    def token_rule(self, items) :
        first_minor, test_type, test_content, res_type, second_minor = items
        return Rule(first_minor, test_type, test_content, res_type, second_minor)
    
    def tokens(self, items) :
        return SchemaImport(items)