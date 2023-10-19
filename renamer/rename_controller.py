# : coding: utf-8

import os

from PySide2.QtWidgets  import *

from rename_view        import MainWindow as ReNameView
from rename_model       import ReName
from logger             import Logger


class Controller(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ReNamer")
        self.setMinimumSize(473, 157)

        self.model = ReName()
        self.view = ReNameView()
        self.logging = Logger()

        self.logging.set_logger()
        self.setCentralWidget(self.view)
        
        self.view.add_btn.clicked.connect(self.add_replace_line)
        self.view.delete_btn.clicked.connect(self.delete_replace_line)
        self.view.reset_btn.clicked.connect(self.reset_replace_line)

        self.view.replace_btn.clicked.connect(self.run_replace_name)
        self.view.space_change_to_underbar_btn.clicked.connect(self.run_replace_space)
        self.view.cancel_btn.clicked.connect(self.run_cancel)

    def run_replace_name(self):
        for i in range(self.view.replace_box_layout.count()):
            self.find = self.view.replace_box_layout.itemAt(i).layout().itemAt(0).widget().text()
            if len(self.find) == 0: 
                self.make_message_box("Warning","find name space is empty")
                self.logging.find_name_log()
                break

            self.replace = self.view.replace_box_layout.itemAt(i).layout().itemAt(2).widget().text()
            if len(self.replace) == 0:
                self.make_message_box("Warning", "repace name space is empty")
                self.logging.replace_name_log()
                break

            self.path = self.view.path_line_edit.text()
            if not os.path.exists(self.path):
                self.make_message_box("Warning", "check your file path")
                self.logging.path_log()
                break

            self.file_check = self.view.all_files_inside_folder_checkbox.isChecked()
            self.dir_check = self.view.folder_name_change_option_checkbox.isChecked()

            if self.file_check or self.dir_check:
                self.run_replace_all_inside(self.path, self.find, self.replace, self.file_check, self.dir_check)
                self.model.replace_name(self.path, self.find, self.replace, self.file_check, self.dir_check)
            else:
                self.model.replace_name(self.path, self.find, self.replace, self.file_check, self.dir_check)
            
            self.logging.change_log(self.path, self.find, self.replace, self.file_check, self.dir_check)

        if self.find and self.replace and os.path.exists(self.path):
            self.make_message_box("RENAME", "Rename Success")

    def run_replace_all_inside(self, path, find, replace, file, dir):
        self.model.replace_all_file(path, find, replace, file, dir)

    def run_replace_space(self):
        self.path = self.view.path_line_edit.text()
        self.find = " "
        self.replace = "_"
        self.file_check = self.view.all_files_inside_folder_checkbox.isChecked()
        self.dir_check = self.view.folder_name_change_option_checkbox.isChecked()

        if not os.path.exists(self.path):
            self.make_message_box("Warning", "check your file path")
            self.logging.path_log()
        else:
            if self.file_check or self.dir_check:
                self.run_replace_all_inside(self.path, self.find, self.replace, self.file_check, self.dir_check)
                self.model.replace_name(self.path, self.find, self.replace, self.file_check, self.dir_check)
            else:
                self.model.replace_name(self.path, self.find, self.replace, self.file_check, self.dir_check)
            self.logging.change_log(self.path, self.find, self.replace, self.file_check, self.dir_check)

    def run_cancel(self):
        for i in range(self.view.replace_box_layout.count()):
            self.find = self.view.replace_box_layout.itemAt(i).layout().itemAt(0).widget().text()
            if len(self.find) == 0: 
                self.make_message_box("Warning","find name space is empty")
                self.logging.find_name_log()
                break
            self.replace = self.view.replace_box_layout.itemAt(i).layout().itemAt(2).widget().text()
            if len(self.replace) == 0:
                self.make_message_box("Warning", "repace name space is empty")
                self.logging.replace_name_log()
                break
            self.path = self.view.path_line_edit.text()
            if not os.path.exists(self.path):
                self.make_message_box("Warning", "check your file path")
                self.logging.path_log()
                break

            if self.file_check or self.dir_check:
                self.run_replace_all_inside(self.path, self.replace, self.find, self.file_check, self.dir_check)
                self.model.replace_name(self.path, self.replace, self.find, self.file_check, self.dir_check)
            else:
                self.model.replace_name(self.path, self.replace, self.find, self.file_check, self.dir_check)
            
            self.logging.change_log(self.path, self.replace, self.find, self.file_check, self.dir_check)

        if self.find and self.replace and os.path.exists(self.path):
            self.make_message_box("RENAME", "Rename Cancel")

    def add_replace_line(self):
        mini_h = self.minimumHeight()
        mini_h += 29
        self.setMinimumHeight(mini_h)
        self.resize(self.minimumSize())

    def delete_replace_line(self):
        self.view.delete_replace_line() 
        if self.view.replace_box_layout.count() > 1:
            mini_h = self.minimumHeight()
            mini_h -= 29
            self.setMinimumHeight(mini_h)
        self.resize(self.minimumSize())

    def reset_replace_line(self):
        self.view.clear_all()
        self.setMinimumHeight(157)
        self.resize(self.minimumSize())

    def make_message_box(self, window_title, text):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(window_title)
        dlg.setText(text)
        dlg.exec_()


if __name__ == "__main__":
    app = QApplication()
    window = Controller()
    window.show()
    app.exec_()
