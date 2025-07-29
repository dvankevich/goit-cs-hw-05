# original from https://github.com/dvankevich/goit-algo-hw-03/blob/main/task01.py
import sys
import argparse
from pathlib import Path
import shutil
import errno


def check_paths(src_path, dst_path):
    if src_path.absolute() == dst_path.absolute():
        raise ValueError(f"{src_path} and {dst_path} are the same directory")

    if dst_path.absolute().is_relative_to(src_path.absolute()):
        raise ValueError(f"{dst_path} cannot be inside {src_path.absolute()}")


def validate_source(src_path):
    if not src_path.exists():
        raise FileNotFoundError(errno.ENOENT, f"{src_path} does not exist")

    if not src_path.is_dir():
        raise NotADirectoryError(errno.ENOTDIR, f"{src_path} is not a directory")


def validate_destination(dst_path):
    if dst_path.exists() and not dst_path.is_dir():
        raise NotADirectoryError(errno.ENOTDIR, f"{dst_path} is not a directory")

    if dst_path.exists() and any(dst_path.iterdir()):
        raise OSError(errno.ENOTEMPTY, f"{dst_path} is not empty")


def copy_file(src: Path, dst: Path, verbose):
    file_name = src.name
    file_ext = src.suffix[1:]
    dir_name = src.parent
    # create destination path
    dst_dir = dst / file_ext / Path(*dir_name.parts[1:])  # remove source dirname
    # create destination dir if is not exist
    if dst_dir.exists():
        if dst_dir.is_file():
            raise ValueError(f"Error: '{dst_dir}' is a file, not a directory.")
    else:
        dst_dir.mkdir(parents=True, exist_ok=True)
        if verbose:
            print("create directory", dst_dir, dst_dir.absolute())

    dst_file = dst_dir / file_name

    if verbose:
        print(f"copy {src.absolute()} to {dst_file.absolute()}")

    shutil.copy(src, dst_file)


def copy_dir(srcdir: Path, dstdir: Path, verbose):
    for path in srcdir.iterdir():
        if path.is_dir():
            copy_dir(path, dstdir, verbose)
        else:
            copy_file(path, dstdir, verbose)


def main():
    parser = argparse.ArgumentParser(description="Recursive file copier.")
    parser.add_argument("srcdir", type=str, help="source dir")
    parser.add_argument(
        "-d",
        "--dstdir",
        type=str,
        default="dist",
        help="destination dir. dist for default",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="enable verbose output"
    )

    parser.epilog = (
        f"Example usage:\n  python {parser.prog} source_dir -d <destination_dir>\n"
    )

    args = parser.parse_args()
    src_path = Path(args.srcdir)
    dst_path = Path(args.dstdir)
    verbose = args.verbose

    try:
        check_paths(src_path, dst_path)
        validate_source(src_path)
        validate_destination(dst_path)
        copy_dir(src_path, dst_path, verbose)
    except ValueError as ve:
        print(ve)
        sys.exit(1)
    except FileNotFoundError as fe:
        print(fe)
        sys.exit(fe.errno)
    except NotADirectoryError as nde:
        print(nde)
        sys.exit(nde.errno)
    except OSError as oe:
        print(oe)
        sys.exit(oe.errno)


if __name__ == "__main__":
    main()
