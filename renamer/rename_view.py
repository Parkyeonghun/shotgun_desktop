# : coding: utf-8

from PySide2.QtWidgets  import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("renamer")  
        self.setMinimumSize(473, 128)
        
        # first line = file_path_ui
        path_layout = QHBoxLayout()

        self.path_lable = QLabel("Path")
        self.path_line_edit = QLineEdit()
        self.path_btn = QPushButton(">>>")

        path_layout.addWidget(self.path_lable)
        path_layout.addWidget(self.path_line_edit)
        path_layout.addWidget(self.path_btn)

        # second line = file_name_replace_ui
        self.add_delete_layout = QHBoxLayout()

        self.add_btn = QPushButton("Add")
        self.delete_btn = QPushButton("Delete")
        self.reset_btn = QPushButton("Reset")

        self.add_delete_layout.addWidget(self.add_btn)
        self.add_delete_layout.addWidget(self.delete_btn)
        self.add_delete_layout.addWidget(self.reset_btn)

        # third line
        self.replace_box_layout = QVBoxLayout()


        # third line = rename_options
        options_layout = QHBoxLayout()


        self.folder_name_change_option_checkbox = QCheckBox("All folders inside folder")
        self.all_files_inside_folder_checkbox = QCheckBox("All files inside folder")

        self.space_change_to_underbar_btn = QPushButton("Space  ->  UnderBar")
        self.replace_btn = QPushButton("Replace")
        self.cancel_btn = QPushButton("Cancel")
        
        check_option_layout = QVBoxLayout()
        check_option_layout.addWidget(self.folder_name_change_option_checkbox)
        check_option_layout.addWidget(self.all_files_inside_folder_checkbox)

        btn_layout = QVBoxLayout()
        replace_cancel_btn_layout = QHBoxLayout()
        replace_cancel_btn_layout.addWidget(self.replace_btn)
        replace_cancel_btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.space_change_to_underbar_btn)
        btn_layout.addLayout(replace_cancel_btn_layout)

        options_layout.addLayout(check_option_layout)
        options_layout.addLayout(btn_layout)
        
        # layout
        self.v_layout = QVBoxLayout()

        self.v_layout.addLayout(path_layout)
        self.v_layout.addLayout(self.add_delete_layout)
        self.v_layout.addLayout(self.replace_box_layout)
        self.v_layout.addLayout(options_layout)
    
        self.setLayout(self.v_layout)

        # signal & slot
        self.path_btn.clicked.connect(self.clicked_path_btn)
        self.folder_name_change_option_checkbox.clicked.connect(self.folder_checked)
        self.all_files_inside_folder_checkbox.clicked.connect(self.inside_folder_checked)
        self.replace_btn.clicked.connect(self.replace_clicked)
        self.cancel_btn.clicked.connect(self.cancel_clicked)
        self.add_btn.clicked.connect(self.add_replace_line )
        self.delete_btn.clicked.connect(self.delete_replace_line)
        self.reset_btn.clicked.connect(self.clear_all)

        self.add_replace_line()

    def clicked_path_btn(self):
        self.file_path = QFileDialog.getExistingDirectory(self, ("Open Directory"), "/home/") 
        print("file_path ==", self.file_path)
        self.path_line_edit.setText(self.file_path )
        
    def clicked_replace_space(self):
        print("change Space bar")

    def folder_checked(self):
        check = self.folder_name_change_option_checkbox.isChecked()
        print("folder checked", check)

    def inside_folder_checked(self):
        check = self.all_files_inside_folder_checkbox.isChecked()
        print("inside folder checked", check)
    
    def replace_clicked(self):
        print("replace")

    def cancel_clicked(self):
        print("cancel")

    def delete_replace_line(self):
        if self.replace_box_layout.count() > 1:
            i = self.replace_box_layout.count()-1
            layout = self.replace_box_layout.itemAt(i).layout()
            for i in range(layout.count()):
                layout.itemAt(i).widget().deleteLater()
            layout.deleteLater()

            mini_h = self.minimumHeight()
            mini_h -= 29
            self.setMinimumHeight(mini_h)
            self.resize(self.minimumSize())

    def add_replace_line(self):
        self.replace_layout = QHBoxLayout()

        self.find_line_edit = QLineEdit()
        self.replace_label = QLabel("->")
        self.replace_line_edit = QLineEdit()

        self.replace_layout.addWidget(self.find_line_edit)
        self.replace_layout.addWidget(self.replace_label)
        self.replace_layout.addWidget(self.replace_line_edit)

        self.replace_box_layout.addLayout(self.replace_layout)

        mini_h = self.minimumHeight()
        mini_h += 29
        self.setMinimumHeight(mini_h)
        self.resize(self.minimumSize())

    def clear_all(self):
        self.path_line_edit.setText("")
        
        for i in range(self.replace_box_layout.count()):
            layout = self.replace_box_layout.itemAt(i).layout()
            layout.deleteLater()
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                widget.deleteLater()
        
        self.setMinimumHeight(128)
        self.resize(self.minimumSize())
        self.add_replace_line()


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec_()
