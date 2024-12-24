import os
import sys
import logging

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDialog)
from PyQt5.QtGui import QPixmap, QIcon, QFontDatabase
from PyQt5.QtCore import Qt, QTimer

import main_window
# Setup logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
current_path = os.getcwd()
print(current_path)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.resize(400, 700)
        font_id = QFontDatabase.addApplicationFont(f'{current_path}\\font\\Roboto-Black.ttf')
        if (font_id != -1):
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setStyleSheet(f"""
                        background-color: #f0f0f0;
                        font-family: '{font_family}';
                        font-size: 14px;
                        color: #333;
                    """)
        else:
            print("Failed to load font.")

        self.setWindowIcon(QIcon(f'{current_path}\\img\\Luxor.ico'))
        self.setStyleSheet("""
            background-color: #fff;
            font-family: Arial, sans-serif;
            font-size: 14px;
        """)  # Setting background color and default font

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Image placement
        pixmap = QPixmap(
            f'{current_path}\\img\\logo.jpg').scaledToWidth(250)
        img_label = QLabel(self)
        img_label.setPixmap(pixmap)
        img_label.setScaledContents(True)
        img_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(img_label)

        # Username and password fields
        username_layout = QVBoxLayout()
        lbl_username = QLabel('Username:', self)
        lbl_username.setStyleSheet("""
            font-size: 16px;
            color: #333;
            margin-bottom: 5px;
        """)
        self.le_username = QLineEdit(self)
        self.le_username.setFixedWidth(250)  # Set specific width
        self.le_username.setStyleSheet("""
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
        """)
        username_layout.addWidget(lbl_username)
        username_layout.addWidget(self.le_username)

        password_layout = QVBoxLayout()
        lbl_password = QLabel('Password:', self)
        lbl_password.setStyleSheet("""
            font-size: 16px;
            color: #333;
            margin-bottom: 5px;
        """)
        self.le_password = QLineEdit(self)
        self.le_password.setFixedWidth(250)  # Set specific width
        self.le_password.setEchoMode(QLineEdit.Password)
        self.le_password.setStyleSheet("""
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
        """)
        password_layout.addWidget(lbl_password)
        password_layout.addWidget(self.le_password)

        layout.addLayout(username_layout)
        layout.addLayout(password_layout)

        # Login button with updated styling
        self.btn_login = QPushButton('Login', self)
        self.btn_login.setFixedWidth(250)  # Set specific width
        self.btn_login.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 16px;
                background-color: #1976D2;
                border: 2px solid #eee;
                color: white;
                border-radius: 10px;
                margin-top: 20px;
                min-width: 150px;
                transition: background-color 0.3s, color 0.3s;
            }
            QPushButton:hover {
                background-color: #1976D9;
                color: white;
            }
        """)
        self.btn_login.clicked.connect(self.animate_login)
        layout.addWidget(self.btn_login)

        # Change Password button
        self.btn_change_password = QPushButton('Change Password', self)
        self.btn_change_password.setFixedWidth(250)  # Set specific width
        self.btn_change_password.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 16px;
                background-color: #1976D2;
                border: 2px solid #eee;
                color: white;
                border-radius: 10px;
                margin-top: 10px;
                min-width: 150px;
                transition: background-color 0.3s, color 0.3s;
            }
            QPushButton:hover {
                background-color: #677D6A;
                color: white;
            }
        """)
        self.btn_change_password.clicked.connect(self.open_change_password_dialog)
        layout.addWidget(self.btn_change_password)

        # Connect the Enter key to trigger the login
        self.le_username.returnPressed.connect(self.animate_login)
        self.le_password.returnPressed.connect(self.animate_login)

    def animate_login(self):
        # Change button color briefly
        self.btn_login.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 16px;
                background-color: #333;
                color: white;
                border: 2px solid #677D6A;
                border-radius: 10px;
                margin-top: 20px;
                min-width: 150px;
                transition: background-color 0.3s, color 0.3s;
            }
            QPushButton:hover {
                background-color: #1976D2;
                color: white;
            }
        """)

        # Reset button color after a delay (optional)
        QTimer.singleShot(200, self.reset_button_style)

        # Perform login action
        self.login()

    def reset_button_style(self):
        self.btn_login.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 16px;
                background-color: #1976D2;
                border: 2px solid #000;
                color: white;
                border-radius: 10px;
                margin-top: 20px;
                min-width: 150px;
                transition: background-color 0.3s, color 0.3s;
            }
            QPushButton:hover {
                background-color: #1976D2;
                color: white;
            }
        """)

    def login(self):
        username = self.le_username.text().strip()
        password = self.le_password.text().strip()

        if username=="Rafik" and password=="Luxorapp":
            QMessageBox.information(self, 'Login', 'You are now logged in!', QMessageBox.Ok)
            self.hide()

            self.main_window = main_window.MainWindow()
            self.main_window.show()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Please enter your username and password.', QMessageBox.Ok)

    def open_change_password_dialog(self):
        dialog = passwordchange.ChangePasswordDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Handle any additional logic if needed after the password has been changed
            pass







if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
