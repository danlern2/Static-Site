import os
# import pathlib
import shutil

from copystatic2 import directory_copier
from page_generator2 import generate_pages_recursive


# def main():
#     content = pathlib.Path(
#         os.path.abspath(os.path.expanduser(os.path.expandvars("static_site/content")))
#     )
#     static = pathlib.Path(
#         os.path.abspath(os.path.expanduser(os.path.expandvars("static_site/static")))
#     )
#     template = pathlib.Path(
#         os.path.abspath(os.path.expanduser(os.path.expandvars("static_site/template.html")))
#     )
#     dest_path = pathlib.Path(
#         os.path.abspath(os.path.expanduser(os.path.expandvars("static_site/public")))
#     )
#     print(f"")
#     print(f"Setting up directory at {dest_path}")
#     if os.path.exists(dest_path):
#         print("Removing old files")
#         shutil.rmtree(dest_path)
#         print("Creating files:")
#     directory_copier(static, dest_path)  # type: ignore
#     generate_pages_recursive(content, template, dest_path) # type: ignore
    

# main()

def main():
    # __file__ gives us the absolute path to this `main2.py` file.
    # Now.. retrieve the path to the directory containing `main2.py`.
    src_directory_path = os.path.dirname(__file__)
    # After that.. retrieve the parent directory path of
    # `src_2_electric_danaloo` which is your project root path.
    project_root_path = os.path.dirname(src_directory_path)
    # Then wherever you execute this `main2.py` file you'd end up with the same
    # path to your project root that has all the stuff you expect like
    # contnet/static/template.html/public.
    content = os.path.join(project_root_path, "content")
    static = os.path.join(project_root_path, "static")
    template = os.path.join(project_root_path, "template.html")
    dest_path = os.path.join(project_root_path, "public")
    print(f"Setting up directory at {dest_path}")
    if os.path.exists(dest_path):
        print("Removing old files")
        shutil.rmtree(dest_path)
        print("Creating files:")
    directory_copier(static, dest_path)  # type: ignore
    generate_pages_recursive(content, template, dest_path)  # type: ignore

main()