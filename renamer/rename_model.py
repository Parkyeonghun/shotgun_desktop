# : coding: utf-8

import os
import re


class ReName:
    def __init__(self):
        pass

    def replace_name(self, in_path, in_find, in_replace, replace_file, replace_dir):
        for filename in os.listdir(in_path):
            if replace_file == True and replace_dir == False:
                path = os.path.join(in_path, filename)
                if os.path.isfile(path):
                    if re.search(in_find, filename) != None:
                        new_name = re.sub(in_find, in_replace, filename)
                        os.rename(os.path.join(in_path,filename), os.path.join(in_path, new_name))
            elif replace_file == False and replace_dir == True:
                path =os.path.join(in_path, filename)
                if os.path.isdir(path):
                    if re.search(in_find, filename) != None:
                        new_name = re.sub(in_find, in_replace, filename)
                        os.rename(os.path.join(in_path,filename), os.path.join(in_path, new_name))
            else:
                path = in_path
                if re.search(in_find, filename) != None:
                    new_name = re.sub(in_find, in_replace, filename)
                    os.rename(os.path.join(in_path,filename), os.path.join(in_path, new_name))
        print("replace name")


    def replace_all_file(self, in_path, in_find, in_replace, replace_file, replace_dir):
        files = os.listdir(in_path)
        for file in files:
            path = os.path.join(in_path, file)
            if os.path.isdir(path):
                self.replace_name(path, in_find, in_replace, replace_file, replace_dir)
                self.replace_all_file(path, in_find, in_replace, replace_file, replace_dir)



if __name__ == "__main__":
    rn = ReName()
    # rn.replace_name("/home/t003/project/renamer/rename_TEST", "test", "TEST" )
    # rn.replace_folder_name("/home/t003/project/renamer/rename_TEST", "TEST",  "test" , True)
    rn.replace_all_file("/home/t003/project/name_test", "test", "TEST", False, True)
