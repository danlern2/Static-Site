from markdown_to_nodes import *
from textnode import *
from htmlnode import *
from copystatic import *
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        full_doc = file.read()
    with open(template_path) as file:
        template = file.read()
    html_doc = mk_doc_to_html_node(full_doc).to_html()
    title = extract_title(full_doc)
    step1 = template.replace("{{ Title }}", title)
    final = step1.replace("{{ Content }}", html_doc)
    if os.path.exists(os.path.dirname(dest_path)) == False:
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as file:
        file.write(final)
    return
    
def extract_title(markdown_doc):
    for block in markdown_to_blocks(markdown_doc)[:3]:
        if block.startswith("# "):
            return block
    raise Exception("Submitted document requires an h1 header")



generate_page("/home/danlern2/bootdevworkspace/static_site/content/index.md", "/home/danlern2/bootdevworkspace/static_site/template.html", "/home/danlern2/bootdevworkspace/static_site/public/index.html")