from curses.ascii import isdigit
import os
import sys
import sqlite3 as sql
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QStackedWidget, QLineEdit, QLabel, QFormLayout, QVBoxLayout, QHBoxLayout, QMessageBox
from attr import field

dir = os.path.dirname(os.path.abspath(__file__))

def get_conn():
    conn = sql.connect(dir + '/example.db')
    return conn

def create_op_db():
    create_op_table_command = """CREATE TABLE IF NOT EXISTS anime_openings (
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    anime TEXT NOT NULL,
    number INTEGER NOT NULL,
    link TEXT NOT NULL,
    UNIQUE(anime, number));"""

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(create_op_table_command)
    conn.commit()
    conn.close()

def create_op_rating_table():
    create_rating_table_command = """CREATE TABLE IF NOT EXISTS op_ratings (
    anime TEXT NOT NULL,
    number INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    UNIQUE(anime, number));"""

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(create_rating_table_command)
    conn.commit()
    conn.close()

def add_op(name, artist, anime, number, link):
    add_op_command = """INSERT INTO anime_openings VALUES (?, ?, ?, ?, ?);"""

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(add_op_command, (name, artist, anime, number, link))
    conn.commit()
    conn.close()

def add_rating(anime, number, rating):
    add_rating_command = """INSERT INTO op_ratings VALUES (?, ?, ?);"""

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(add_rating_command, (anime, number, rating))
    conn.commit()
    conn.close()

def update_op_rating(anime, number, rating):
    update_rating_command = """UPDATE op_ratings SET rating = ? WHERE anime = ? AND number = ?;"""

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(update_rating_command, (rating, anime, number))
    conn.commit()
    conn.close()

def attempt_add_op(input) -> bool:
    name, artist, anime, number, link = input

    if is_form_input_valid(name, artist, number, link):
        add_op(name, artist, anime, number, link)
        return True
    
    return False

def is_form_input_valid(name, artist, number, link) -> bool:
    if isdigit(number):
        return True
    
    return False

def valid_rating(rating):
    return rating <= 10 and rating > 0

# Create gui window

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle('Anime OP Ratings')
        self.setGeometry(0, 0, 700, 500)

        self.setupUI()

    def setupUI(self):
        self.pages = QStackedWidget()

        self.setupMainUI()
        self.setupAddUI()

        self.setCentralWidget(self.pages)

    def setupMainUI(self):
        mainUI = QWidget()

        rate_button = QPushButton(mainUI)
        rate_button.setGeometry(100, 200, 200, 100)
        rate_button.setText('Rate Opening')

        add_button = QPushButton(mainUI)
        add_button.setGeometry(400, 200, 200, 100)
        add_button.setText('Add Opening')
        add_button.clicked.connect(lambda: self.pages.setCurrentIndex(1))

        self.add_page(mainUI)
        self.pages.setCurrentWidget(mainUI)

    def setupAddUI(self):
        add_UI = QWidget()

        v_layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        button_layout = QHBoxLayout()

        # Input Form
        labels = ['OP Title', 'Artist', 'Anime', 'Number', 'Link']
        self.input_fields = []

        for i in range(0, 5):
            input_field = QLineEdit()
            self.form_layout.addRow(QLabel(labels[i]), input_field)
            self.input_fields.append(input_field)

        # Add and Cancel buttons
        add_button = QPushButton()
        add_button.setText('Add')
        add_button.clicked.connect(lambda: self.clear_form_input() if attempt_add_op(self.get_form_input()) else print('Failed to add opening'))

        cancel_button = QPushButton()
        cancel_button.setText('Cancel')
        cancel_button.clicked.connect(lambda: self.pages.setCurrentIndex(0))

        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        v_layout.addLayout(self.form_layout)
        v_layout.addLayout(button_layout)
        add_UI.setLayout(v_layout)

        self.add_page(add_UI)

    def get_form_input(self):
        input = []
        for row in range(0, 5):
            input_field = self.input_fields[row]
            input.append(input_field.text())
            
        return input
    
    def clear_form_input(self):
        for row in range(0, 5):
            input_field = self.input_fields[row]
            input_field.clear()

    def add_page(self, page):
        self.pages.addWidget(page)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())