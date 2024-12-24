from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

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


# Create a database connection
engine = create_engine('sqlite:///your_database.db')  # Update the database URL as necessary
Base.metadata.create_all(engine)  # Create all tables

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Populate the Devise table
eur = Devise(name='Euro', taux_change=1.1)
tnd = Devise(name='Tunisian Dinar', taux_change=0.3)

# Populate the Unites table
kg = Unites(name='Kilogram')
l = Unites(name='Liter')

# Populate the Fournisseurs table with realistic suppliers
supplier1 = Fournisseurs(name='Coca-Cola Company', Adresse_de_siege='1 Coca-Cola Plaza, Atlanta, GA, USA',
                         Adresse_de_usine='Weybridge, UK', devise='Euro', modalite_paiment='Bank Transfer')
supplier2 = Fournisseurs(name='Nestlé S.A.', Adresse_de_siege='Avenue Nestlé 55, Vevey, Switzerland',
                         Adresse_de_usine='Moscow, Russia', devise='Tunisian Dinar', modalite_paiment='Credit')
supplier3 = Fournisseurs(name='PepsiCo, Inc.', Adresse_de_siege='700 Anderson Hill Road, Purchase, NY, USA',
                         Adresse_de_usine='Lima, Peru', devise='Euro', modalite_paiment='Bank Transfer')
supplier4 = Fournisseurs(name='Mondelez International', Adresse_de_siege='Three Parkway North, Deerfield, IL, USA',
                         Adresse_de_usine='Mexico City, Mexico', devise='Tunisian Dinar', modalite_paiment='Cash')

# Populate the Emballage table with realistic packaging types
packaging1 = Emballage(type_emballage='Plastic Bottle')
packaging2 = Emballage(type_emballage='Glass Jar')
packaging3 = Emballage(type_emballage='Cardboard Box')
packaging4 = Emballage(type_emballage='Tin Can')

# Populate the Autorisation table with realistic authorizations
authorization1 = Autorisation(designation='Health and Safety Authorization', ministere='Ministry of Health')
authorization2 = Autorisation(designation='Food Safety Certification', ministere='Ministry of Agriculture')

# Populate the PositionnTarifaire table with realistic tariff positions
tariff_position1 = PositionnTarifaire(HS_code=220210, designation='Soft Drinks', droits_taxe='5%', autorisation='Health and Safety Authorization')
tariff_position2 = PositionnTarifaire(HS_code=210690, designation='Food Preparations', droits_taxe='10%', autorisation='Food Safety Certification')

# Populate the ClasseDanger table with realistic hazard classes
danger_class1 = ClasseDanger(UN='UN2000', classe=1)  # Example UN number and class
danger_class2 = ClasseDanger(UN='UN3000', classe=2)

# Populate the Convention table with realistic trade conventions
trade_convention1 = Convention(name='EU Trade Agreement', dd=0.5)
trade_convention2 = Convention(name='Tunisian Export Convention', dd=1.0)

# Populate the Incoterm table with additional realistic Incoterms
incoterm1 = Incoterm(name='CIF')  # Cost, Insurance, and Freight
incoterm2 = Incoterm(name='FOB')  # Free on Board
incoterm3 = Incoterm(name='EXW')  # Ex Works
incoterm4 = Incoterm(name='DDP')  # Delivered Duty Paid
incoterm5 = Incoterm(name='DAP')  # Delivered at Place
incoterm6 = Incoterm(name='FAS')  # Free Alongside Ship

# Populate the ModalitePaiment table with realistic payment modalities
payment_modality1 = ModalitePaiment(name='Cash on Delivery')
payment_modality2 = ModalitePaiment(name='Letter of Credit')

# Populate the Conteneur table with realistic container information
container1 = Conteneur(name='20 ft Standard Container', prix=2500.0, devise='Euro', volume=33.0, UC=1.0)
container2 = Conteneur(name='40 ft High Cube Container', prix=3000.0, devise='Tunisian Dinar', volume=67.0, UC=2.0)

# Populate the Origin table with realistic origins
origin1 = Origin(name='Tunisia')
origin2 = Origin(name='Italy')
origin3 = Origin(name='USA')
origin4 = Origin(name='Switzerland')

# Populate the TaxInfo table with realistic tax information
tax_info1 = TaxInfo(TVA=19.0, FODEC=5.0, DD=2.0, TPE=3.0, RPD=1.0)
tax_info2 = TaxInfo(TVA=20.0, FODEC=4.0, DD=1.5, TPE=2.5, RPD=1.2)

# Populate the MsdsTech table with realistic MSDS and technical documents
msds_tech1 = MsdsTech(msds=b'Sample MSDS for Coca-Cola', tech=b'Sample Tech Data for Coca-Cola')
msds_tech2 = MsdsTech(msds=b'Sample MSDS for ', tech=b'Sample Tech Data for ')

# Populate the Produits table with realistic products
product1 = Produits(
    name='Coca-Cola Classic',
    unite='Liter',
    colisage='12',
    devise='Euro',
    prix_unitaire=0.80,
    fournisseur='Coca-Cola Company',
    lieu_enlevement='Atlanta, GA, USA',
    autorisation='Health and Safety Authorization',
    EUR1=True,
    Incoterm='CIF',
    pelletisation=False,
    libre=True,
    Convention_de_commerce='EU Trade Agreement',
    origine='USA',
    danger_class='1',
    code=1001,
    prix_revient=0.50
)

product2 = Produits(
    name='Nestlé Chocolate',
    unite='Kilogram',
    colisage='6',
    devise='Tunisian Dinar',
    prix_unitaire=3.00,
    fournisseur='Nestlé S.A.',
    lieu_enlevement='Vevey, Switzerland',
    autorisation='Food Safety Certification',
    EUR1=False,
    Incoterm='FOB',
    pelletisation=True,
    libre=False,
    Convention_de_commerce='Tunisian Export Convention',
    origine='Switzerland',
    danger_class='2',
    code=1002,
    prix_revient=2.00
)

product3 = Produits(
    name='Pepsi-Cola',
    unite='Liter',
    colisage='12',
    devise='Euro',
    prix_unitaire=0.75,
    fournisseur='PepsiCo, Inc.',
    lieu_enlevement='Purchase, NY, USA',
    autorisation='Health and Safety Authorization',
    EUR1=True,
    Incoterm='EXW',
    pelletisation=False,
    libre=True,
    Convention_de_commerce='EU Trade Agreement',
    origine='USA',
    danger_class='1',
    code=1003,
    prix_revient=0.45
)

product4 = Produits(
    name='Oreo Cookies',
    unite='Kilogram',
    colisage='12',
    devise='Tunisian Dinar',
    prix_unitaire=2.50,
    fournisseur='Mondelez International',
    lieu_enlevement='Deerfield, IL, USA',
    autorisation='Food Safety Certification',
    EUR1=False,
    Incoterm='DAP',
    pelletisation=True,
    libre=False,
    Convention_de_commerce='Tunisian Export Convention',
    origine='USA',
    danger_class='2',
    code=1004,
    prix_revient=1.50
)

product5 = Produits(
    name='Nestlé Nido Milk Powder',
    unite='Kilogram',
    colisage='6',
    devise='Euro',
    prix_unitaire=4.00,
    fournisseur='Nestlé S.A.',
    lieu_enlevement='Vevey, Switzerland',
    autorisation='Food Safety Certification',
    EUR1=True,
    Incoterm='DDP',
    pelletisation=False,
    libre=True,
    Convention_de_commerce='EU Trade Agreement',
    origine='Switzerland',
    danger_class='1',
    code=1005,
    prix_revient=3.00
)

# Add records to the session
session.add_all([
    eur, tnd, kg, l,
    supplier1, supplier2, supplier3, supplier4,
    packaging1, packaging2, packaging3, packaging4,
    authorization1, authorization2,
    tariff_position1, tariff_position2,
    danger_class1, danger_class2,
    trade_convention1, trade_convention2,
    incoterm1, incoterm2, incoterm3, incoterm4, incoterm5, incoterm6,
    payment_modality1, payment_modality2,
    container1, container2,
    origin1, origin2, origin3, origin4,
    tax_info1, tax_info2,
    msds_tech1, msds_tech2,
    product1, product2, product3, product4, product5
])

# Commit the session to save the records in the database
session.commit()

# Close the session
session.close()
