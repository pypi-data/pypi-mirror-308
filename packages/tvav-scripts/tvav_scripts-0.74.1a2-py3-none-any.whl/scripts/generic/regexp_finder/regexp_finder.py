import logging
import os
import re

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)


def parse_file_with_regexp(filename_in: str, filename_out: str, pattern: str, mode: str = "wt"):
    with open(filename_in, "rt", encoding="ISO-8859-1") as f:
        file_stream = f.read()
        results = re.findall(pattern, file_stream)

    with open(filename_out, mode=mode) as f:
        for res in results:
            f.write(res + "\n")


def get_input_kwargs():
    dir_in = os.getenv("PATH_DIR_IN")
    regexp = os.getenv("REG_EXP")

    if dir_in[0] != os.sep:
        raise ValueError("Please, provide an absolute path")

    path_dir_in = os.path.join(os.sep, *dir_in.split("/"))
    path_dir_out = os.path.join(os.sep, *dir_in.split("/"), "out")

    if not os.path.isdir(path_dir_in):
        raise FileNotFoundError(f"{path_dir_in} does not exist")

    try:
        re.compile(regexp)
    except re.error:
        raise ValueError("Invalid regular expression")

    logging.info(f"Creating output dir: {path_dir_out}")
    os.makedirs(path_dir_out)

    files = []
    for file in os.listdir(path_dir_in):
        if os.path.isfile(os.path.join(path_dir_in, file)):
            files.append(file)

    if len(files) == 0:
        raise FileNotFoundError(f"No files found under {path_dir_in}")

    return str(path_dir_in), str(path_dir_out), files, regexp


if __name__ == "__main__":
    path_dir_in, path_dir_out, files, regexp = get_input_kwargs()

    for file in files:
        parse_file_with_regexp(
            filename_in=str(os.path.join(path_dir_in, str(file))), filename_out=str(os.path.join(path_dir_out, str(file))), pattern=regexp, mode="wt"
        )
