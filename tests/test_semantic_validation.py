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

def test_undefined_minor_in_rule() :
    pos_str = """
    @MEDFORD{
        Version: version,
        requires Version == "1.0" => Cookie
    }
    """
    neg_str = """
    @MEDFORD{
        Version: version,
        Cookie?: str,
        requires Version == "1.0" => Cookie
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

def test_if_minor_then_same_minor_dne() :
    pos_str = """
    @MEDFORD{
        Version: version,
        Cookie?: str,
        requires Version == "1.0" => !Version
    }
    """
    neg_str = """
    @MEDFORD{
        Version: version,
        Cookie?: str,
        requires Version == "1.0" => !Cookie
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

def test_if_minor_then_req_e() :
    pos_str = """
    @MEDFORD{
        Version: version,
        Cookie!: str,
        requires Version == "1.0" => Cookie
    }
    """
    neg_str = """
    @MEDFORD{
        Version: version,
        Cookie?: str,
        requires Version == "1.0" => Cookie
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

def test_if_minor_then_req_dne() :
    pos_str = """
    @MEDFORD{
        Version: version,
        Cookie!: str,
        requires Version == "1.0" => !Cookie
    }
    """
    neg_str = """
    @MEDFORD{
        Version: version,
        Cookie?: str,
        requires Version == "1.0" => !Cookie
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