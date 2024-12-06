from optparse import OptionParser
from os import path
from shutil import copytree, ignore_patterns

print(9)


def main():
    usage = "Params: -a/--app app"
    print(usage)
    parser = OptionParser(usage=usage)
    parser.add_option(
        "-a",
        "--app",
        dest="app",
        help="Application name",
        metavar="FILE",
    )
    (options, _) = parser.parse_args()
    if not options.app:
        print(usage)
        exit(1)
    from_dir = path.join(path.dirname(path.abspath(__file__)), "app")
    to_dir = path.join(path.abspath("./"), str(options.app))
    if path.exists(to_dir):
        print(f"Dir `{to_dir}` already exists")
        exit(1)
    copytree(from_dir, to_dir, False, ignore=ignore_patterns("__pycache__"))


if __name__ == "__main__":
    main()
