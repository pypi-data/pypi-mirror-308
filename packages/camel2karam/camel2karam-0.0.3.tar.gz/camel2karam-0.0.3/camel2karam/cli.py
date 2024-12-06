from argparse import ArgumentParser

from __about__ import __version__

def main():
    parser = ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args()
    raise NotImplementedError("The cli is not implemented yet !")
