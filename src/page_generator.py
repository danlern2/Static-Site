from markdown_to_nodes import markdown_to_blocks
from htmlnode import mk_doc_to_html_node
import os


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        full_doc = file.read()
    with open(template_path) as file:
        template = file.read()
    html_doc: str | None = mk_doc_to_html_node(full_doc).to_html()
    title = extract_title(full_doc)
    step1 = template.replace("{{ Title }}", title)
    final = step1.replace("{{ Content }}", html_doc)  # type: ignore
    if os.path.exists(os.path.dirname(dest_path)) is False:
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as file:
        file.write(final)
    return


def extract_title(markdown_doc: str) -> str:
    for block in markdown_to_blocks(markdown_doc)[:3]:
        if block.startswith("# "):
            return block
    raise Exception("Submitted document requires an h1 header")


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    if os.path.isfile(dir_path_content) is True and os.path.split(dir_path_content)[
        1
    ].endswith(".md"):
        new_html = dest_dir_path[:-2] + "html"
        return generate_page(dir_path_content, template_path, new_html)
    elif os.path.isdir(dir_path_content):
        for item in os.listdir(dir_path_content):
            new_path = os.path.join(dir_path_content, item)
            new_dest = os.path.join(dest_dir_path, item)
            generate_pages_recursive(new_path, template_path, new_dest)
    return
