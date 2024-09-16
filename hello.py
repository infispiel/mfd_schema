from lark import Lark

def main():
    schema_parser = Lark(open("src/grammar.lark"), start="value", 
                         maybe_placeholders=True,
                         propagate_positions=True)

    ex_1 = ""
    with open('examples/version_ex') as file :
        ex_1 = file.read()

    t = schema_parser.parse(ex_1)
    print( t.pretty())

    ex_2 = ""
    with open('examples/contributor_ex') as file :
        ex_2 = file.read()

    t = schema_parser.parse(ex_2)
    print( t.pretty() )


if __name__ == "__main__":
    main()
