import sys
import os
import logging
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QTableView, QHBoxLayout, QHeaderView
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex
from PyQt5.QtGui import QIcon
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define paths
current_path = os.getcwd()
db_path = os.path.join(current_path, 'db', 'file.db')
icon_path = os.path.join(current_path, 'img', 'Luxor.ico')

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# SQLAlchemy setup
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

    msds_tech = relationship("MsdsTech", back_populates="product")



class MsdsTech(Base):
    __tablename__ = 'msds_tech'
    id = Column(Integer, primary_key=True, autoincrement=True)
    msds = Column(BLOB)
    tech = Column(BLOB)
    prod_id = Column(Integer, ForeignKey('produits.id'))
    produit = relationship("Produits", back_populates="msds_tech")


Produits.msds_tech = relationship("MsdsTech", order_by=MsdsTech.id, back_populates="produit")

engine = create_engine(f'sqlite:///{db_path}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


# PyQt5 Model
class ProductMsdsModel(QAbstractTableModel):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.data_list = []
        self.load_data()

    def load_data(self):
        query = self.session.query(Produits, MsdsTech).join(MsdsTech, Produits.id == MsdsTech.prod_id).all()
        self.data_list = [
            (produit.id, produit.name, msds_tech.msds, msds_tech.tech)
            for produit, msds_tech in query
        ]

    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self.data_list)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return 2  # Number of columns to display: ID, Name

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> QVariant:
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()

        produit_id, name, _, _ = self.data_list[index.row()]
        if index.column() == 0:
            return produit_id
        elif index.column() == 1:
            return name

        return QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> QVariant:
        headers = ["ID", "Name"]
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return headers[section]
        return QVariant()


# PyQt5 Window
class MsdsFTechWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('MSDS/FTech Information')
        self.resize(600, 400)

        # Set window icon
        self.setWindowIcon(QIcon(icon_path))

        # Layout setup
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.session = Session()

        # Table View
        self.table_view = QTableView()
        self.model = ProductMsdsModel(self.session)
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Allow selection of entire rows
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)

        # Connect selection model signals
        selection_model = self.table_view.selectionModel()
        selection_model.selectionChanged.connect(self.on_selection_changed)

        layout.addWidget(self.table_view)

        # Button layout
        button_layout = QVBoxLayout()

        # MSDS Button
        self.msds_button = QPushButton('MSDS')
        self.msds_button.clicked.connect(self.show_msds)
        button_layout.addWidget(self.msds_button)

        # Tech Button
        self.tech_button = QPushButton('Fiche Technique')
        self.tech_button.clicked.connect(self.show_tech)
        button_layout.addWidget(self.tech_button)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.selected_row = None

        # Apply styles
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QPushButton {
                background-color: #7BC9FF;
                color: white;
                border: 1px solid #fff;
                padding: 10px;
                margin: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius = 10px;
            }
            QPushButton:hover {
                background-color: darkgray;
            }
        """)

    def on_selection_changed(self, selected, deselected):
        indexes = self.table_view.selectionModel().selectedRows()
        if indexes:
            self.selected_row = indexes[0].row()
        else:
            self.selected_row = None

    def show_msds(self):
        if self.selected_row is not None:
            _, _, msds_data, _ = self.model.data_list[self.selected_row]
            self.display_pdf(msds_data, 'MSDS.pdf')

    def show_tech(self):
        if self.selected_row is not None:
            _, _, _, tech_data = self.model.data_list[self.selected_row]
            self.display_pdf(tech_data, 'Tech.pdf')

    def display_pdf(self, data, filename):
        try:
            temp_path = os.path.join(current_path, filename)
            with open(temp_path, 'wb') as file:
                file.write(data)
            os.startfile(temp_path)
        except Exception as e:
            logging.error(f"Error displaying PDF: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MsdsFTechWindow()
    window.show()
    sys.exit(app.exec_())
