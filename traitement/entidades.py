""" 
 Ce programme sert uniquement a definir
 les tables de la base de donnee avec 
 le concepte d'ORM (Object Relational Mapping)
 en utilisant le :SQLALCHEMY
     
 :sqlalchemy.orm -> pour la heritage des declarative_base
 :sqlalchemy -> pour les colunes, motor
     
 ce programme utilise 2 tables (classes) avec
 ORM (object Relational Mapping)
"""

from sqlalchemy.orm import  declarative_base
from sqlalchemy import create_engine

from sqlalchemy import Integer, String, Date, Column, Text

# cree une connexion avec le address du base de donne
engine = create_engine("sqlite:///Gerencia.db")
# class creater des tables en class(ORM)
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
    print(f"Errer: < {ex} >")
    