import pytest
from lark import Lark
from src.mfdobjs import TreeToSchemaObjs

grammar = "src/grammar.lark"
opts = {"start": "tokens",
        "maybe_placeholders": True,
        "propagate_positions": True}

def test_repeated_major_defs() :
    pos_str = """
    @MEDFORD!{
    }
    @MEDFORD!{
    }
    """

    neg_str = """
    @MEDFORD!{
    }
    @MEDFORDTWO!{
    }
    """

    schema_parser = Lark(open(grammar), **opts)
    pos_tree = schema_parser.parse(pos_str)
    neg_tree = schema_parser.parse(neg_str)

    pos_schem = TreeToSchemaObjs().transform(pos_tree)
    neg_schem = TreeToSchemaObjs().transform(neg_tree)

    with pytest.raises(ValueError) as e_info :
        pos_schem.validate_semantics()
    neg_schem.validate_semantics()