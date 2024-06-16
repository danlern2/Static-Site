from textnode import *
from htmlnode import *
from markdown_to_nodes import *
import os
import shutil
from copystatic import *
from page_generator import *


def main():
    copy = "/home/danlern2/bootdevworkspace/static_site/static"
    target = "/home/danlern2/bootdevworkspace/static_site/public"
    print(f"Setting up directory at {target}")
    if os.path.exists(target):
        print("Removing old files")
        shutil.rmtree(target)
    directory_copier(copy, target)
    generate_page("/home/danlern2/bootdevworkspace/static_site/content/index.md", "/home/danlern2/bootdevworkspace/static_site/template.html", "/home/danlern2/bootdevworkspace/static_site/public/index.html")
    # print()
main()
