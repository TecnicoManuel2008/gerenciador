from traitement.entidades import Caisse, engine
from sqlalchemy.orm import sessionmaker

class ControlerError:
    def __init__(self):
        self.__Session = sessionmaker(engine)
    
    @property
    def MainSession(self: object) -> object:
        return self.__Session
    
    def __select__(self: object) -> object:
        """ cette fonction sert a retourner la liste des operations
        que sont dans la caisse
        """
        with self.__Session() as session:
            database = session.query(Caisse).all()
            return database
        
    def verifier_operation(self, mont: int, type_mon: str) -> bool:
        """ 
        Cette function teste si le montant de la retrait 
        suffie pour la retrait
        
        si le montant suffie : return true
        si non : return false
        """
        donnee = self.__select__()
        if type_mon == "dolar":
            return True if mont > donnee[-1].dolar else False
        else:
            return True if mont > donnee[-1].franc else False
            
    def ilya_argent_sur_caisse(self: object) -> bool:
        """ 
        Cette fonction teste si il a argent et si il a deja
        une premiere operation dans le banque
        """
        return False if len(self.__select__()) == 0 else True
            
            

        