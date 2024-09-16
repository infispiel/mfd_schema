from lark import Lark
from src.mfdobjs import TreeToSchemaObjs
from src.typedefs import Validators

def main():
    schema_parser = Lark(open("src/grammar.lark"), start="tokens", 
                         maybe_placeholders=True,
                         propagate_positions=True)

    ex_1 = ""
    with open('examples/version_ex') as file :
        ex_1 = file.read()

    t = schema_parser.parse(ex_1)
    #print( t.pretty())
    schemaobjs = TreeToSchemaObjs().transform(t)
    print(schemaobjs)

    ex_2 = ""
    with open('examples/contributor_ex') as file :
        ex_2 = file.read()

    t = schema_parser.parse(ex_2)
    #print( t.pretty() )
    schemaobjs = TreeToSchemaObjs().transform(t)
    print(schemaobjs)

    ex_3 = ""
    with open('examples/multiple_ex') as file :
        ex_3 = file.read()

    t = schema_parser.parse(ex_3)
    #print( t.pretty() )
    schemaobjs = TreeToSchemaObjs().transform(t)
    schemaobjs.validate_semantics()
    print(schemaobjs)

if __name__ == "__main__":
    main()
