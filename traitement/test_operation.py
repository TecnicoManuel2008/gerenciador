from traitement.entidades import Caisse, Argent

from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

from rich.traceback import install

install()
class Controller:
    def __init__(self):
        # cree une connexion avec le address du base de donne
        self.__engine = create_engine("sqlite:///Gerencia.db")
        # class creater des tables en class(ORM)
        self.__base = declarative_base()
        # Cree un createur des Sessions
        self.__Session = sessionmaker(self.__engine)
    
    # Cree les methodes acessibles
    @property
    def MainSession(self: object) -> object:
        return self.__Session
    @MainSession.setter
    def MainSession(self: object, valeur: str) -> None:
        raise PermissionError('Error: tu n\'as pas la permission ! ')
        
    @property
    def Engine(self: object) -> object:
        return self.__engine
    @Engine.setter
    def Engine(self, valeur: str) -> None:
        raise PermissionError('Error: tu n\'as pas la permission ! ')
    
    @property
    def Base(self):
        return self.__base
    @Base.setter
    def Base(self: object, valeur: str) -> None:
        raise PermissionError('Error: tu n\'as pas la permission ! ')
        
        
    def __select__(self) -> object:
        """ cette fonction sert a retourner la liste des operations
        que sont dans la caisse
        """
        with self.__Session() as session:
            database = session.query(Caisse).all()
            return database
        
    def verifier_operation(self: object, mont: int, type_mon: str) -> bool:
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
           return True if mont > donnee[-1].francs else False
            
    def ilya_argent_sur_caisse(self: object) -> bool:
        """ 
        Cette fonction teste si il a argent et si il a deja
        une premiere operation dans le banque
        """
        return False if len(self.__select__()) == 0 else True
  