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

        self.menuBar().setStyleSheet(
            "color: purple; font-weight: 700; background-color: lightgreen; font-size: 14px; padding: 10px")

        # Add actions to the File, Edit And About menus

        # Add action
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)

        # Search action
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)

        # about action
        about_action = QAction("About", self)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # Adding all actions to the specified menu
        file_menu_item.addAction(search_action)
        edit_menu_item.addAction(add_student_action)
        help_menu_item.addAction(about_action)
      

       
        # Create a table widget to display database data
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ("ID", "Name", "Course", "Mobile Number"))
        self.table.setStyleSheet("font-size: 18px; color: white; font-weight: bold")
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStyleSheet("font-weight: bold; color: darkblue")
        self.setCentralWidget(self.table)
        

        



        # Create and configure the toolbar
        toolbar = QToolBar()
        toolbar.setStyleSheet("background-color: #EBDBF6")
        toolbar.setMovable(True)
        toolbar.setFixedSize(200, 40)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create and configure the status bar
        self.statusbar = QStatusBar()
        self.statusbar.setStyleSheet("font-weight: 700; background-color: lightgreen")
        self.setStatusBar(self.statusbar)

        
        
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)
        edit_button.setStyleSheet("background-color: #39897E; color: white; font-size: 14px; border-radius: 10px; padding: 10px")


        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)
        delete_button.setStyleSheet("background-color: #39897E; color: white; font-size: 14px; border-radius: 10px; padding: 10px")


        children = self.findChildren(QPushButton)
        if children :
            for child in children:
                self.statusbar.removeWidget(child)
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)
        
        

    
        


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
        self.table.resizeColumnsToContents()


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
        


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(500)
        self.setFixedHeight(300)
        self.setStyleSheet("background-color: white")

        layout = QVBoxLayout()

        # Get current row (index) in table to extract specific columns
        index = main_window.table.currentRow()
        print(f"index is {index}")
        # Get index for selected row
        if index != -1:
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
            button.setStyleSheet("background-color: #39897E; color: white; font-size: 20px; border-radius: 20px; padding: 10px")
            button.clicked.connect(self.update_record)
            button.clicked.connect(self.close)

            layout.addWidget(self.course_name)
            layout.addWidget(self.mobile)
            layout.addWidget(button)

            self.setLayout(layout)
        
        else :
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Try Again")
            msg_box.setText("Select a specific record to update...")
            msg_box.setStyleSheet("background-color: gray; color: white; font-size: 24px")
            msg_box.exec()
                   


    def update_record(self):
        connection = sqlite3.connect("students.db")
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
