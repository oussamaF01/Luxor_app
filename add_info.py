import os
import sys
from PyQt5.QtGui import QPixmap, QIcon, QFontDatabase
import logging
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget,
    QComboBox, QHBoxLayout, QPushButton, QMessageBox, QFileDialog, QDialog, QLabel, QLineEdit,QSpacerItem,QSizePolicy,QGridLayout
)
from PyQt5.QtCore import Qt, QStandardPaths,QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import add_prod
# Setup logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Define SQLAlchemy base
Base = declarative_base()

# Define database models
class Produits(Base):
    __tablename__ = 'produits'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    unite = Column(String)
    colisage = Column(String)
    devise = Column(String)
    prix_unitaire = Column(Float)
    quantite = Column(Float)
    fournisseur = Column(String)
    lieu_enlevement = Column(String)
    poids = Column(Float)
    qte_par_palette = Column(Float)
    autorisation = Column(String)
    positionn_tarifaire = Column(String)
    droits_taxe = Column(Float)
    EUR1 = Column(Boolean)
    Incoterm = Column(String)
    pelletisation = Column(Boolean)
    libre = Column(Boolean)
    Convention_de_commerce = Column(String)
    origine = Column(String)
    assurance = Column(Float)
    danger_class = Column(String)
    total_cost = Column(Float)
    code = Column(Integer)
    prix_revient = Column(Float)

    # Define relationships


class Fournisseurs(Base):
    __tablename__ = 'fournisseurs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    Adresse_de_siege = Column(String)
    Adresse_de_usine = Column(String)
    devise = Column(String)
    modalite_paiment = Column(String)

class Devise(Base):
    __tablename__ = 'devise'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    taux_change = Column(Float)


class Unites(Base):
    __tablename__ = 'unites'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class DroitsTaxe(Base):
    __tablename__ = 'droits_taxe'
    id = Column(Integer, primary_key=True, autoincrement=True)
    designation = Column(String)
    taxes = Column(Float)


class Emballage(Base):
    __tablename__ = 'emballage'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_emballage = Column(String)


class Autorisation(Base):
    __tablename__ = 'autorisation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    designation = Column(String)
    ministere = Column(String)


class PositionnTarifaire(Base):
    __tablename__ = 'positionn_tarifaire'
    id = Column(Integer, primary_key=True, autoincrement=True)
    HS_code = Column(Integer)
    designation = Column(String)
    droits_taxe = Column(String)
    autorisation = Column(String)


class ClasseDanger(Base):
    __tablename__ = 'classe_danger'
    id = Column(Integer, primary_key=True, autoincrement=True)
    UN = Column(String)
    classe = Column(Integer)


class Convention(Base):
    __tablename__ = 'convention'
    id = Column(Integer, primary_key=True, autoincrement=True)
    designation = Column(String)
    dd = Column(Float)


class Incoterm(Base):
    __tablename__ = 'incoterm'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class ModalitePaiment(Base):
    __tablename__ = 'modalite_paiment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

class conteneur  (Base):
    __tablename__ = 'conteneur'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    prix = Column(Float)
    devise = Column(String)
    volume = Column(Float)
    UC = Column(Float)

class origin (Base):
    __tablename__ = 'origin'
    id= Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String)

current_path = os.getcwd()
print(current_path)
# Setup SQLAlchemy engine and session
engine = create_engine(f'sqlite:///{current_path}\\db\\file.db')
Base.metadata.create_all(engine)  # Ensure the database is created
Session = sessionmaker(bind=engine)



class AddFournisseurDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Fournisseur")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Name")
        layout.addWidget(self.name_input)

        self.adresse_siege_input = QLineEdit(self)
        self.adresse_siege_input.setPlaceholderText("Adresse de Siege")
        layout.addWidget(self.adresse_siege_input)

        self.adresse_usine_input = QLineEdit(self)
        self.adresse_usine_input.setPlaceholderText("Adresse de Usine")
        layout.addWidget(self.adresse_usine_input)

        self.devise_input = QComboBox(self)
        self.devise_input.setStyleSheet("""
            QComboBox {
                border: 1px solid #000000;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
            }
        """)
        self.load_devise_options()
        layout.addWidget(self.devise_input)

        self.modalite_paiment_input = QLineEdit(self)
        self.modalite_paiment_input.setPlaceholderText("Modalite de Paiement")
        layout.addWidget(self.modalite_paiment_input)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.add_fournisseur)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #f2f2f2;
            }
            QLineEdit {
                border: 1px solid #000000;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #000000;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)

    def load_devise_options(self):
        try:
            session = Session()
            devises = session.query(Devise).all()
            for devise in devises:
                self.devise_input.addItem(devise.name)
            session.close()
        except Exception as e:
            logging.error(f"Error loading devise options: {e}")
            QMessageBox.critical(self, "Error", "Failed to load devise options")

    def add_fournisseur(self):
        name = self.name_input.text()
        adresse_siege = self.adresse_siege_input.text()
        adresse_usine = self.adresse_usine_input.text()
        devise = self.devise_input.currentText()
        modalite_paiment = self.modalite_paiment_input.text()

        if not (name and adresse_siege and adresse_usine and devise and modalite_paiment):
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return

        try:
            session = Session()
            new_fournisseur = Fournisseurs(
                name=name,
                Adresse_de_siege=adresse_siege,
                Adresse_de_usine=adresse_usine,
                devise=devise,
                modalite_paiment=modalite_paiment
            )
            session.add(new_fournisseur)
            session.commit()
            logging.info(f"New Fournisseur added: {name}")
            QMessageBox.information(self, "Success", "New Fournisseur added successfully")
            self.close()
        except Exception as e:
            session.rollback()
            logging.error(f"Error adding fournisseur: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add Fournisseur: {e}")
        finally:
            session.close()
class AddDeviseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Devise")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add a title label
        title_label = QLabel("Add New Devise", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #000000;
            margin-bottom: 20px;
        """)
        layout.addWidget(title_label)

        # Add input fields with improved styling
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Name")
        self.name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #000000;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.name_input)

        self.taux_change_input = QLineEdit(self)
        self.taux_change_input.setPlaceholderText("Taux de Change")
        self.taux_change_input.setStyleSheet(self.name_input.styleSheet())
        layout.addWidget(self.taux_change_input)

        # Add submit button with improved styling
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.add_devise)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                border: none;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        layout.addWidget(self.submit_button)

        # Set the dialog layout and style
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #f2f2f2;
                border-radius: 10px;
            }
        """)

    def add_devise(self):
        name = self.name_input.text()
        taux_change = self.taux_change_input.text()

        if not (name and taux_change):
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return

        try:
            session = Session()
            new_devise = Devise(
                name=name,
                taux_change=float(taux_change)
            )
            session.add(new_devise)
            session.commit()
            logging.info(f"New Devise added: {name}")
            QMessageBox.information(self, "Success", "New Devise added successfully")
            self.close()
        except Exception as e:
            logging.error(f"Error adding devise: {e}")
            QMessageBox.critical(self, "Error", "Failed to add Devise")
        finally:
            session.close()


class AddUnitesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Unit")
        self.setGeometry(100, 100, 400, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add a title label
        title_label = QLabel("Add New Unit", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #000000;
            margin-bottom: 20px;
        """)
        layout.addWidget(title_label)

        # Add input field for unit name with improved styling
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Name")
        self.name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #000000;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.name_input)

        # Add submit button with improved styling
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.add_unite)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                border: none;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        layout.addWidget(self.submit_button)

        # Set the dialog layout and style
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border-radius: 10px;
            }
        """)

    def add_unite(self):
        name = self.name_input.text()

        if not name:
            QMessageBox.warning(self, "Input Error", "Name field is required")
            return

        try:
            session = Session()
            new_unite = Unites(name=name)
            session.add(new_unite)
            session.commit()
            logging.info(f"New Unit added: {name}")
            QMessageBox.information(self, "Success", "New Unit added successfully")
            self.close()
        except Exception as e:
            logging.error(f"Error adding unit: {e}")
            QMessageBox.critical(self, "Error", "Failed to add Unit")
        finally:
            session.close()

class AddEmballageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Emballage")
        self.setGeometry(100, 100, 400, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add a title label
        title_label = QLabel("Add New Emballage", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #000000;
            margin-bottom: 20px;
        """)
        layout.addWidget(title_label)

        # Add input field for emballage type with improved styling
        self.type_input = QLineEdit(self)
        self.type_input.setPlaceholderText("Type d'Emballage")
        self.type_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #000000;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.type_input)

        # Add submit button with improved styling
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.add_emballage)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                border: none;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        layout.addWidget(self.submit_button)

        # Set the dialog layout and style
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border-radius: 10px;
            }
        """)

    def add_emballage(self):
        type_emballage = self.type_input.text()

        if not type_emballage:
            QMessageBox.warning(self, "Input Error", "Type d'Emballage field is required")
            return

        try:
            session = Session()
            new_emballage = Emballage(type_emballage=type_emballage)
            session.add(new_emballage)
            session.commit()
            logging.info(f"New Emballage added: {type_emballage}")
            QMessageBox.information(self, "Success", "New Emballage added successfully")
            self.close()
        except Exception as e:
            logging.error(f"Error adding emballage: {e}")
            QMessageBox.critical(self, "Error", "Failed to add Emballage")
        finally:
            session.close()

class AddAutorisationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Autorisation")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add a title label
        title_label = QLabel("Add New Autorisation", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #000000;
            margin-bottom: 20px;
        """)
        layout.addWidget(title_label)

        # Add input field for designation
        self.designation_input = QLineEdit(self)
        self.designation_input.setPlaceholderText("Designation")
        self.designation_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #000000;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.designation_input)

        # Add input field for ministere
        self.ministere_input = QLineEdit(self)
        self.ministere_input.setPlaceholderText("Ministere")
        self.ministere_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #000000;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.ministere_input)

        # Add submit button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.add_autorisation)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                border: none;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        layout.addWidget(self.submit_button)

        # Set the dialog layout and style
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border-radius: 10px;
            }
        """)

    def add_autorisation(self):
        designation = self.designation_input.text()
        ministere = self.ministere_input.text()

        if not (designation and ministere):
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return

        try:
            session = Session()
            new_autorisation = Autorisation(
                designation=designation,
                ministere=ministere
            )
            session.add(new_autorisation)
            session.commit()
            logging.info(f"New Autorisation added: {designation}")
            QMessageBox.information(self, "Success", "New Autorisation added successfully")
            self.close()
        except Exception as e:
            logging.error(f"Error adding autorisation: {e}")
            QMessageBox.critical(self, "Error", "Failed to add Autorisation")
        finally:
            session.close()




class AddConventionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Convention")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add a title label
        title_label = QLabel("Add New Convention", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #000000;
            margin-bottom: 20px;
        """)
        layout.addWidget(title_label)

        # Add input field for designation
        self.designation_input = QLineEdit(self)
        self.designation_input.setPlaceholderText("Designation")
        self.designation_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #000000;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.designation_input)

        # Add input field for dd
        self.dd_input = QLineEdit(self)
        self.dd_input.setPlaceholderText("DD (Decimal)")
        self.dd_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #000000;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.dd_input)

        # Add submit button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.add_convention)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                border: none;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        layout.addWidget(self.submit_button)

        # Set the dialog layout and style
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border-radius: 10px;
            }
        """)

    def add_convention(self):
        designation = self.designation_input.text()
        dd = self.dd_input.text()

        if not (designation and dd):
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return

        try:
            session = Session()
            new_convention = Convention(
                designation=designation,
                dd=float(dd)
            )
            session.add(new_convention)
            session.commit()
            logging.info(f"New Convention added: {designation}")
            QMessageBox.information(self, "Success", "New Convention added successfully")
            self.close()
        except Exception as e:
            session.rollback()
            logging.error(f"Error adding convention: {e}")
            QMessageBox.critical(self, "Error", "Failed to add Convention")
        finally:
            session.close()

class AddIncotermDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Incoterm")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add a title label
        title_label = QLabel("Add New Incoterm", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #000000;
            margin-bottom: 20px;
        """)
        layout.addWidget(title_label)

        # Add input field for name
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Name")
        self.name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #000000;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.name_input)

        # Add submit button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.add_incoterm)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                border: none;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        layout.addWidget(self.submit_button)

        # Set the dialog layout and style
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border-radius: 10px;
            }
        """)

    def add_incoterm(self):
        name = self.name_input.text()

        if not name:
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return

        try:
            session = Session()
            new_incoterm = Incoterm(
                name=name
            )
            session.add(new_incoterm)
            session.commit()
            logging.info(f"New Incoterm added: {name}")
            QMessageBox.information(self, "Success", "New Incoterm added successfully")
            self.close()
        except Exception as e:
            session.rollback()
            logging.error(f"Error adding incoterm: {e}")
            QMessageBox.critical(self, "Error", "Failed to add Incoterm")
        finally:
            session.close()




class AddModalitePaimentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Modalité de Paiement")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add a title label
        title_label = QLabel("Add New Modalité de Paiement", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        """)
        layout.addWidget(title_label)

        # Add input field for name
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Name")
        self.name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #333;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.name_input)

        # Add submit button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.add_modalite_paiment)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                border: none;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        layout.addWidget(self.submit_button)

        # Set the dialog layout and style
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #e3f2fd;
                border-radius: 10px;
            }
        """)

    def add_modalite_paiment(self):
        name = self.name_input.text()

        if not name:
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return

        try:
            session = Session()
            new_modalite_paiment = ModalitePaiment(
                name=name
            )
            session.add(new_modalite_paiment)
            session.commit()
            logging.info(f"New Modalité de Paiement added: {name}")
            QMessageBox.information(self, "Success", "New Modalité de Paiement added successfully")
            self.close()
        except Exception as e:
            logging.error(f"Error adding modalité de paiement: {e}")
            QMessageBox.critical(self, "Error", "Failed to add Modalité de Paiement")
        finally:
            session.close()

class AddConteneurDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Conteneur")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add a title label
        title_label = QLabel("Add New Conteneur", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        """)
        layout.addWidget(title_label)

        # Add input field for name
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Name")
        self.name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #333;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.name_input)

        # Add input field for prix
        self.prix_input = QLineEdit(self)
        self.prix_input.setPlaceholderText("Prix")
        self.prix_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #333;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.prix_input)

        # Add input field for devise
        self.devise_input = QComboBox(self)
        self.devise_input.setStyleSheet("""
            QComboBox {
                border: 1px solid #333;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
                background-color: #ffffff;
            }
        """)
        self.load_devise_options()
        layout.addWidget(self.devise_input)

        # Add input field for volume
        self.volume_input = QLineEdit(self)
        self.volume_input.setPlaceholderText("Volume")
        self.volume_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #333;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.volume_input)

        # Add input field for UC
        self.uc_input = QLineEdit(self)
        self.uc_input.setPlaceholderText("UC")
        self.uc_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #333;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
                background-color: #ffffff;
            }
        """)
        layout.addWidget(self.uc_input)

        # Add submit button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.add_conteneur)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                border: none;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        layout.addWidget(self.submit_button)

        # Set the dialog layout and style
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #e3f2fd;
                border-radius: 10px;
            }
        """)

    def load_devise_options(self):
        try:
            session = Session()
            devises = session.query(Devise).all()
            for devise in devises:
                self.devise_input.addItem(devise.name)
            session.close()
        except Exception as e:
            logging.error(f"Error loading devise options: {e}")
            QMessageBox.critical(self, "Error", "Failed to load devise options")

    def add_conteneur(self):
        name = self.name_input.text()
        prix = self.prix_input.text()
        devise = self.devise_input.currentText()
        volume = self.volume_input.text()
        uc = self.uc_input.text()

        # Check if all fields are filled
        if not (name and prix and devise and volume and uc):
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return

        # Validate numeric fields
        try:
            prix = float(prix)
            volume = float(volume)
            uc = float(uc)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Prix, Volume, and UC must be numeric")
            return

        # Add new conteneur to the database
        try:
            session = Session()
            new_conteneur = conteneur(
                name=name,
                prix=prix,
                devise=devise,
                volume=volume,
                UC=uc
            )
            session.add(new_conteneur)
            session.commit()
            logging.info(f"New Conteneur added: {name}")
            QMessageBox.information(self, "Success", "New Conteneur added successfully")
            self.close()
        except Exception as e:
            session.rollback()
            logging.error(f"Error adding conteneur: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add Conteneur: {e}")
        finally:
            session.close()

class AddOriginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Origin")
        self.setGeometry(100, 100, 400, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.origin_input = QLineEdit(self)
        self.origin_input.setPlaceholderText("Origin")
        layout.addWidget(self.origin_input)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.add_origin)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #e3f2fd;
            }
            QLineEdit {
                border: 1px solid #333;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #333;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)

    def add_origin(self):
        origin_text = self.origin_input.text()

        if not origin_text:
            QMessageBox.warning(self, "Input Error", "Origin field is required")
            return

        try:
            session = Session()
            new_origin = origin(name=origin_text)
            session.add(new_origin)
            session.commit()
            logging.info(f"New Origin added: {origin_text}")
            QMessageBox.information(self, "Success", "New Origin added successfully")
            self.close()
        except Exception as e:
            logging.error(f"Error adding origin: {e}")
            QMessageBox.critical(self, "Error", f"Failed to add Origin: {e}")
        finally:
            session.close()


class EmptyWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Information")
        self.setGeometry(100, 100, 700, 700)
        font_id = QFontDatabase.addApplicationFont(f'{current_path}\\font\\Roboto-Black.ttf')
        self.setWindowIcon(QIcon(f'{current_path}\\img\\Luxor.ico'))

        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setStyleSheet(f"""
                background-color: #f0f0f0;
                font-family: '{font_family}';
                font-size: 14px;
                color: #333;
            """)
        else:
            print("Failed to load font.")

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #fff;")

        main_layout = QVBoxLayout()

        # Add title label
        label = QLabel("Add Information", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            font-size: 20px;
            padding-bottom:50px;
            padding-top:50px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(label)

        # Add logo image
        img_label = QLabel(self)
        pixmap = QPixmap(f'{current_path}\\icons\\information.png').scaledToWidth(200)


        img_label.setPixmap(pixmap)
        img_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(img_label)

        # Spacer for additional spacing
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add buttons in a grid layout
        grid_layout = QGridLayout()

        categories = [
            ('Fournisseurs', f'{current_path}\\icons\\1.png'),
            ('Devise', f'{current_path}\\icons\\2.png'),
            ('Unites', f'{current_path}\\icons\\3.png'),
            ('Emballage', f'{current_path}\\icons\\4.png'),
            ('Autorisation', f'{current_path}\\icons\\5.png'),
            ('Convention', f'{current_path}\\icons\\6.png'),
            ('Incoterm', f'{current_path}\\icons\\7.png'),
            ('Modalite de Paiement', f'{current_path}\\icons\\8.png'),
            ('Conteneur', f'{current_path}\\icons\\9.png'),
            ('Origine', f'{current_path}\\icons\\10.png'),
            ('ADD Product', f'{current_path}\\icons\\11.png'),  # New button
            ('Add Class de Danger', f'{current_path}\\icons\\12.png')  # New button
        ]

        row = 0
        col = 0
        for category, icon_path in categories:
            button = QPushButton(f'Add {category}', self)
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(32, 32))
            button.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    background-color: #007BFF; /* Blue background */
                    color: white;
                    padding: 10px;
                    margin: 5px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #0056b3; /* Darker blue on hover */
                    transition: background-color 0.3s;
                }
            """)
            button.clicked.connect(self.get_dialog_function(category))

            # Add the button to the grid layout
            grid_layout.addWidget(button, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def get_dialog_function(self, category):
        """Return the appropriate dialog method based on the category."""
        dialog_methods = {
            'Fournisseurs': self.open_add_fournisseur_dialog,
            'Devise': self.open_add_devise_dialog,
            'Unites': self.open_add_unites_dialog,
            'Emballage': self.open_add_emballage_dialog,
            'Autorisation': self.open_add_autorisation_dialog,
            'Convention': self.open_add_convention_dialog,
            'Incoterm': self.open_add_incoterm_dialog,
            'Modalite de Paiement': self.open_add_modalite_paiment_dialog,
            'Conteneur': self.open_add_conteneur_dialog,
            'Origine': self.open_add_Origine,
            'ADD Product': self.open_add_product_dialog,
            'Add Class de Danger': self.open_add_class_de_danger_dialog
        }
        return dialog_methods.get(category, lambda: self.add_information(category))

    def open_add_Origine(self):
        self.add_origin_dialog = AddOriginDialog(self)
        self.add_origin_dialog.exec_()

    def open_add_modalite_paiment_dialog(self):
        self.add_modalite_paiment_dialog = AddModalitePaimentDialog(self)
        self.add_modalite_paiment_dialog.exec_()

    def open_add_conteneur_dialog(self):
        self.add_conteneur_dialog = AddConteneurDialog(self)
        self.add_conteneur_dialog.exec_()

    def open_add_convention_dialog(self):
        self.add_convention_dialog = AddConventionDialog(self)
        self.add_convention_dialog.exec_()

    def open_add_incoterm_dialog(self):
        self.add_incoterm_dialog = AddIncotermDialog(self)
        self.add_incoterm_dialog.exec_()

    def open_add_autorisation_dialog(self):
        self.add_autorisation_dialog = AddAutorisationDialog(self)
        self.add_autorisation_dialog.exec_()

    def open_add_emballage_dialog(self):
        self.add_emballage_dialog = AddEmballageDialog(self)
        self.add_emballage_dialog.exec_()

    def open_add_fournisseur_dialog(self):
        self.add_fournisseur_dialog = AddFournisseurDialog(self)
        self.add_fournisseur_dialog.exec_()

    def open_add_devise_dialog(self):
        self.add_devise_dialog = AddDeviseDialog(self)
        self.add_devise_dialog.exec_()

    def open_add_unites_dialog(self):
        self.add_unites_dialog = AddUnitesDialog(self)
        self.add_unites_dialog.exec_()

    def open_add_product_dialog(self):
        add_product_dialog = add_prod.AddProductForm()
        add_product_dialog.exec_()

    def open_add_class_de_danger_dialog(self):
        QMessageBox.information(self, "Add Danger classe",
                                f"Add  information functionality not implemented yet.")

    def add_information(self, category):
        QMessageBox.information(self, "Add Information",
                                f"Add {category} information functionality not implemented yet.")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmptyWindow()
    window.show()
    sys.exit(app.exec_())
