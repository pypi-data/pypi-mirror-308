import subprocess
import pathlib
import contextlib
from pathlib import Path
import sys
from compile_all import compile_forms

CURRENT = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT.parent))


@contextlib.contextmanager
def cd(dir: str):
    import os

    cwd = os.getcwd()
    try:
        os.chdir(dir)
        yield
    finally:
        os.chdir(cwd)


PREFIX = ""
if pathlib.Path("venv/bin/python").exists():
    PREFIX += "venv/bin/"
elif pathlib.Path(".venv/Scripts/python.exe").exists():
    PREFIX += ".venv/Scripts/"


def run(command):
    subprocess.run(f"{PREFIX}{command}".split(), check=True)


def get_files(folder: str, ext: str):
    with cd(str(CURRENT.parent)):
        files1 = pathlib.Path(folder).glob(f"*.{ext}")
        files1 = [f"{folder}/{x.name}" for x in files1]
        return files1


def design():
    all_files = []
    all_files.extend(get_files("form", "ui"))

    with cd(str(CURRENT.parent)):
        run(f"pyside6-designer {' '.join(all_files)}")


if __name__ == "__main__":
    design()
    compile_forms()
