from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QTableWidget, \
    QTableWidgetItem, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

current_path = os.getcwd()

# Define your database connection
DATABASE_URL = f'sqlite:///{current_path}/db/file.db'  # Update with your actual database URL
Base = declarative_base()


class Produits(Base):
    __tablename__ = 'produits'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    unite = Column(String)
    colisage = Column(String)
    devise = Column(String)
    prix_unitaire = Column(Float)
    fournisseur = Column(String)
    lieu_enlevement = Column(String)
    autorisation = Column(String)
    EUR1 = Column(Boolean)
    Incoterm = Column(String)
    pelletisation = Column(Boolean)
    libre = Column(Boolean)
    Convention_de_commerce = Column(String)
    origine = Column(String)
    danger_class = Column(String)
    code = Column(Integer)
    prix_revient = Column(Float)
    # Define relationships
    tax_info = relationship("TaxInfo", back_populates="product")
    msds_tech = relationship("MsdsTech", back_populates="product")
    classe_danger = relationship("ClasseDanger", back_populates="product")


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
    produit_id = Column(Integer, ForeignKey('produits.id'))
    product = relationship("Produits", back_populates="classe_danger")


class Convention(Base):
    __tablename__ = 'convention'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    dd = Column(Float)


class Incoterm(Base):
    __tablename__ = 'incoterm'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class ModalitePaiment(Base):
    __tablename__ = 'modalite_paiment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class Conteneur(Base):
    __tablename__ = 'conteneur'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    prix = Column(Float)
    devise = Column(String)
    volume = Column(Float)
    UC = Column(Float)


class Origin(Base):
    __tablename__ = 'origin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class TaxInfo(Base):
    __tablename__ = 'tax_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    TVA = Column(Float)
    FODEC = Column(Float)
    DD = Column(Float)
    TPE = Column(Float)
    RPD = Column(Float)
    product_id = Column(Integer, ForeignKey('produits.id'))
    product = relationship("Produits", back_populates="tax_info")


class MsdsTech(Base):
    __tablename__ = 'msds_tech'
    id = Column(Integer, primary_key=True, autoincrement=True)
    msds = Column(BLOB)
    tech = Column(BLOB)
    prod_id = Column(Integer, ForeignKey('produits.id'))
    product = relationship("Produits", back_populates="msds_tech")


# Set up SQLAlchemy
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Explorer")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon(f'{current_path}\\img\\Luxor.ico'))

        main_layout = QVBoxLayout(self)
        controls_layout = QHBoxLayout()
        main_layout.addLayout(controls_layout)

        self.table_selector = QComboBox()
        self.table_selector.addItems(["Fournisseurs", "Devise", "Unites", "Emballage", "Autorisation",
                                      "PositionnTarifaire", "ClasseDanger", "Convention", "Incoterm",
                                      "ModalitePaiment", "Conteneur", "Origin", "TaxInfo"])
        controls_layout.addWidget(self.table_selector)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.textChanged.connect(self.filter_data)
        controls_layout.addWidget(self.search_input)

        self.load_button = QPushButton("Load Data")
        self.load_button.setFixedWidth(100)
        self.load_button.setStyleSheet("background-color: #508C9B; color: white;")
        self.load_button.clicked.connect(self.load_data)
        controls_layout.addWidget(self.load_button)

        self.save_button = QPushButton("Save Changes")
        self.save_button.setFixedWidth(100)
        self.save_button.setStyleSheet("background-color: #508C9B; color: white;")
        self.save_button.clicked.connect(self.save_changes)
        controls_layout.addWidget(self.save_button)

        self.delete_button = QPushButton("Delete Row")
        self.delete_button.setFixedWidth(100)
        self.delete_button.setStyleSheet("background-color: #d9534f; color: white;")
        self.delete_button.clicked.connect(self.delete_row)
        controls_layout.addWidget(self.delete_button)

        self.export_button = QPushButton("Export to PDF")
        self.export_button.setFixedWidth(100)
        self.export_button.setStyleSheet("background-color: #508C9B; color: white;")
        self.export_button.clicked.connect(self.export_to_pdf)
        controls_layout.addWidget(self.export_button)

        self.table_view = QTableWidget()
        main_layout.addWidget(self.table_view)

        self.data = []  # Store the loaded data

    def save_changes(self):
        selected_table = self.table_selector.currentText()

        table_mapping = {
            "Produits": Produits,
            "Fournisseurs": Fournisseurs,
            "Devise": Devise,
            "Unites": Unites,
            "Emballage": Emballage,
            "Autorisation": Autorisation,
            "PositionnTarifaire": PositionnTarifaire,
            "ClasseDanger": ClasseDanger,
            "Convention": Convention,
            "Incoterm": Incoterm,
            "ModalitePaiment": ModalitePaiment,
            "Conteneur": Conteneur,
            "Origin": Origin,
            "TaxInfo": TaxInfo,
        }

        model_class = table_mapping.get(selected_table)
        if model_class is None:
            print("Error: Invalid table selection.")
            return

        data = session.query(model_class).all()

        for row_idx in range(self.table_view.rowCount()):
            for col_idx in range(self.table_view.columnCount()):
                item = self.table_view.item(row_idx, col_idx)
                if item:
                    column_name = list(data[0].__table__.columns.keys())[col_idx]
                    value = item.text()

                    if column_name in ["EUR1", "pelletisation", "libre"]:
                        value = value == 'True'
                    elif column_name in ["prix_unitaire", "prix_revient"]:
                        value = float(value)
                    elif column_name in ["id", "code", "HS_code"]:
                        value = int(value)
                    else:
                        value = str(value)

                    setattr(data[row_idx], column_name, value)

        try:
            session.commit()
            QMessageBox.information(self, "Save Changes", "Changes saved successfully.")
        except Exception as e:
            print(f"Error saving changes: {e}")
            session.rollback()

    def delete_row(self):
        selected_row = self.table_view.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Delete Row", "No row selected for deletion.")
            return

        selected_table = self.table_selector.currentText()

        table_mapping = {
            "Produits": Produits,
            "Fournisseurs": Fournisseurs,
            "Devise": Devise,
            "Unites": Unites,
            "Emballage": Emballage,
            "Autorisation": Autorisation,
            "PositionnTarifaire": PositionnTarifaire,
            "ClasseDanger": ClasseDanger,
            "Convention": Convention,
            "Incoterm": Incoterm,
            "ModalitePaiment": ModalitePaiment,
            "Conteneur": Conteneur,
            "Origin": Origin,
            "TaxInfo": TaxInfo,
        }

        model_class = table_mapping.get(selected_table)
        if model_class is None:
            print("Error: Invalid table selection.")
            return

        data = session.query(model_class).all()
        item_to_delete = data[selected_row]

        try:
            session.delete(item_to_delete)
            session.commit()
            self.table_view.removeRow(selected_row)
            QMessageBox.information(self, "Delete Row", "Row deleted successfully.")
        except Exception as e:
            print(f"Error deleting row: {e}")
            session.rollback()
            QMessageBox.warning(self, "Delete Row", f"Error deleting row: {e}")

    def load_data(self):
        selected_table = self.table_selector.currentText()

        table_mapping = {
            "Produits": Produits,
            "Fournisseurs": Fournisseurs,
            "Devise": Devise,
            "Unites": Unites,
            "Emballage": Emballage,
            "Autorisation": Autorisation,
            "PositionnTarifaire": PositionnTarifaire,
            "ClasseDanger": ClasseDanger,
            "Convention": Convention,
            "Incoterm": Incoterm,
            "ModalitePaiment": ModalitePaiment,
            "Conteneur": Conteneur,
            "Origin": Origin,
            "TaxInfo": TaxInfo,
        }

        model_class = table_mapping.get(selected_table)
        if model_class is None:
            print("Error: Invalid table selection.")
            return

        data = session.query(model_class).all()
        self.data = data

        self.table_view.setRowCount(len(data))
        self.table_view.setColumnCount(len(data[0].__table__.columns.keys()))
        self.table_view.setHorizontalHeaderLabels(data[0].__table__.columns.keys())

        for row_idx, row_data in enumerate(data):
            for col_idx, column in enumerate(row_data.__table__.columns.keys()):
                value = getattr(row_data, column)
                if value is True:
                    value = "True"
                elif value is False:
                    value = "False"
                else:
                    value = str(value)
                item = QTableWidgetItem(value)
                self.table_view.setItem(row_idx, col_idx, item)

    def filter_data(self):
        filter_text = self.search_input.text().lower()
        for row in range(self.table_view.rowCount()):
            match = False
            for col in range(self.table_view.columnCount()):
                item = self.table_view.item(row, col)
                if item and filter_text in item.text().lower():
                    match = True
                    break
            self.table_view.setRowHidden(row, not match)

    def export_to_pdf(self):
        file_path = os.path.join(current_path, "exported_table.pdf")
        doc = SimpleDocTemplate(file_path, pagesize=letter)

        data = []
        # Adding the headers
        headers = [self.table_view.horizontalHeaderItem(col).text() for col in range(self.table_view.columnCount())]
        data.append(headers)

        # Adding the data
        for row in range(self.table_view.rowCount()):
            row_data = []
            for col in range(self.table_view.columnCount()):
                item = self.table_view.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)

        # Creating the table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements = [table]
        doc.build(elements)

        QMessageBox.information(self, "Export to PDF", f"Table data exported to {file_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
