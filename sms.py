# Import necessary modules from PyQt6 and other libraries
from PyQt6.QtWidgets import (
    QApplication, QLabel, QWidget, QGridLayout, QLineEdit,
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem,
    QDialog, QVBoxLayout, QComboBox, QToolBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


# Define the main application window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 400)
        self.setWindowIcon(QIcon("icons/time.png"))

        # Create menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        self.menuBar().setStyleSheet(
            "color: black; font-weight: 700; background-color: lightgreen")

        # Add actions to the File, Edit And About menus
        add_student_action = QAction(
            QIcon("icons/add.png"), "Add Student", self)
        file_menu_item.addAction(add_student_action)
        file_menu_item.triggered.connect(self.insert)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        # Create a table widget to display database data
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ("ID", "Name", "Course", "Mobile Number"))
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStyleSheet("font-weight: bold;")
        self.setCentralWidget(self.table)

        # Create and configure the toolbar
        toolbar = QToolBar()
        toolbar.setStyleSheet("background-color: #EBDBF6")
        toolbar.setMovable(True)
        toolbar.setFixedSize(200, 40)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

    
    def load_data(self):
        """Fetches data from the database and displays it in the table."""
        connection = sqlite3.connect("students.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number,
                                   QTableWidgetItem(str(data)))
        connection.close()

    # instantiate insert dialog object from the class we made.
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()


# Adding search dialog window
class SearchDialog(QDialog):
    def __init__(self):

        super().__init__()
        # Set window title and size
        self.setWindowTitle("Search For Student")
        self.setFixedWidth(500)
        self.setFixedHeight(300)

        # Create layout and input widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("name")
        self.student_name.setStyleSheet(
            "border-radius: 8px; font-size: 18px; padding: 10px; background-color: #39897E; color: white")
        layout.addWidget(self.student_name)

        # Creating button
        button = QPushButton("Search")
        button.setStyleSheet(
            "background-color: #39897E; color: white; font-size: 20px; border-radius: 20px; padding: 10px")
        button.clicked.connect(self.search)
        button.clicked.connect(self.close)
        layout.addWidget(button)

        self.setLayout(layout)

    # Searching in database by name
    def search(self):
        """Searches the database for students with the given name.
        Args:
            self: the object
            self.student_name: The name to search for.
        """

        name = self.student_name.text()
        connection = sqlite3.connect("students.db")
        cursor = connection.cursor()
        result = cursor.execute(
            "SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(
            name, Qt.MatchFlag.MatchFixedString)

        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


class InsertDialog(QDialog):
    """
    class for taking input from user and insert it into database table.
    this new window will be triggered when we navigate to file --> Add Student in menu bar
    or by plus icon.
    """

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
        self.student_name.setStyleSheet(
            "border-radius: 8px; font-size: 18px; padding: 10px; background-color: #39897E; color: white")
        layout.addWidget(self.student_name)

        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']
        self.course_name.addItems(courses)
        self.course_name.setStyleSheet(
            "border-radius: 8px; font-size: 18px; padding: 10px; background-color: #39897E; color: white")

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile Number")
        self.mobile.setStyleSheet(
            "border-radius: 8px; font-size: 18px; padding: 10px; background-color: #39897E; color: white")

        # Add submit button
        button = QPushButton("Register Student")
        button.setStyleSheet(
            "background-color: #39897E; color: white; font-size: 20px; border-radius: 20px; padding: 10px")
        button.clicked.connect(self.register_student)
        button.clicked.connect(self.close)

        layout.addWidget(self.course_name)
        layout.addWidget(self.mobile)
        layout.addWidget(button)

        self.setLayout(layout)

    # connect to database to insert data
    def register_student(self):
        """
        Inserts a new student record into the database.
        Args : self.->
            name: The student's name.
            course: The student's course.
            mobile: The student's mobile number.
        """
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

        main_window.load_data()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
