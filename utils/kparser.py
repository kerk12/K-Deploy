import argparse

_parser = argparse.ArgumentParser(description=\
    "Kuickly Deploy single container docker applications.")

_parser.add_argument('image', type=str, \
    help="The image to be deployed.")
_parser.add_argument('name', type=str, \
    help="The final container's name. Take care when updating a deployed container that you provide the same name otherwise the old container will not be spinned down.")
_parser.add_argument('-v', type=str, \
    help="Volumes")

parser = _parser.parse_args()

