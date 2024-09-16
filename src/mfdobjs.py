from typing import List, Union
from lark import Transformer

class MinorToken :
    minor_token: str
    is_required: bool
    minor_type: str

    def __init__(self, minor_token: str, is_required: bool, minor_type: str) :
        self.minor_token = minor_token
        self.is_required = is_required
        self.minor_type = minor_type

    def __str__(self) -> str:
        res = "Minor: {minor_token} ({req}) of type {type}".format(minor_token = self.minor_token, req = "req" if self.is_required else "opt", type = self.minor_type)
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
        
    def __str__(self) -> str :
        res = "Rule : {m1} {test} {cont} implies {m2} {res}.".format(m1 = self.first_minor, 
                                                                    test = self.test_type,
                                                                    cont = self.test_content,
                                                                    m2 = self.second_minor,
                                                                    res = "exists" if self.second_exists else "does not exist")
        return res

class MajorToken :
    major_token: str
    is_required: bool
    minor_tokens: List[MinorToken]
    rules: List[Rule]

    def __init__(self, major_token: str, is_required: bool, content: Union[MinorToken, List[Union[MinorToken, Rule]]]) :
        self.major_token = major_token
        self.is_required = is_required
        
        if isinstance(content,MinorToken) :
            self.minor_tokens = [content]
            self.rules = []
        elif isinstance(content, Rule) :
            raise TypeError("Cannot have Rules without MinorTokens in a MajorToken.")
        elif isinstance(content, List) :
            self.minor_tokens = []
            self.rules = []
            for c in content :
                if isinstance(c,MinorToken) :
                    self.minor_tokens.append(c)
                elif isinstance(c,Rule) :
                    self.rules.append(c)
                else :
                    raise TypeError("Unexpected type passed as content to MajorToken in a List.")
        elif content is None :
            self.minor_tokens = []
            self.rules = []
        else :
            raise TypeError("Unexpected type passed to MajorToken.")
                
    def __str__(self) -> str:
        res = "Major: {major_token} ({req})".format(major_token = self.major_token, req = "req" if self.is_required else "opt")
        if len(self.minor_tokens) > 0 or len(self.rules) > 0 :
            for m in self.minor_tokens :
                res += "\n       " + m.__str__()
            for r in self.rules :
                res += "\n       " + r.__str__()
        return res

class TreeToSchemaObjs(Transformer):
    WORD = str

    def REQ(self, value) :
        if value == "!" :
            return True
        else :
            return False
    
    def minor_token_def(self, items) :
        name, required, minortype = items
        return MinorToken(name, required, minortype)
    
    def major_token_def(self, items) :
        #name, required, [minor_tokens/rules](opt)
        name, required, *content = items
        return MajorToken(name, required, content)
    
    def token_rule(self, items) :
        first_minor, test_type, test_content, res_type, second_minor = items
        return Rule(first_minor, test_type, test_content, res_type, second_minor)