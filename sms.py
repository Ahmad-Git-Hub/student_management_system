from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
     QLineEdit, QPushButton, QMainWindow, QTableWidget
from PyQt6.QtGui import QAction
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Student Management System")
        self.setStyleSheet("background-color: #397E89")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        self.menuBar().setStyleSheet("padding: 20px; font-size: 20px; margin-top: 20px; color: black; font-weight: 700; background-color: #EBF0EC")
        

        # Add subitems to the File and Help items
        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile Number"))
        self.table.horizontalHeader().setStyleSheet("font-weight: bold; background-color: lightblue;")
        

        self.setCentralWidget(self.table)
        


def load_data(self):
    self.table.co

app = QApplication(sys.argv)
calc = MainWindow()
calc.show()
sys.exit(app.exec())    