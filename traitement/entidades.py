from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData, Table

# criar o motor do banco de dados
engine = create_engine("mysql+pymysql://root:SuaNovaSenha123@localhost:3306/Gerencia")
metadata = MetaData()

base = declarative_base()

# utilisar a tabela do banco
class Caisse(base):
    __table__ = Table("Caixa", metadata, autoload_with=engine)
    