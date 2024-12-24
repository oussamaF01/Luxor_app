from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QDialog, QLabel, QLineEdit, QPushButton,QFileDialog, QComboBox, \
    QCheckBox, \
    QDoubleSpinBox, QSpinBox, QGridLayout, QHBoxLayout,QMessageBox,QGroupBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, BLOB
import os
from sqlalchemy.ext.declarative import declarative_base

current_path = os.getcwd()
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


# Create the SQLite database engine and session
engine = create_engine(f'sqlite:///{current_path}\\db\\file.db')
Session = sessionmaker(bind=engine)
session = Session()


class AddProductForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(current_path, "img", "Luxor.ico")))
        self.setGeometry(100, 100, 600, 600)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add New Product')

        # Set blue theme
        self.setStyleSheet("""
            QWidget {
                background-color: #e0f7fa;
            }
            QLabel {
                color: #01579b;
            }
            QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox {
                background-color: #ffffff;
                border: 1px solid #0277bd;
                padding: 5px;
                border-radius: 5px;  
            }
            QCheckBox {
                color: #01579b;
            }
            QPushButton {
                background-color: #0288d1;
                color: white;
                border: none;
                padding: 10px 20px;  
                border-radius: 5px;   
                font-size: 16px;      
            }
            QPushButton:hover {
                background-color: #0277bd;
            }
            QGroupBox {
                border: 1px solid #0277bd;  
                border-radius: 5px;         
                margin-top: 20px;           
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;                 
                color: #01579b;             
            }
        """)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        title_label = QLabel("Add Product")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        grid_layout.addWidget(title_label, 0, 0, 1, 3, alignment=Qt.AlignCenter)

        form_layout1 = QFormLayout()
        form_layout2 = QFormLayout()
        form_layout3 = QFormLayout()

        input_width = 200
        self.create_input_fields(input_width)

        # Adding fields to form layouts
        form_layout1.addRow('Code:', self.code_input)
        form_layout1.addRow('Name:', self.name_input)
        form_layout1.addRow('Devise:', self.devise_input)
        form_layout1.addRow('Unite',self.unit_input)
        form_layout1.addRow('Prix Unitaire:', self.prix_unitaire_input)
        form_layout1.addRow('Fournisseur:', self.fournisseur_input)
        form_layout1.addRow('Colisage:', self.colisage_input)
        form_layout1.addRow('Lieu Enlevement:', self.lieu_enlevement_input)

        form_layout2.addRow('Libre:', self.libre_input)
        form_layout2.addRow('Autorisation:', self.autorisation_input)
        form_layout2.addRow('EUR1:', self.EUR1_input)
        form_layout2.addRow('Incoterm:', self.Incoterm_input)
        form_layout2.addRow('Pelletisation:', self.pelletisation_input)
        form_layout2.addRow('Convention:', self.convention_cheek_input)
        form_layout2.addRow('Convention de Commerce:', self.Convention_de_commerce_input)
        form_layout2.addRow('Origine:', self.origine_input)

        form_layout3.addRow('Danger:', self.danger_input)
        form_layout3.addRow('Danger Class:', self.danger_class_input)
        form_layout3.addRow('Code UN:', self.code_un_input)
        form_layout3.addRow('Fiche Technique: ', self.fiche_technique_button)
        form_layout3.addRow('MSDS:', self.msds_button)
        form_layout3.addRow('Prix Revient:', self.prix_revient_input)

        grid_layout.addLayout(form_layout1, 1, 0)
        grid_layout.addLayout(form_layout2, 1, 1)
        grid_layout.addLayout(form_layout3, 1, 2)

        tax_group = QGroupBox("Tax Information")
        tax_layout = QFormLayout()
        tax_layout.addRow('TVA:', self.tax_info_tva_input)
        tax_layout.addRow('FODEC:', self.tax_info_fodec_input)
        tax_layout.addRow('DD:', self.tax_info_dd_input)
        tax_layout.addRow('TPE:', self.tax_info_tpe_input)
        tax_layout.addRow('RPD:', self.tax_info_rpd_input)
        tax_group.setLayout(tax_layout)
        grid_layout.addWidget(tax_group, 2, 0, 1, 3)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton('Save')
        self.save_button.setFixedSize(150, 50)
        self.save_button.clicked.connect(self.save_product)
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addStretch()
        grid_layout.addLayout(button_layout, 3, 0, 1, 3)

        self.setLayout(grid_layout)
        self.populate_comboboxes()

        self.danger_input.stateChanged.connect(self.toggle_danger_fields)
        self.libre_input.stateChanged.connect(self.toggle_autorisation)
        self.convention_cheek_input.stateChanged.connect(self.toggle_convention_fields)

    def create_input_fields(self, input_width):
        self.code_input = QLineEdit()
        self.code_input.setFixedWidth(input_width)
        self.name_input = QLineEdit()
        self.name_input.setFixedWidth(input_width)
        self.devise_input = QComboBox()
        self.devise_input.setFixedWidth(input_width)
        self.unit_input = QComboBox()
        self.unit_input.setFixedWidth(input_width)
        self.prix_unitaire_input = QLineEdit()
        self.prix_unitaire_input.setFixedWidth(input_width)
        self.fournisseur_input = QComboBox()
        self.fournisseur_input.setFixedWidth(input_width)
        self.colisage_input = QComboBox()
        self.colisage_input.setFixedWidth(input_width)
        self.lieu_enlevement_input = QLineEdit()
        self.lieu_enlevement_input.setFixedWidth(input_width)

        self.libre_input = QCheckBox()
        self.libre_input.setChecked(True)
        self.autorisation_input = QComboBox()

        self.autorisation_input.setFixedWidth(input_width)
        self.autorisation_input.setEnabled(False)

        self.EUR1_input = QCheckBox()
        self.Incoterm_input = QComboBox()
        self.Incoterm_input.setFixedWidth(input_width)
        self.pelletisation_input = QCheckBox()
        self.convention_cheek_input = QCheckBox()
        self.Convention_de_commerce_input = QComboBox()
        self.Convention_de_commerce_input.setFixedWidth(input_width)
        self.Convention_de_commerce_input.setEnabled(False)
        self.origine_input = QComboBox()
        self.origine_input.setFixedWidth(input_width)

        self.danger_input = QCheckBox()
        self.danger_class_input = QLineEdit()
        self.danger_class_input.setFixedWidth(input_width)
        self.danger_class_input.setEnabled(False)
        self.code_un_input = QLineEdit()
        self.code_un_input.setFixedWidth(input_width)
        self.prix_revient_input = QLineEdit()
        self.prix_revient_input.setFixedWidth(input_width)
        #Upload file
        # MSDS and Fiche Technique

        self.msds_data = None
        self.fiche_technique_data =None

        self.fiche_technique_button = QPushButton("Upload Technical Sheet")
        self.fiche_technique_button.clicked.connect(self.upload_fiche_technique)
        self.msds_button = QPushButton("Upload MSDS")
        self.msds_button.clicked.connect(self.upload_msds)
        # Tax Information Fields
        self.tax_info_tva_input = QDoubleSpinBox()
        self.tax_info_tva_input.setMaximum(100)
        self.tax_info_tva_input.setFixedWidth(input_width)
        self.tax_info_fodec_input = QDoubleSpinBox()
        self.tax_info_fodec_input.setMaximum(100)
        self.tax_info_fodec_input.setFixedWidth(input_width)
        self.tax_info_dd_input = QDoubleSpinBox()
        self.tax_info_dd_input.setMaximum(100)
        self.tax_info_dd_input.setFixedWidth(input_width)
        self.tax_info_tpe_input = QDoubleSpinBox()
        self.tax_info_tpe_input.setMaximum(100)
        self.tax_info_tpe_input.setFixedWidth(input_width)
        self.tax_info_rpd_input = QDoubleSpinBox()
        self.tax_info_rpd_input.setMaximum(100)
        self.tax_info_rpd_input.setFixedWidth(input_width)

    def upload_fiche_technique(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Technical Sheet", "", "PDF Files (*.pdf);;All Files (*)")
        if file_path:
            self.fiche_technique_path = file_path
            self.fiche_technique_button.setText("Uploaded")


    def upload_msds(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload MSDS", "", "PDF Files (*.pdf);;All Files (*)")
        if file_path:
            self.msds_path = file_path
            self.msds_button.setText("Uploaded")

    def populate_comboboxes(self):
        # Populate your comboboxes with data from the database
        with Session() as session:
            # Populate Devise
            devises = session.query(Devise).all()
            self.devise_input.addItem("Select Devise")
            for devise in devises:
                self.devise_input.addItem(devise.name)
            # Populate unit
            unites = session.query(Unites).all()
            self.unit_input.addItem("Select Unites")
            for unite in unites:
                self.unit_input.addItem(unite.name)

            # Populate Fournisseur
            fournisseurs = session.query(Fournisseurs).all()
            self.fournisseur_input.addItem("Select Fournisseur")
            for fournisseur in fournisseurs:
                self.fournisseur_input.addItem(fournisseur.name)

            # Populate Autorisation
            autorisations = session.query(Autorisation).all()
            self.autorisation_input.addItem("Select Autorisation")
            for autorisation in autorisations:
                self.autorisation_input.addItem(autorisation.designation)

            # Populate Incoterm
            incoterms = session.query(Incoterm).all()
            self.Incoterm_input.addItem("Select Incoterm")
            for incoterm in incoterms:
                self.Incoterm_input.addItem(incoterm.name)

            # Populate Convention de Commerce
            conventions = session.query(Convention).all()
            self.Convention_de_commerce_input.addItem("Select Convention")
            for convention in conventions:
                self.Convention_de_commerce_input.addItem(convention.name)
            # load type d'emballage
            emballage = session.query(Emballage).all()
            self.colisage_input.addItem("Select Colisage")
            for i in emballage :
                self.colisage_input.addItem(i.type_emballage)
            # Populate Origine
            origines = session.query(Origin).all()
            self.origine_input.addItem("Select Origine")
            for origine in origines:
                self.origine_input.addItem(origine.name)

    def toggle_danger_fields(self):
        self.danger_class_input.setEnabled(self.danger_input.isChecked())

    def toggle_autorisation(self):
        self.autorisation_input.setEnabled(not(self.libre_input.isChecked()))

    def toggle_convention_fields(self):
        self.Convention_de_commerce_input.setEnabled(self.convention_cheek_input.isChecked())

    def save_product(self):
        session = Session()
        try:
            produit = Produits(
                code=int(self.code_input.text()),
                name=self.name_input.text(),
                unite=self.unit_input.currentText(),
                devise=self.devise_input.currentText(),
                prix_unitaire=float(self.prix_unitaire_input.text()),
                fournisseur=self.fournisseur_input.currentText(),
                colisage=self.colisage_input.currentText(),
                lieu_enlevement=self.lieu_enlevement_input.text(),
                libre=self.libre_input.isChecked(),
                autorisation=self.autorisation_input.currentText() if not self.libre_input.isChecked() else None,
                EUR1=self.EUR1_input.isChecked(),
                Incoterm=self.Incoterm_input.currentText(),
                pelletisation=self.pelletisation_input.isChecked(),
                Convention_de_commerce=self.Convention_de_commerce_input.currentText() if self.convention_cheek_input.isChecked() else None,
                origine=self.origine_input.currentText(),
                danger_class=self.danger_class_input.text() if self.danger_input.isChecked() else None,

                prix_revient=float(self.prix_revient_input.text()) if self.prix_revient_input.text() else None
            )

            session.add(produit)
            session.flush()  # Flush to get the produit.id

            tax_info = TaxInfo(
                TVA=self.tax_info_tva_input.value(),
                FODEC=self.tax_info_fodec_input.value(),
                DD=self.tax_info_dd_input.value(),
                TPE=self.tax_info_tpe_input.value(),
                RPD=self.tax_info_rpd_input.value(),
                product_id=produit.id
            )
            session.add(tax_info)
            if hasattr(self, 'msds_path'):
                with open(self.msds_path, 'rb') as file:
                    msds_data = file.read()

            if hasattr(self, 'fiche_technique_path'):
                with open(self.fiche_technique_path, 'rb') as file:
                    fiche_technique_data = file.read()

            if msds_data or fiche_technique_data:
                msds_tech = MsdsTech(
                    msds=msds_data,
                    tech=fiche_technique_data,
                    prod_id=produit.id
                )
                session.add(msds_tech)

            session.commit()
            QMessageBox.information(self, "Success", "Product saved successfully.")

            # Reset form after successful save
            self.reset_form()
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to save product: {str(e)}")
        finally:
            session.close()


    def reset_form(self):
        self.code_input.clear()
        self.name_input.clear()
        self.devise_input.setCurrentIndex(0)
        self.prix_unitaire_input.clear()
        self.fournisseur_input.setCurrentIndex(0)
        self.colisage_input.clear()
        self.lieu_enlevement_input.clear()
        self.libre_input.setChecked(False)
        self.autorisation_input.setCurrentIndex(0)


        self.EUR1_input.setChecked(False)
        self.Incoterm_input.setCurrentIndex(0)
        self.pelletisation_input.setChecked(False)
        self.convention_cheek_input.setChecked(False)
        self.Convention_de_commerce_input.setCurrentIndex(0)
        self.origine_input.setCurrentIndex(0)
        self.danger_input.setChecked(False)
        self.danger_class_input.clear()
        self.code_un_input.clear()
        self.prix_revient_input.clear()

        # Reset tax information
        self.tax_info_tva_input.setValue(0)
        self.tax_info_fodec_input.setValue(0)
        self.tax_info_dd_input.setValue(0)
        self.tax_info_tpe_input.setValue(0)
        self.tax_info_rpd_input.setValue(0)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    form = AddProductForm()
    form.show()
    sys.exit(app.exec_())
