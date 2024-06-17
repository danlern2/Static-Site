from markdown_to_nodes import *
from textnode import *
from htmlnode import *
from copystatic import *
import os
import pathlib

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        full_doc = file.read()
    with open(template_path) as file:
        template = file.read()
    step1 = template.replace("{{ Title }}", extract_title(full_doc))
    final = step1.replace("{{ Content }}", mk_doc_to_html_node(full_doc).to_html())
    if os.path.exists(os.path.dirname(dest_path)) == False:
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as file:
        file.write(final)
        print(f"Generated pages.")
    return
    
def extract_title(markdown_doc):
    for block in markdown_to_blocks(markdown_doc)[:3]:
        if block.startswith("# "):
            return block
    raise Exception("Submitted document requires an h1 header")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    pathreal = pathlib.Path(dir_path_content)
    dest_path = pathlib.Path(dest_dir_path)
    template = pathlib.Path(template_path)
    head_tail = os.path.split(pathreal)
    if os.path.isfile(pathreal) and head_tail[1].endswith(".md") == False:
        print("hi")
        return
    elif os.path.isfile(pathreal):
        return generate_page(pathreal, template, dest_path)
    elif os.path.isdir(pathreal):
        for dir in os.listdir(pathreal):
            new_path = os.path.join(pathreal, dir)
            new_dest = os.path.join(dest_path, dir)
            if os.path.isfile(dir_path_content):
                generate_page(new_path, template, new_dest)
                continue
            else:
                generate_pages_recursive(new_path, template, new_dest)
    return 



# generate_page("./static_site/content/index.md", "./static_site/template.html", "./static_site/public/index.html")