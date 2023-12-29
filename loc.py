from pathlib import Path


class Loc:
    def __init__(self, path: str = "", lang: str = ""):
        self.total = 0
        self.stripped = 0
        match lang:
            case ".py":
                self.lines_of_code_python(path)
            case ".go":
                self.lines_of_code_go(path)

    def __repr__(self):
        stripped: str = str(self.stripped)
        total: str = str(self.total)
        return "|  " + total.ljust(10, " ") + stripped.ljust(10, " ")

    def lines_of_code_python(self, path: str):
        with open(path) as f:
            lines = f.readlines()
            self.total = len(lines)
            i = 0
            while i < len(lines):
                lines[i] = lines[i].lstrip().rstrip()
                if lines[i].startswith("'''"):
                    trim_multiline(lines, i, "'''")
                    continue
                if lines[i].startswith('"""'):
                    trim_multiline(lines, i, '"""')
                    continue
                if lines[i] == "" or lines[i].startswith("#"):
                    lines.pop(i)
                    continue
                i += 1
            self.stripped = len(lines)

    def lines_of_code_go(self, path: str):
        with open(path) as f:
            lines = f.readlines()
            self.total = len(lines)
            i = 0
            while i < len(lines):
                lines[i] = lines[i].lstrip().rstrip()
                if lines[i].startswith("/*"):
                    trim_multiline(lines, i, "*/")
                    continue
                if lines[i] == "" or lines[i].startswith("//"):
                    lines.pop(i)
                    continue
                i += 1
            self.stripped = len(lines)


class Dir:
    def __init__(
            self,
            path: Path,
            ignore: list,
            root: bool = True,
            offset: str = "",
    ):
        self.dir = {}
        self.root = root
        self.__loc = Loc()
        self.path = path
        self.out = offset + path.name
        self.__ignore = ignore

        for path in self.path.iterdir():
            if self.ignore(path.name):
                continue
            if path.is_dir():
                self.dir[path] = Dir(path, ignore, False, offset + "  ")
            elif path.suffix != "":
                self.dir[path] = Txt(offset + "  " + path.name, path.suffix)

    def count_loc(self, path: str = ""):
        for dir in self.dir:
            loc = self.dir[dir].count_loc(dir)
            self.__loc.total += loc.total
            self.__loc.stripped += loc.stripped
        return self.__loc

    def ignore(self, path: str = "") -> bool:
        for p in self.__ignore:
            if p in path:
                return True
        return False

    def get_loc(self):
        return self.__loc

    def __repr__(self):
        out = self.out.ljust(40, " ") + str(self.__loc) + "\n"
        for dir in self.dir:
            out += str(self.dir[dir])
        if self.root:
            out = (
                "".rjust(40, " ") + "| "
                + "total".ljust(10, " ")
                + "stripped".ljust(10, " ")
                + "\n" + out)
        return out


class Txt:
    def __init__(self, path: str, lang: str):
        self.out = path
        self.lang = lang
        self.__loc = Loc()

    def count_loc(self, path: str):
        self.__loc = Loc(path, self.lang)
        return self.__loc

    def get_loc(self):
        return self.__loc

    def __repr__(self):
        return self.out.ljust(40, " ") + str(self.__loc) + "\n"


def trim_multiline(lines: list, i: int, suffix: str):
    while i < len(lines):
        line = lines.pop(i)
        line = line.lstrip(suffix)
        if suffix in line or line == "":
            return
