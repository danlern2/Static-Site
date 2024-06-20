import os
import pathlib
import shutil

from copystatic import directory_copier
from page_generator import generate_pages_recursive


def main():
    content = pathlib.Path(
        os.path.abspath(os.path.expanduser(os.path.expandvars("content")))
    )
    static = pathlib.Path(
        os.path.abspath(os.path.expanduser(os.path.expandvars("static")))
    )
    template = pathlib.Path(
        os.path.abspath(os.path.expanduser(os.path.expandvars("template.html")))
    )
    dest_path = pathlib.Path(
        os.path.abspath(os.path.expanduser(os.path.expandvars("public")))
    )
    print(f"Setting up directory at {dest_path}")
    if os.path.exists(dest_path):
        print("Removing old files")
        shutil.rmtree(dest_path)
        print("Creating files:")
    directory_copier(static, dest_path)  # type: ignore
    generate_pages_recursive(content, template, dest_path)  # type: ignore


main()
