import argparse

_parser = argparse.ArgumentParser(
    description="Kuickly Deploy single container docker applications."
    )

_parser.add_argument(
    'mode', type=str,
    help="Whether to spin up or spin down the container. \
    Valid arguments are 'up' and 'down'"
    )

_parser.add_argument(
    'image', type=str, nargs="?",
    help="The image to be deployed."
    )

_parser.add_argument(
    'name', type=str,
    help="The final container's name. \
    Take care when updating a deployed container that you provide the \
    same name otherwise the old container will not be spinned down."
    )
_parser.add_argument(
    '-v', '--volumes', type=str,
    help="Volumes"
    )

_parser.add_argument(
    '-n', '--network', type=str,
    help="Networks to connect the container to."
    )

_parser.add_argument(
    '-p', '--ports', type=str,
    help="Ports to publish."
    )

_parser.add_argument(
    '-e', '--env', type=str,
    help="Environment Variables in the form of 'VAR=somevalue'. \
    Separated with spaces."
    )

_parser.add_argument(
    '--restart', type=str,
    help="Restart Policy. Only 'on-failure' and 'always' are supported."
    )

_parser.add_argument(
    '-d', '--debug', action="store_true",
    help="Debug mode."
    )

_parser.add_argument(
    '--pull', action="store_true",
    help="Always pull the latest image."
    )

_parser.add_argument(
    '-c', '--command', type=str,
    help="Run the specified command in the container."
    )

parser = _parser.parse_args()
