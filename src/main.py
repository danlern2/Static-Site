from textnode import *
from htmlnode import *
from markdown_to_nodes import *
import os
import shutil

def directory_copier(dir_filepath_to_copy, new_dir_target, log=[]):
    log = []
    if os.path.exists(new_dir_target) == False:
        os.mkdir(new_dir_target)
    print(dir_filepath_to_copy)
    if os.path.exists(dir_filepath_to_copy) == False:
        raise Exception("Not a valid filepath")
    if os.path.isfile(dir_filepath_to_copy) == True:
            shutil.copy(dir_filepath_to_copy, new_dir_target)
            log.append(new_dir_target)
            return log
    for item in os.listdir(dir_filepath_to_copy):
        print(dir_filepath_to_copy)
        dir_path_to_copy = os.path.join(dir_filepath_to_copy, item)
        target_path = os.path.join(new_dir_target, item)
        os.mkdir(target_path)
        log.append(directory_copier(dir_path_to_copy, target_path, log))
        continue
    print(log)
    return log
    







def main():
    copy = "/home/danlern2/bootdevworkspace/static_site/TESTDIRECTORY"
    target = "/home/danlern2/bootdevworkspace/static_site/public/TESTFOLDER"
    shutil.rmtree(target)
    directory_copier(copy, target)
    # print()
main()
