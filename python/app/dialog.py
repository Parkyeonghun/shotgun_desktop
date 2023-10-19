# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
import os
import sys
import threading

# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog
from .rename_model import ReName
from .logger import Logger

# standard toolkit logger
logger = sgtk.platform.get_logger(__name__)


def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # in order to handle UIs seamlessly, each toolkit engine has methods for launching
    # different types of windows. By using these methods, your windows will be correctly
    # decorated and handled in a consistent fashion by the system.

    # we pass the dialog class to this method and leave the actual construction
    # to be carried out by toolkit.
    app_instance.engine.show_dialog("Re-Namer", app_instance, AppDialog)


class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """

    def __init__(self):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QWidget.__init__(self)

        # now load in the UI that was created in the UI designer
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


        self.model = ReName()
        self.logging = Logger()


        # most of the useful accessors are available through the Application class instance
        # it is often handy to keep a reference to this. You can get it via the following method:
        self._app = sgtk.platform.current_bundle()

        # logging happens via a standard toolkit logger
        logger.info("Launching Re-Namer Application...")

        # via the self._app handle we can for example access:
        # - The engine, via self._app.engine
        # - A Shotgun API instance, via self._app.shotgun
        # - An Sgtk API instance, via self._app.sgtk

        # lastly, set up our very basic UI
        # self.ui.context.setText("Current Context: %s" % self._app.context)
        self.ui.replace_box_layout.setAlignment(QtCore.Qt.AlignTop)
        self.ui.scrollAreaWidgetContents.setLayout(self.ui.replace_box_layout)
        self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)


        self.add_replace_line()

        self.replace_line_list = []
        self.replace_line_counter = 0


        # signal & slot
        self.ui.path_btn.clicked.connect(self.clicked_path_btn)

        self.ui.add_btn.clicked.connect(self.add_replace_line)
        self.ui.delete_btn.clicked.connect(self.delete_replace_line)
        self.ui.reset_btn.clicked.connect(self.clear_all)

        self.ui.replace_btn.clicked.connect(self.run_replace_name)
        self.ui.space_change_to_underbar_btn.clicked.connect(self.run_replace_space)
        self.ui.cancel_btn.clicked.connect(self.run_cancel)

    def clicked_path_btn(self):
        self.file_path = QtGui.QFileDialog.getExistingDirectory(self, ("Open Directory"), "/home/") 
        print("file_path ==", self.file_path)
        self.ui.path_lineEdit.setText(self.file_path )

    def add_replace_line(self):

        self.ui.replace_layout = QtGui.QHBoxLayout()
        self.ui.find_line_edit = QtGui.QLineEdit()
        self.ui.replace_label = QtGui.QLabel("->")
        self.ui.replace_line_edit = QtGui.QLineEdit()


        self.ui.replace_layout.addWidget(self.ui.find_line_edit)
        self.ui.replace_layout.addWidget(self.ui.replace_label)
        self.ui.replace_layout.addWidget(self.ui.replace_line_edit)

        self.ui.replace_box_layout.addLayout(self.ui.replace_layout)




        # mini_h = self.minimumHeight()
        # mini_h += 29
        # self.setMinimumHeight(mini_h)
        # self.resize(self.minimumSize())

        # ui_mini_h = self.ui.minimumHeight()
        # ui_mini_h += 29
        # self.ui.setMinimumHeight(ui_mini_h)
        # self.ui.resize(self.ui.minimumSize())
    
    def delete_replace_line(self):
        if self.ui.replace_box_layout.count() > 1:
            i = self.ui.replace_box_layout.count()-1
            layout = self.ui.replace_box_layout.itemAt(i).layout()
            for i in range(layout.count()):
                layout.itemAt(i).widget().deleteLater()
            layout.deleteLater()

            # mini_h = self.minimumHeight()
            # mini_h -= 29
            # self.setMinimumHeight(mini_h)
            # self.resize(self.minimumSize())



            # ui_mini_h = self.ui.minimumHeight()
            # ui_mini_h -= 29
            # self.ui.setMinimumHeight(ui_mini_h)
            # self.ui.resize(self.ui.minimumSize())


    def clear_all(self):
        self.ui.path_lineEdit.setText("")
        
        for i in range(self.ui.replace_box_layout.count()):
            layout = self.ui.replace_box_layout.itemAt(i).layout()
            layout.deleteLater()
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                widget.deleteLater()
        
        # self.setMinimumHeight(158)
        # self.resize(self.minimumSize())
        self.add_replace_line()

    def run_replace_name(self):
        for i in range(self.ui.replace_box_layout.count()):
            self.find = self.ui.replace_box_layout.itemAt(i).layout().itemAt(0).widget().text()
            if len(self.find) == 0: 
                self.make_message_box("Warning","find name space is empty")
                self.logging.find_name_log()
                break

            self.replace = self.ui.replace_box_layout.itemAt(i).layout().itemAt(2).widget().text()
            if len(self.replace) == 0:
                self.make_message_box("Warning", "repace name space is empty")
                self.logging.replace_name_log()
                break

            self.path = self.ui.path_lineEdit.text()
            if not os.path.exists(self.path):
                self.make_message_box("Warning", "check your file path")
                self.logging.path_log()
                break

            self.file_check = self.ui.all_files_inside_folder_checkbox.isChecked()
            self.dir_check = self.ui.folder_name_change_option_checkbox.isChecked()

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

    def make_message_box(self, window_title, text):
        dlg = QtGui.QMessageBox(self)
        dlg.setWindowTitle(window_title)
        dlg.setText(text)
        dlg.exec_()

    def run_replace_space(self):
        self.path = self.ui.path_lineEdit.text()
        self.find = " "
        self.replace = "_"
        self.file_check = self.ui.all_files_inside_folder_checkbox.isChecked()
        self.dir_check = self.ui.folder_name_change_option_checkbox.isChecked()

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
        for i in range(self.ui.replace_box_layout.count()):
            self.find = self.ui.replace_box_layout.itemAt(i).layout().itemAt(0).widget().text()
            if len(self.find) == 0: 
                self.make_message_box("Warning","find name space is empty")
                self.logging.find_name_log()
                break
            self.replace = self.ui.replace_box_layout.itemAt(i).layout().itemAt(2).widget().text()
            if len(self.replace) == 0:
                self.make_message_box("Warning", "repace name space is empty")
                self.logging.replace_name_log()
                break
            self.path = self.ui.path_lineEdit.text()
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
