from lark import Lark
grammar = "src/grammar.lark"
opts = {"start": "value",
        "maybe_placeholders": True,
        "propagate_positions": True}

def test_no_minor_tokens() :
    ex_str = "@Major{}"
    schema_parser = Lark(open(grammar), **opts)
    schema_parser.parse(ex_str)
