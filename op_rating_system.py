import os
import sys
import sqlite3 as sql
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QStackedWidget, QLineEdit, QLabel, QFormLayout, QVBoxLayout, QHBoxLayout

dir = os.path.dirname(os.path.abspath(__file__))

conn = sql.connect(dir + '/example.db')
cursor = conn.cursor()

def close_conn():
    conn.close()

def create_op_db():
    create_op_table_command = """CREATE TABLE IF NOT EXISTS anime_openings (
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    anime TEXT NOT NULL,
    number INTEGER NOT NULL,
    link TEXT NOT NULL,
    UNIQUE(anime, number));"""

    cursor.execute(create_op_table_command)
    conn.commit()

def create_op_rating_table():
    create_rating_table_command = """CREATE TABLE IF NOT EXISTS op_ratings (
    anime TEXT NOT NULL,
    number INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    UNIQUE(anime, number));"""

    cursor.execute(create_rating_table_command)
    conn.commit()

def add_op(name, artist, anime, number, link):
    add_op_command = """INSERT INTO anime_openings VALUES (?, ?, ?, ?, ?);"""

    cursor.execute(add_op_command, (name, artist, anime, number, link))
    conn.commit()

def add_rating(anime, number, rating):
    add_rating_command = """INSERT INTO op_ratings VALUES (?, ?, ?);"""

    cursor.execute(add_rating_command, (anime, number, rating))
    conn.commit()

def update_op_rating(anime, number, rating):
    update_rating_command = """UPDATE op_ratings SET rating = ? WHERE anime = ? AND number = ?;"""

    cursor.execute(update_rating_command, (rating, anime, number))
    conn.commit()

def is_form_input_valid():
    pass

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
        form_layout = QFormLayout()
        button_layout = QHBoxLayout()

        form_layout.addRow(QLabel('OP Title'), QLineEdit())
        form_layout.addRow(QLabel('Artist'), QLineEdit())
        form_layout.addRow(QLabel('Anime'), QLineEdit())
        form_layout.addRow(QLabel('Number'), QLineEdit())
        form_layout.addRow(QLabel('Link'), QLineEdit())

        add_button = QPushButton()
        add_button.setText('Add')

        cancel_button = QPushButton()
        cancel_button.setText('Cancel')
        cancel_button.clicked.connect(lambda: self.pages.setCurrentIndex(0))

        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        v_layout.addLayout(form_layout)
        v_layout.addLayout(button_layout)
        add_UI.setLayout(v_layout)

        self.add_page(add_UI)

    def add_page(self, page):
        self.pages.addWidget(page)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

close_conn()