# : coding: utf-8

import os
import logging
import getpass


class Logger:
    def __init__(self):
        self.className = "ReName"

        self.dir_path = os.path.dirname(os.path.abspath(__file__))+"/.config"
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

        self.set_logger()
        self.user = getpass.getuser()
    
    def set_logger(self):
        self.log = logging.getLogger("ReName")
        self.log.setLevel(logging.DEBUG)

        if len(self.log.handlers) == 0:
            formatter = logging.Formatter('%(levelname)s : %(asctime)s \n%(message)s')
            self.log.setLevel(logging.DEBUG)

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            stream_handler.setLevel(logging.DEBUG)
            self.log.addHandler(stream_handler)

            file_handler = logging.FileHandler(os.path.join(self.dir_path, 'ReName.log'))
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            self.log.addHandler(file_handler)

    def change_log(self, path, find, replace, all_dir, all_file):
        if find and replace and path:
            self.log.info("<USER : {}> [Path : {}] [{} -> {}]  \n[All Folder Inside Folder Checked : {}]  \
                          \n[All Files Inside Folder : {}]" 
                          .format(self.user, path, find, replace, all_dir, all_file, ))
            
    def path_log(self):
        self.log.debug('<USER : {} > Problem : No Path'.format(self.user))
    
    def find_name_log(self):
        self.log.debug('<USER : {} > Problem : No Find Name'.format(self.user))

    def replace_name_log(self):
        self.log.debug('<USER : {} > Problem : No Replace Name'.format(self.user))
        

