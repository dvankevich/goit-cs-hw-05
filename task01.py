# original from https://github.com/dvankevich/goit-algo-hw-03/blob/main/task01.py
import sys
import argparse
from aiopath import Path
import aioshutil
import asyncio
import errno


async def check_paths(src_path, dst_path):
    if await src_path.absolute() == await dst_path.absolute():
        raise ValueError(f"{src_path} and {dst_path} are the same directory")

    if dst_path.is_relative_to(src_path):  # synchronous method
        raise ValueError(f"{dst_path} cannot be inside {src_path.absolute()}")


async def validate_source(src_path):
    if not await src_path.exists():
        raise FileNotFoundError(errno.ENOENT, f"{src_path} does not exist")

    if not await src_path.is_dir():
        raise NotADirectoryError(errno.ENOTDIR, f"{src_path} is not a directory")


async def validate_destination(dst_path):
    if await dst_path.exists() and not await dst_path.is_dir():
        raise NotADirectoryError(errno.ENOTDIR, f"{dst_path} is not a directory")

    if await dst_path.exists() and any(await dst_path.iterdir()):
        raise OSError(errno.ENOTEMPTY, f"{dst_path} is not empty")


async def copy_file(src: Path, dst: Path, verbose):
    file_name = src.name
    file_ext = src.suffix[1:]
    dir_name = src.parent
    # create destination path
    dst_dir = dst / file_ext / Path(*dir_name.parts[1:])  # remove source dirname
    # create destination dir if it does not exist
    if await dst_dir.exists():
        if await dst_dir.is_file():
            raise ValueError(f"Error: '{dst_dir}' is a file, not a directory.")
    else:
        await dst_dir.mkdir(parents=True, exist_ok=True)
        if verbose:
            print("create directory", dst_dir, dst_dir.absolute())

    dst_file = dst_dir / file_name

    if verbose:
        print(f"copy {src.absolute()} to {dst_file.absolute()}")

    await aioshutil.copy(src, dst_file)


async def read_folder(srcdir: Path, dstdir: Path, verbose):
    async for path in srcdir.iterdir():
        if await path.is_dir():
            await read_folder(path, dstdir, verbose)
        else:
            await copy_file(path, dstdir, verbose)


async def main():
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
        await check_paths(src_path, dst_path)
        await validate_source(src_path)
        await validate_destination(dst_path)
        await read_folder(src_path, dst_path, verbose)
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
    asyncio.run(main())
