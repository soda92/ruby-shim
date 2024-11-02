from pathlib import Path
import shutil
import subprocess

CURRENT = Path(__file__).resolve().parent


def compile_shim():
    from ruby_shim.shim_c import SHIM_C

    shim_c = CURRENT.joinpath("shim.c")
    shim_c.write_text(SHIM_C, encoding="utf-8")
    subprocess.run(("python", "-m", "ziglang", "cc", str(shim_c)), check=True)
    shim_out = CURRENT.joinpath("a.exe")
    shim_exe = CURRENT.joinpath("shim.exe")
    shutil.copy(shim_out, shim_exe)


def get_shim_path():
    SHIM_PATH = CURRENT.joinpath("shim.exe")
    if not SHIM_PATH.exists():
        compile_shim()
    return SHIM_PATH


def generate_shim(bin: Path, bat: Path):
    shim_path = get_shim_path()
    shim_out = bat.parent.joinpath(bat.stem + ".exe")
    shutil.copy(shim_path, shim_out)

    shim_config = bat.parent.joinpath(bat.stem + ".shim")
    shim_config.write_text(
        rf"""path = ruby.exe
args = C:\Ruby33-x64\bin\{bat.stem}
""",
        encoding="utf-8",
    )


def generate_shims(bin: Path, bats: list[Path]):
    print(bats)
    for bat in bats:
        generate_shim(bin, bat)
    pass


def find_ruby():
    installs = list(Path("C:/").glob("Ruby*"))
    print(installs)

    for p in installs:
        bin = p.joinpath("bin")
        bats = list(bin.glob("*.bat"))
        generate_shims(bin, bats)


def main():
    find_ruby()
