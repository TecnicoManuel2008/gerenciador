from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine

from sqlalchemy import ForeignKey, Integer, String, Date, Column, Text

# criar o motor do banco de dados
engine = create_engine("sqlite:///Gerencia.db")
base = declarative_base()

# cree une nouvelle table sur le DataBase
class Caisse(base):
    __tablename__ = "Caisse"
    
    # definir les colunes de la table
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    date = Column(Date, nullable=False)
    semaine = Column(String(50), nullable=False)
    dolar = Column(Integer, nullable=False)
    francs = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)


class Argent(base):
    __tablename__ = "Argent"
    
    # definir les colunes de la table
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    dolar = Column(Integer, nullable=False)
    francs = Column(Integer, nullable=False)


# essaye d'eviter des erreurs
try:
    # cree les tables dans le base
    base.metadata.create_all(engine)
except Exception as ex:
    print(ex)
    