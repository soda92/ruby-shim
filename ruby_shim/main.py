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


def generate_shims(bin: Path):
    print(bin)
    bats = list(filter(lambda path: path.stem == path.name, bin.glob("*")))
    print(bats)
    for bat in bats:
        generate_shim(bin, bat)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        "-p",
        type=str,
        default="",
        help=r"path for 'bin' dir. default to ruby installation in C:\. change it to related bin dir for rails application.",
    )
    args = parser.parse_args()
    bin_path = ""
    if args.path == "":
        ruby_install = list(Path("C:/").glob("Ruby*"))[0]
        bin_path = ruby_install.joinpath("bin")
    else:
        bin_path = Path(args.path).resolve()
    generate_shims(bin_path)
