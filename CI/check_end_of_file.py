import argparse
from curses import LINES
import os
import sys
from subprocess import check_output

def find_files(input_path, exclude_paths):
    command = [
        "find", input_path,
        "-iname", "*.cpp", "-or",
        "-iname", "*.hpp", "-or",
        "-iname", "*.ipp"
    ] + sum([["-not", "-path", exclude] for exclude in exclude_paths], [])

    return str(check_output(command), "utf-8").strip().split("\n")

def check_newline_at_end(file_path, fix):
    with open(file_path) as f:
        lines = f.readlines()

    if not lines[-1].endswith("\n"):
        print(f"Missing newline at end of file: {file_path}")

        if fix:
            with open(file_path, "a") as f:
                f.write("\n")
        else:
            return False

    return True

def check_multiple_newlines(file_path, fix):
    with open(file_path) as f:
        lines = f.readlines()

    if args.reject_multiple_newlines and lines[-1] == "\n":
        print(f"Multiple newlines at end of file: {file_path}")

        if fix:
            while lines[-1] == "\n":
                lines.pop(-1)
            with open(file_path, "w") as f:
                f.write("".join(lines))
        else:
            return False

    return True

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("--exclude", nargs="+")
    p.add_argument("--fix", action="store_true")
    p.add_argument("--reject-multiple-newlines", action="store_true")
    p.add_argument("--github", action="store_true")
    args = p.parse_args()

    files = find_files(args.input, args.exclude)
    failed = []

    for file in files:
        file = os.path.normpath(file)

        if not check_newline_at_end(file, args.fix):
            failed.append(file)
        elif not check_multiple_newlines(file, args.fix):
            failed.append(file)
        
        if args.github:
            print(f"::error file={file},line={len(LINES)},title=End of file check::missing newline")

    if failed:
        print(f"failed for files: {' '.join(failed)}")
        return 1

    print("success")
    return 0

if __name__ == "__main__":
    sys.exit(main())
