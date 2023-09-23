from zipfile import ZipFile, is_zipfile, ZipInfo
from pathlib import Path
from typing import List, Callable, Union, Literal
import subprocess
import shlex
import re

RESOURCES_DIR = Path("./resources")
EXTRACTED_DIR = Path("./extracted")

def extract_file(path: Path) -> None:
    path = path.as_posix()
    if (not is_zipfile(path)):
        raise ValueError("Bad argument passed, expected path to zip file")
    with ZipFile(path, "r") as zip:
        zip.extractall(EXTRACTED_DIR)

def sanitize_extracted_dir() -> None:
    sanitize_dir(EXTRACTED_DIR)

def sanitize_tex(path: Path) -> None:
    if (path.name.endswith("tex")):
        tmp_read = None
        with (path).open("r") as tex_file:
            tmp_read = tex_file.read()
        with (path).open("w") as tex_file:
            r = re.sub(r"Questions\/quiz\s[0-9]+\/", lambda x: x.group(0).replace(" ", "_"), tmp_read)
            r = re.sub(r"quiz[0-9]+\.tex", lambda x: x.group(0).replace(".tex", ""), r)
            tex_file.write(r)


def sanitize_dir(path: Path, depth: int = 0) -> None:
    if (not path.is_dir()):
        return
    sanitized = False
    posix_path = path.as_posix()
    for item in path.iterdir():
        if (item.is_dir()):
            sanitize_dir(item, depth + 1)
        else:
            if (posix_path.find(" ") == -1):
                sanitize_tex(item)
                continue
            sanitized = True
            new_path: Path = Path(posix_path.replace(" ", "_"))
            if (not new_path.exists()):
                new_path.mkdir(511, parents=True)
            item.rename(new_path / item.name)
            sanitize_tex(new_path / item.name)
    if (sanitized and depth > 0):
        path.rmdir()

def clean_extracted_dir() -> None:
    clean_dir(EXTRACTED_DIR)

def clean_dir(path: Path, depth: int = 0) -> None:
    if (not path.is_dir()):
        return
    for item in path.iterdir():
        if (item.is_dir()):
            clean_dir(item, depth + 1)
        else:
            item.unlink()
    if (depth > 0):
        path.rmdir()

is_tex_file: Callable[[Path], bool] = lambda item : item.name.endswith(".tex")

DEPENDENCY_VALUES = {
    "main": -1,
    "others": 0,
    "tex": 1,
}

def get_dependency_type(dependency: Path) -> Literal["others", "tex", "main"]:
    if (dependency.name.endswith(".tex") and not dependency.name.endswith("main.tex")):
        return "tex"
    elif (dependency.name.endswith("main.tex")):
        return "main"
    else:
        return "others"


def linear_dependency_sorter(dependencies: List[Path]) -> List[Path]:
    dependency_value_map = {dependency: DEPENDENCY_VALUES[get_dependency_type(dependency)] for dependency in dependencies}
    return sorted(dependencies, key=lambda dependency: dependency_value_map[dependency])

def build_latex_dependency_chain(path: Path, depth: int = 0) -> str:
    items = [item for item in path.iterdir()]
    if (len(items) == 0 or (depth == 0 and len(list(filter(is_tex_file, items))) == 0)):
        raise ValueError(f"{path} is empty or doesn't have `.tex` files in root")
    dependency_chain: str = ""
    dependencies: List[Path] = []
    for item in items:
        if (item.is_dir()):
            dependency_chain += build_latex_dependency_chain(item, depth + 1)
        else:
            dependencies.append(item)
    dependencies_as_str: str = " ".join([dependency.relative_to(Path("./extracted")).as_posix() for dependency in linear_dependency_sorter(dependencies)])
    if (depth == 0):
        dependency_chain = dependencies_as_str + " " + dependency_chain
    else:
        dependency_chain += dependencies_as_str
    return dependency_chain + (" " if depth > 0 else "")


def process_file(path: Path) -> None:
    if (not path.exists()):
        raise FileNotFoundError("No such file found")
    clean_extracted_dir()
    extract_file(path)
    sanitize_extracted_dir()
    dependency_chain = build_latex_dependency_chain(EXTRACTED_DIR)
    # print(dependency_chain)
    args = shlex.split(f"laton -o main.pdf {dependency_chain}")
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=Path("./extracted"))
    if result.stderr:
        print(result.stderr)
    else:
        print(result.stdout)

if __name__ == "__main__":
    if (not EXTRACTED_DIR.exists()):
        EXTRACTED_DIR.mkdir()
    process_file(RESOURCES_DIR / "latex-copy.zip")