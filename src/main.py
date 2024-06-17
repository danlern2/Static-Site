from textnode import *
from htmlnode import *
from markdown_to_nodes import *
import os
import shutil
from copystatic import *
from page_generator import *


def main():
    copy = "./static_site/static/"
    target = "./static_site/public/"
    print(f"Setting up directory at {target}")
    if os.path.exists(target):
        print("Removing old files")
        shutil.rmtree(target)
    directory_copier(copy, target)
    generate_pages_recursive("./static_site/content/", "./static_site/template.html", "./static_site/public/")
    # generate_page("./static_site/content/", "./static_site/template.html", "./static_site/public/")
    # print()
main()
