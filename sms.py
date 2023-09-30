# Import necessary modules from PyQt6 and other libraries
from PyQt6.QtWidgets import (
    QApplication, QLabel, QWidget, QGridLayout, QLineEdit,
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem,
    QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


# Establish connection
class DatabaseConnection:
    def __init__(self, database_file="students.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection


# Define the main application window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 400)
        self.setWindowIcon(QIcon("icons/time.png"))
        self.setStyleSheet("background-color: #86A3BE")

        # Create menu items
        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Add style to the menu
        self.menuBar().setStyleSheet(
            "color: white; font-weight: 700; background-color: #00BFA5; font-size: 14px; padding: 10px;")

        # Adding actions to the File, Edit And About menus
        # Add student action
        add_student_action = QAction(
            QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)

        # Search action
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)

        # about action
        about_action = QAction(QIcon("icons/about.png"), "About", self)
        about_action.triggered.connect(self.about)

        # Adding all actions to the specified menu
        file_menu_item.addAction(search_action)
        edit_menu_item.addAction(add_student_action)
        help_menu_item.addAction(about_action)

        # Create a table widget to display database data
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ("ID", "Name", "Course", "Mobile Number"))
        self.table.setStyleSheet(
            "font-size: 18px; color: white; font-weight: bold")
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStyleSheet(
            "font-weight: bold; color: darkblue")
        self.setCentralWidget(self.table)

        # Create and configure the toolbar
        toolbar = QToolBar()
        toolbar.setStyleSheet("background-color: #EBDBF6;")
        toolbar.setMovable(True)
        toolbar.setFixedSize(200, 40)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)
        toolbar.addAction(about_action)

        # Create and configure the status bar
        self.statusbar = QStatusBar()
        self.statusbar.setStyleSheet(
            "font-weight: 700; background-color: #00BFA5")
        self.setStatusBar(self.statusbar)

        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.check_for_edit)
        edit_button.setStyleSheet(
            "background-color: #39897E; color: white; font-size: 14px; border-radius: 10px; padding: 10px")

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.check_for_delete)
        delete_button.setStyleSheet(
            "background-color: #39897E; color: white; font-size: 14px; border-radius: 10px; padding: 10px")
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        """Fetches data from the database and displays it in the table."""
        connection = DatabaseConnection().connect()
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number,
                                   QTableWidgetItem(str(data)))
        connection.close()
        self.table.resizeColumnsToContents()

    def warning_message(self, content):
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowIcon(QIcon("icons/warning.png"))
        confirmation_widget.setWindowTitle("Warning")
        confirmation_widget.setText(content)
        confirmation_widget.setStyleSheet(
            "font-size: 20px; background-color: #EBDBF6; color: purple; border: none;")
        confirmation_widget.exec()

    def check_for_edit(self):
        if main_window.table.currentRow() < 0:
            self.warning_message("Please Select a user to edit")
        else:
            self.edit()

    def check_for_delete(self):
        if main_window.table.currentRow() < 0:
            self.warning_message("Please select a user to delete!")
        else:
            self.delete()

    # instantiate object from the classes we made.

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


# Adding about dialog window
class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setStyleSheet(
            "font-size: 20px; background-color: #EBDBF6; color: purple; border: none;")
        self.setWindowIcon(QIcon("icons/about.png"))
        content = """
Student management system that have basic crud functionality 
created by Ahmad Mohamad Naji
Feel free to modify the code."""
        self.setText(content)


# Adding delete dialog window
class DeleteDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete a student")
        self.setWindowIcon(QIcon("icons/delete.png"))

        self.setStyleSheet("background-color: #69897E")

        layout = QGridLayout()

        confirmation = QLabel("Are you sure you want to delete this record?")
        confirmation.setStyleSheet(
            "background-color: #69897E; color: white; font-size: 18px")
        yes = QPushButton("Yes")
        no = QPushButton("No")
        yes.setStyleSheet(
            "background-color: #39897E; color: white; font-size: 14px; border-radius: 6px; padding: 5px")
        no.setStyleSheet(
            "background-color: #39897E; color: white; font-size: 14px; border-radius: 6px; padding: 5px")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)
        yes.clicked.connect(self.delete_record)
        no.clicked.connect(self.accept)

    def delete_record(self):
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setWindowIcon(QIcon("icons/successful.png"))
        confirmation_widget.setText("Student was deleted successfully")
        confirmation_widget.setStyleSheet(
            "font-size: 20px; background-color: #EBDBF6; color: purple; border: none;")
        confirmation_widget.exec()


# Adding edit dialog window
class EditDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Update Student Data")
        self.setWindowIcon(QIcon("icons/update.png"))
        self.setFixedWidth(500)
        self.setFixedHeight(300)
        self.setStyleSheet("background-color: white")

        layout = QVBoxLayout()

        # Get current row (index) in table to extract specific columns
        index = main_window.table.currentRow()

        self.id = main_window.table.item(index, 0).text()
        # Extract name column
        selected_name = main_window.table.item(index, 1).text()
        # Extract course column
        course = main_window.table.item(index, 2).text()
        # Extract mobile number
        mobile = main_window.table.item(index, 3).text()

        # Add student name widget
        self.student_name = QLineEdit(selected_name)
        self.student_name.setPlaceholderText("Name goes here..")
        self.student_name.setStyleSheet(
            "border-radius: 8px; font-size: 18px; padding: 10px; background-color: #39897E; color: white")
        layout.addWidget(self.student_name)

        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course)
        self.course_name.setStyleSheet(
            "border-radius: 8px; font-size: 18px; padding: 10px; background-color: #39897E; color: white")

        # Add mobile widget
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile Number")
        self.mobile.setStyleSheet(
            "border-radius: 8px; font-size: 18px; padding: 10px; background-color: #39897E; color: white")

        # Add an update button
        button = QPushButton("Update")
        button.setStyleSheet(
            "background-color: #39897E; color: white; font-size: 20px; border-radius: 20px; padding: 10px")
        button.clicked.connect(self.edit_record)
        button.clicked.connect(self.close)

        layout.addWidget(self.course_name)
        layout.addWidget(self.mobile)
        layout.addWidget(button)
        self.setLayout(layout)

    def edit_record(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile =  ? WHERE id = ?", (
            self.student_name.text(),
            self.course_name.itemText(self.course_name.currentIndex()),
            self.mobile.text(),
            self.id
        ))

        connection.commit()
        cursor.close()
        connection.close()

        # Refresh the table
        main_window.load_data()


# Adding search dialog window
class SearchDialog(QDialog):
    def __init__(self):

        super().__init__()
        # Set window title and size
        self.setWindowTitle("Search For Student")
        self.setWindowIcon(QIcon("icons/search.png"))
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
        button.clicked.connect(self.search_record)
        button.clicked.connect(self.close)
        layout.addWidget(button)

        self.setLayout(layout)

    # Searching in database by name
    def search_record(self):
        """Searches the database for students with the given name.
        Args:
            self: the object
            self.student_name: The name to search for.
        """

        name = self.student_name.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        result = cursor.execute(
            "SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        if len(rows) == 0:
            MainWindow.warning_message(self, "No student matching the provided name was found in the database.")
        else:
            items = main_window.table.findItems(
                name, Qt.MatchFlag.MatchFixedString)
            for item in items:
                main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()

# Adding insert dialog window
class InsertDialog(QDialog):
    """
    class for taking input from user and insert it into database table.
    this new window will be triggered when we navigate to file --> Add Student in menu bar
    or by plus icon.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setWindowIcon(QIcon("icons/add.png"))
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
        button.clicked.connect(self.insert_record)
        button.clicked.connect(self.close)

        layout.addWidget(self.course_name)
        layout.addWidget(self.mobile)
        layout.addWidget(button)

        self.setLayout(layout)

    # connect to database to insert data
    def insert_record(self):
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
        connection = DatabaseConnection().connect()
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
