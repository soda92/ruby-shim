import shutil
import argparse
import subprocess
from pathlib import Path

CURRENT = Path(__file__).resolve().parent


def compile_shim():
    from ruby_shim.shim_c import SHIM_C

    shim_c = CURRENT.joinpath("shim.c")
    shim_c.write_text(SHIM_C, encoding="utf-8")
    shim_exe = CURRENT.joinpath("shim.exe")
    subprocess.run(
        ("python", "-m", "ziglang", "cc", str(shim_c), "-o", str(shim_exe)), check=True
    )


def get_shim_path():
    SHIM_PATH = CURRENT.joinpath("shim.exe")
    if not SHIM_PATH.exists():
        compile_shim()
    return SHIM_PATH


def generate_shim(bin: Path, bat: Path):
    shim_path = get_shim_path()
    shim_out = bat.parent.joinpath(bat.stem + ".exe")
    try:
        shutil.copy(shim_path, shim_out)
    except Exception as _e:
        pass

    shim_config = bat.parent.joinpath(bat.stem + ".shim")
    file_path = bin.joinpath(bat.stem)
    shim_config.write_text(
        rf"""path = ruby.exe
args = {file_path}
""",
        encoding="utf-8",
    )


def is_script(file: Path):
    if not file.is_file():
        return False
    if not (file.stem == file.name):
        return False
    content = file.read_text(encoding="utf-8")
    line0 = content.split("\n")[0]
    return "ruby" in line0


def generate_shims(bin: Path):
    print("dest dir: " + str(bin))
    bats = list(filter(is_script, bin.glob("*")))
    print(f"creating shims for {', '.join(map(lambda x:x.stem, bats))}")
    for bat in bats:
        generate_shim(bin, bat)


def clean_shims(bin_path: Path):
    shims = bin_path.glob("*.shim")
    for shim in shims:
        exe = shim.parent.joinpath(shim.stem + ".exe")
        import os

        os.unlink(exe)
        os.unlink(shim)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        "-p",
        type=str,
        default="",
        help=r"path for 'bin' dir. default to ruby installation in C:\. change it to related bin dir for rails application.",
    )
    parser.add_argument(
        "--clean",
        "-c",
        action="store_true",
        default=False,
        help="clean installed shim files",
    )
    args = parser.parse_args()
    bin_path = ""
    if args.path == "":
        ruby_install = list(Path("C:/").glob("Ruby*"))[0]
        bin_path = ruby_install.joinpath("bin")
    else:
        bin_path = Path(args.path).resolve()
    if args.clean:
        clean_shims(bin_path)
    else:
        generate_shims(bin_path)
