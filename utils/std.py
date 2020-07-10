import sys

def eprint(str_out):
    """
    Prints the given message to stderr.
    """
    print(str_out, file=sys.stderr)