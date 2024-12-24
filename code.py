import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFormLayout,
    QVBoxLayout, QHBoxLayout, QGroupBox, QComboBox, QCheckBox, QScrollArea,QMessageBox,QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

current_path = os.getcwd()

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
    tax_info = relationship("TaxInfo", back_populates="product")

class Devise(Base):
    __tablename__ = 'devise'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    taux_change = Column(Float)

class Conteneur(Base):
    __tablename__ = 'conteneur'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    prix = Column(Float)
    devise = Column(String)
    volume = Column(Float)
    UC = Column(Float)

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

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.engine = create_engine(f'sqlite:///{os.path.join(current_path, "db", "file.db")}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Product Information Form')
        self.setGeometry(100, 100, 1000, 700)

        # Set font for labels and group titles
        label_font = QFont('Arial', 12)
        group_title_font = QFont('Arial', 14, QFont.Bold)

        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        # Create group boxes with background colors
        product_info_group = QGroupBox('Product Information')
        tax_info_group = QGroupBox('Tax Information')
        logistic_cost_group = QGroupBox('Logistic Cost')
        return_fund_group = QGroupBox('Groupage')
        button_group = QGroupBox()

        # Set group box title font and background color
        group_stylesheet = f"""
        QGroupBox {{
            font: {group_title_font.pointSize()}pt {group_title_font.family()};
            font-weight: {group_title_font.weight()};
            background-color: #F5F5F5;
            border: 1px solid #000;
            border-radius: 5px;
            margin-top: 10px; 
        }}
        """
        product_info_group.setStyleSheet(group_stylesheet)
        tax_info_group.setStyleSheet(group_stylesheet)
        logistic_cost_group.setStyleSheet(group_stylesheet)
        return_fund_group.setStyleSheet(group_stylesheet)

        # Create layouts for each group
        product_info_layout = QFormLayout()
        tax_info_layout = QFormLayout()
        logistic_cost_layout = QFormLayout()
        return_fund_layout = QFormLayout()

        # Set larger margins for form layouts
        product_info_layout.setContentsMargins(10, 20, 10, 10)  # Increased top margin
        tax_info_layout.setContentsMargins(10, 20, 10, 10)  # Increased top margin
        logistic_cost_layout.setContentsMargins(10, 20, 10, 10)  # Increased top margin
        return_fund_layout.setContentsMargins(10, 20, 10, 10)  # Increased top margin

        # Align labels to the left
        product_info_layout.setLabelAlignment(Qt.AlignLeft)
        tax_info_layout.setLabelAlignment(Qt.AlignLeft)
        logistic_cost_layout.setLabelAlignment(Qt.AlignLeft)
        return_fund_layout.setLabelAlignment(Qt.AlignLeft)

        # Add product drop-down
        self.product_combo = QComboBox()
        self.product_combo.setFixedHeight(30)
        self.product_combo.setFixedWidth(200)
        self.loadProductNames()
        product_info_layout.addRow(QLabel('Produit'), self.product_combo)

        # Add other labels and line edits for Product Information
        self.devise_input = self.addFormRow(product_info_layout, 'Devise', label_font)
        self.addFormRow(product_info_layout, 'Volume', label_font)
        self.groupage_checkbox = QCheckBox()
        self.groupage_checkbox.stateChanged.connect(self.toggleReturnFundSection)
        self.groupage_checkbox.stateChanged.connect(self.toggleContainerCombo)
        product_info_layout.addRow(QLabel('Groupage'), self.groupage_checkbox)
        self.taux = self.addFormRow(product_info_layout, 'Exchange rate', label_font)

        # Add container drop-down
        self.container_combo = QComboBox()
        self.container_combo.setFixedHeight(30)
        self.container_combo.setFixedWidth(200)
        self.loadContainerNames()
        product_info_layout.addRow(QLabel('Container'), self.container_combo)

        # Add other input fields
        self.container_number_input = self.addFormRow(product_info_layout, 'Container Number', label_font)
        self.unit_price_edit = self.addFormRow(product_info_layout, 'Unit price', label_font)
        self.poids = self.addFormRow(product_info_layout, 'Weight', label_font)
        self.quantity = self.addFormRow(product_info_layout, 'Quantity', label_font)

        # Add labels and line edits for Tax Information
        self.TVA = self.addFormRow(tax_info_layout, '%TVA', label_font)
        self.DD = self.addFormRow(tax_info_layout, '%DD', label_font)
        self.TPE = self.addFormRow(tax_info_layout, '%TPE', label_font)
        self.RPD = self.addFormRow(tax_info_layout, '%RPD', label_font)
        self.FODEC = self.addFormRow(tax_info_layout, '%FODEC', label_font)

        # Add labels and line edits for Logistic Cost
        self.stamp = self.addFormRow(logistic_cost_layout, 'Stamp', label_font)
        self.air_percent_input = self.addFormRow(logistic_cost_layout, '%AIR', label_font)
        self.air_percent_input.setText(str(10))
        self.timber_input = self.addFormRow(logistic_cost_layout, 'Timber', label_font)
        self.fret = self.addFormRow(logistic_cost_layout, 'Freight', label_font)
        self.notice = self.addFormRow(logistic_cost_layout, 'Arrival Notice', label_font)
        self.storage = self.addFormRow(logistic_cost_layout, 'Storage', label_font)
        self.local = self.addFormRow(logistic_cost_layout, 'Local Transport', label_font)
        self.transite = self.addFormRow(logistic_cost_layout,"transite",label_font)

        # Add input fields for 'Retour de fond' section
        self.return_fund_controls = {}

        self.addReturnFundRow(return_fund_layout, 'Débarquement')
        self.addReturnFundRow(return_fund_layout, 'Dépottage')
        self.addReturnFundRow(return_fund_layout, 'Frais de gestion de dossier')
        self.addReturnFundRow(return_fund_layout, 'ISPS')
        self.addReturnFundRow(return_fund_layout, 'Avis et bas')
        self.addReturnFundRow(return_fund_layout, 'Scanner')

        # Initially disable the return fund section
        self.toggleReturnFundSection(Qt.Unchecked)

        # Add 'Calculate' and 'Load Data' buttons
        calculate_button = QPushButton('Calculer')
        load_data_button = QPushButton('Load Data')
        self.setupButtonStyle(calculate_button)
        self.setupButtonStyle(load_data_button)

        load_data_button.clicked.connect(self.loadinfo)
        calculate_button.clicked.connect(self.calcul)

        button_layout = QVBoxLayout()
        button_layout.addWidget(load_data_button)
        button_layout.addWidget(calculate_button)
        button_layout.setAlignment(Qt.AlignCenter)

        # Add horizontal spacing between buttons
        button_layout.addSpacing(10)
        button_group.setLayout(button_layout)

        # Set layouts for group boxes
        product_info_group.setLayout(product_info_layout)
        tax_info_group.setLayout(tax_info_layout)
        logistic_cost_group.setLayout(logistic_cost_layout)
        return_fund_group.setLayout(return_fund_layout)

        # Set a minimum height for group boxes
        product_info_group.setMinimumHeight(150)
        tax_info_group.setMinimumHeight(150)
        logistic_cost_group.setMinimumHeight(150)
        return_fund_group.setMinimumHeight(150)

        # Create horizontal layouts for pairing groups
        group_pair_1 = QHBoxLayout()
        group_pair_1.addWidget(product_info_group)
        group_pair_1.addWidget(tax_info_group)

        group_pair_2 = QHBoxLayout()
        group_pair_2.addWidget(logistic_cost_group)
        group_pair_2.addWidget(return_fund_group)

        # Add pairs to main layout
        main_layout.addLayout(group_pair_1)
        main_layout.addLayout(group_pair_2)
        main_layout.addWidget(button_group)

        # Create a scroll area to contain the main layout
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(QWidget())
        scroll_area.widget().setLayout(main_layout)

        # Set the scroll area as the central widget
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)

    def setupButtonStyle(self, button):
        button.setFixedWidth(200)
        button.setStyleSheet("""
        QPushButton {
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #0056b3;
            border: 1px solid #0056b3;
        }
        QPushButton:pressed {
            background-color: #004494;
        }
        """)

    def addFormRow(self, layout, label_text, font):
        label = QLabel(label_text)
        label.setFont(font)
        line_edit = QLineEdit()
        line_edit.setFixedWidth(200)
        line_edit.setPlaceholderText(f"Enter {label_text}")
        layout.addRow(label, line_edit)
        return line_edit  # Return the line_edit for further use

    def addReturnFundRow(self, layout, label_text):
        label = QLabel(label_text)
        line_edit = QLineEdit()
        line_edit.setFixedWidth(200)
        line_edit.setPlaceholderText(f"Enter {label_text}")
        line_edit.textChanged.connect(self.validateReturnFundInputs)  # Connect signal for validation
        self.return_fund_controls[label_text] = line_edit
        layout.addRow(label, line_edit)

    def validateReturnFundInputs(self):
        try:
            for control in self.return_fund_controls.values():
                if control.isEnabled() and control.text():
                    float(control.text())  # This will raise ValueError if not a valid float
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Please enter valid numbers in the return fund section')

    def toggleReturnFundSection(self, state):
        enable = state == Qt.Checked
        for control in self.return_fund_controls.values():
            control.setEnabled(enable)

    def toggleContainerCombo(self, state):
        enable = state == Qt.Unchecked
        self.container_combo.setEnabled(enable)
        self.container_number_input.setEnabled(enable)
        self.storage.setEnabled(False)
    def loadProductNames(self):
        products = self.session.query(Produits).all()
        self.product_combo.addItem('Select Product')
        for product in products:
            self.product_combo.addItem(product.name)

    def loadContainerNames(self):
        containers = self.session.query(Conteneur).all()
        self.container_combo.addItem('Select Container')
        for container in containers:
            self.container_combo.addItem(container.name)

    def calcul(self):
        try:
            # Get and validate input values
            unit_price = float(self.unit_price_edit.text())
            exchange_rate = float(self.taux.text())
            quantity = float(self.quantity.text())
            fret = float(self.fret.text())
            DD_rate = float(self.DD.text())
            FODEC_rate = float(self.FODEC.text())
            TPE_rate = float(self.TPE.text())
            TVA_rate = float(self.TVA.text())
            RPD_rate = float(self.RPD.text())
            timber = float(self.timber_input.text())
            AIR_rate = float(self.air_percent_input.text())
            stamp = float(self.stamp.text())
            notice = float(self.notice.text())
            local = float(self.local.text())
            poids = float(self.poids.text())
            storage = float(self.storage.text())

            # Print statements for debugging
            print("Unit price:", unit_price)
            print("Exchange rate:", exchange_rate)
            print("Quantity:", quantity)
            print("Fret:", fret)
            print("DD rate:", DD_rate)
            print("FODEC rate:", FODEC_rate)
            print("TPE rate:", TPE_rate)
            print("TVA rate:", TVA_rate)
            print("RPD rate:", RPD_rate)
            print("Timber:", timber)
            print("AIR rate:", AIR_rate)
            print("Stamp:", stamp)
            print("Notice:", notice)
            print("Local:", local)
            print("Poids:", poids)
            print("Storage:", storage)

            # Valeur EXW
            val_EXW = unit_price * exchange_rate * quantity
            print(f"Valeur EXW: {val_EXW}")

            # Calcule de FRET
            fret_calculated = exchange_rate * fret
            print(f"Fret: {fret_calculated}")

            # Assurance
            Assurance = (fret_calculated + val_EXW) * 0.0082

            # DD (Droits de Douane)
            DD = (Assurance + val_EXW + fret_calculated) * DD_rate * 0.01

            # FODEC
            fodec = (Assurance + val_EXW + fret_calculated + DD) * FODEC_rate * 0.01

            # TPE (Taxe Para-fiscale d’Exploitation)
            TPE = (Assurance + val_EXW + fret_calculated + DD + fodec) * TPE_rate * 0.01

            # TVA (Taxe sur la Valeur Ajoutée)
            TVA = (Assurance + val_EXW + fret_calculated + DD + fodec + TPE) * TVA_rate * 0.01

            # RPD (Redevance pour Développement)
            RPD = (fodec + TVA + TPE + DD) * RPD_rate * 0.01

            # AIR (Assurance Internationale des Risques)
            AIR = (Assurance + val_EXW + fret_calculated + DD + fodec + TPE + RPD + timber) * AIR_rate * 0.01

            # Frais Logistique
            frais_logistique = stamp + timber + fret + notice + local + poids * 0.103 + float(self.transite.text())
            print(f"Frais Logistique: {frais_logistique}")

            if self.groupage_checkbox.isChecked():
                # If groupage is checked, include return fund costs in the calculation
                Retour_de_fond = fret_calculated * 0.05

                # Additional print statements for debugging groupage-related inputs
                print("Groupage is checked")

                Débarquement = float(self.return_fund_controls['Débarquement'].text())
                print("Débarquement:", Débarquement)
                Dépotage = float(self.return_fund_controls['Dépottage'].text())
                print("Dépotage:", Dépotage)
                FGDD = float(self.return_fund_controls['Frais de gestion de dossier'].text())
                print("FGDD:", FGDD)
                isps = float(self.return_fund_controls['ISPS'].text())
                print("ISPS:", isps)
                bas = float(self.return_fund_controls['Avis et bas'].text())
                print("Avis et bas:", bas)
                scanner = float(self.return_fund_controls['Scanner'].text())
                print("Scanner:", scanner)


                # Update storage with return fund costs
                storage += Retour_de_fond + Débarquement + Dépotage + FGDD + isps + bas + scanner
                frais_logistique += storage
                total_cost = frais_logistique + val_EXW + fret_calculated + Assurance + DD + fodec + TPE + RPD + timber + AIR
                total_cost_per_unit = total_cost / quantity
            else:
                # If groupage is not checked, include container costs
                container_name = self.container_combo.currentText()
                print("Container name:", container_name)
                if container_name == 'Select Container':
                    QMessageBox.warning(self, 'Container Error', 'No container selected.')
                    return

                container = self.session.query(Conteneur).filter(
                    Conteneur.name == container_name).first()
                if container:
                    uc = int(self.container_number_input.text()) * container.prix + container.UC
                    frais_logistique += storage + uc
                else:
                    QMessageBox.warning(self, 'Container Error', 'Selected container not found')
                    return

            # Total Cost Calculation
            total_cost = frais_logistique + val_EXW + fret_calculated + Assurance + DD + fodec + TPE + RPD + timber + AIR
            total_cost_per_unit = total_cost / quantity

            print(f"Total Cost: {total_cost}")
            print(f"Total Cost per Unit: {total_cost_per_unit}")

            # Prepare the message with HTML styling and "DTN"
            message = (

                "<p><b>Unit price:</b> {unit_price:.2f} {devise}<br>"
                "<p><b>Exchange rate:</b> {exchange_rate:.2f} DTN<br>"
                "<p><b>Quantity:</b> {quantity:.2f} DTN<br>"
                "<p><b>Fret:</b> {fret:.2f} DTN<br>"
                "<p><b>DD rate:</b> {DD_rate:.2f} DTN<br>"
                "<p><b>FODEC rate:</b> {FODEC_rate:.2f} DTN<br>"
                "<p><b>TPE :</b> {TPE_rate:.2f} %<br>"
                "<p><b>TVA :</b> {TVA_rate:.2f} DTN<br>"
                "<p><b>RPD :</b> {RPD_rate:.2f} DTN<br>"
                "<p><b>Timber:</b> {timber:.2f} DTN<br>"
                "<p><b>AIR :</b> {AIR_rate:.2f} DTN<br>"
                "<p><b>Stamp:</b> {stamp:.2f} DTN<br>"
                "<p><b>Notice:</b> {notice:.2f} DTN<br>"
                "<p><b>Local:</b> {local:.2f} DTN<br>"
                "<p><b>Poids:</b> {poids:.2f} KG<br>"
                "<p><b>Storage:</b> {storage:.2f} DTN<br>"
                "<p><b>Valeur EXW:</b> {val_EXW:.2f} DTN<br>"
                "<p><b>Frais Logistique:</b> {frais_logistique:.2f} DTN<br>"
                "<p><b>Total Cost:</b> {total_cost:.2f} DTN<br>"
                "<p><b>Total Cost per Unit:</b> {total_cost_per_unit:.2f} DTN"
            ).format(
                unit_price=unit_price,
                devise=self.devise_input.text(),
                exchange_rate=exchange_rate,
                quantity=quantity,
                fret=fret_calculated,
                DD_rate=DD_rate,
                FODEC_rate=FODEC_rate,
                TPE_rate=TPE_rate,
                TVA_rate=TVA_rate,
                RPD_rate=RPD_rate,
                timber=timber,
                AIR_rate=AIR_rate,
                stamp=stamp,
                notice=notice,
                local=local,
                poids=poids,
                storage=storage,
                val_EXW=val_EXW,
                frais_logistique=frais_logistique,
                total_cost=total_cost,
                total_cost_per_unit=total_cost_per_unit -2.2
            )

            # Show results in a message box
            QMessageBox.information(self, 'Calculation Results', message)


        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Please enter valid numbers for all input fields')
        except Exception as e:
            QMessageBox.critical(self, 'Calculation Error', f'An error occurred during calculation: {e}')

    def loadinfo(self):
        print('Loading data...')
        prod_name = self.product_combo.currentText()
        if prod_name == 'Select Product':
            QMessageBox.warning(self, 'Warning', 'No product selected.')
            return

        try:
            # Query the product based on the selected name
            product = self.session.query(Produits).filter(Produits.name == prod_name).first()
            if product:
                self.devise_input.setText(product.devise)
                self.unit_price_edit.setText(str(product.prix_unitaire))

                # Load tax info
                tax_info = self.session.query(TaxInfo).filter(TaxInfo.product_id == product.id).first()
                if tax_info:
                    self.TVA.setText(str(tax_info.TVA))
                    self.DD.setText(str(tax_info.DD))
                    self.TPE.setText(str(tax_info.TPE))
                    self.RPD.setText(str(tax_info.RPD))
                    self.FODEC.setText(str(tax_info.FODEC))
                else:
                    # Clear tax info fields if no tax info is found
                    self.TVA.clear()
                    self.DD.clear()
                    self.TPE.clear()
                    self.RPD.clear()

                # Load exchange rate
                dev = self.session.query(Devise).filter(Devise.name == product.devise).first()
                if dev:
                    self.taux.setText(str(dev.taux_change))
                else:

                    self.taux.clear()
            else:
                QMessageBox.warning(self, 'Error', 'Product not found.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.exec_()
    sys.exit(app.exec_())
