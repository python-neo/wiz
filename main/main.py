from argparse import ArgumentParser, REMAINDER

if __name__ == "__main__" :
    argparser = ArgumentParser ()
    argparser.add_argument ("command", nargs = REMAINDER)
    args = argparser.parse_args ()
    print (args)