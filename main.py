import loc
from pathlib import Path
import argparse


def main():

    parser = argparse.ArgumentParser(description="""
    count the lines of code in a directory or file""")
    parser.add_argument("path", help="Path to file or directory")
    parser.add_argument("-L", "--lang", help="language to count")
    parser.add_argument(
        "-i", "--ignore",
        nargs="+",
        help="files or directorys to ignore")

    args = parser.parse_args()
    p = Path(args.path)
    ignore = []
    if args.ignore:
        ignore = args.ignore
    dir = loc.Dir(p, ignore)
    dir.count_loc()
    print(dir)


main()
