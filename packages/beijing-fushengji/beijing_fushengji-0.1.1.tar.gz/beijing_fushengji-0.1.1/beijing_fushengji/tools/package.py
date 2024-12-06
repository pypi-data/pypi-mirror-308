import subprocess
from pathlib import Path
import sys
import shutil  # noqa: F401
import contextlib

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


from tools.compile_all import main as compile_ui
from tools.translate import generate as generate_ts, compile as compile_ts

import platform

PYINSTALLER = ".venv/Scripts/pyinstaller.exe" if platform.system() != "Linux" else "venv/bin/pyinstaller"

def run_pyinstaller():
    with cd(str(CURRENT.parent)):
        generate_ts()
        compile_ts()
        compile_ui()
        subprocess.run(f"{PYINSTALLER} entry.py.spec".split(), check=True)


CURRENT = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT.parent))

if __name__ == "__main__":
    run_pyinstaller()
    # with cd(str(CURRENT.parent)):
    #     shutil.copy("res/MiSans-Regular.ttf", "dist")
    # subprocess.run(f"explorer {str(CURRENT.parent.joinpath('dist'))}".split(), check=False)
