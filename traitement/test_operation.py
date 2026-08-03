from traitement.entidades import Caisse, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(engine)

def verifier_montant(mont: int, type_mon: str) -> bool:
    
    with Session() as session:
        donnee = session.query(Caisse.dolar, Caisse.francs).all()
        if type_mon == "dolar":
            return True if mont > donnee[-1].dolar else False
        else:
            return True if mont > donnee[-1].dolar else False
            

