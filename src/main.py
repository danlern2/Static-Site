from textnode import *
from htmlnode import *
from markdown_to_nodes import *
import os
import shutil

def directory_copier(dir_filepath_to_copy, new_dir_target):
    head_tail = os.path.split(new_dir_target)
    log = [head_tail[0]]
    if os.path.exists(dir_filepath_to_copy) == False:
        raise Exception("Not a valid filepath")
    if os.path.exists(new_dir_target) == False and os.path.isfile(dir_filepath_to_copy) == False:
        os.mkdir(new_dir_target)
    if os.path.isfile(dir_filepath_to_copy) == True:
            shutil.copy(dir_filepath_to_copy, new_dir_target)
            log.append(head_tail[1])
            return log
    for item in os.listdir(dir_filepath_to_copy):
        dir_path_to_copy = os.path.join(dir_filepath_to_copy, item)
        target_path = os.path.join(new_dir_target, item)
        log.append(directory_copier(dir_path_to_copy, target_path))
    print(log)
    return log
    


def main():
    copy = "/home/danlern2/bootdevworkspace/static_site/TESTDIRECTORY"
    target = "/home/danlern2/bootdevworkspace/static_site/public/TESTFOLDER/"
    if os.path.exists(target):
        shutil.rmtree(target)
    directory_copier(copy, target)
    # print()
main()
