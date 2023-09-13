from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
     QLineEdit, QPushButton, QMainWindow, \
     QTableWidget, QTableWidgetItem, QDialog, \
     QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Student Management System")
        self.setStyleSheet("background-color: white")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        self.menuBar().setStyleSheet("padding: 1px; font-size: 12px; margin-top: 20px; color: black; font-weight: 700; background-color: #EBF0EC")
        

        # Add subitems to the File and Help items
        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert)
        
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile Number"))
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStyleSheet("font-weight: bold; background-color: lightblue;")
        
        self.setCentralWidget(self.table)


    def load_data(self):
        connection = sqlite3.connect("students.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()            
            

        
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


   
# class for taking input from user and insert it into database table
# this new window will be triggered when we choose file add student
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(500)
        self.setFixedHeight(300)
        self.setStyleSheet("background-color: #EBDBF6")
        

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name goes here..")
        self.student_name.setStyleSheet("border-radius: 8px; font-size: 18px; padding: 10px; background-color: #39897E; color: white")
        layout.addWidget(self.student_name)

        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']
        self.course_name.addItems(courses)
        self.course_name.setStyleSheet("border-radius: 8px; font-size: 18px; padding: 10px; background-color: #39897E; color: white")
        layout.addWidget(self.course_name)


        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile Number")
        self.mobile.setStyleSheet("border-radius: 8px; font-size: 18px; padding: 10px; background-color: #39897E; color: white")
        layout.addWidget(self.mobile)

        # Add submit button
        button = QPushButton("Register Student")
        button.clicked.connect(self.register_student)
        button.setStyleSheet("background-color: #39897E; color: white; font-size: 20px; border-radius: 20px; padding: 10px")
        layout.addWidget(button)

        self.setLayout(layout)

    
    def register_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                      (name, course, mobile))
        
        connection.commit()
        cursor.close()
        connection.close()



app = QApplication(sys.argv)
sms = MainWindow()
sms.show()
sms.load_data()
sys.exit(app.exec())    
