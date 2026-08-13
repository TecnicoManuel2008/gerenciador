""" 
Cet programme sert a faire un API qui 
permet de faire les conctacte entre le les rotes et les bases
"""
from traitement.entidades import Caisse, Argent, engine

from traitement.test_operation import ControlerError
from datetime import date, datetime

from rich import print
# LES CONSTANTS DES TEMPS

# prendre le jour actuel en format: DH-MH-AH
JOUR_ACTUEL = datetime.now()
# prendre le jour de la samine en: anglais
JOUR_SEMAINE = JOUR_ACTUEL.strftime("%A")
#cree un dicionaire en traduisant les jour de la semaine
semaine = {
    "SUNDAY" : "DIMANCHE", "MONDAY": "LUNDI",
    "TUESDAY": "MARDI", "WEDNESDAY": "MERCREDI",
    "THUESDAY": "JEUDI","FRIDAY": "VENDREDI",
    "SATURDAY": "SAMEDI"
}
# cree une fonction lambda que retorne le jour de la semaine en francais
semaine_act = lambda: semaine[JOUR_SEMAINE.upper()]
# instancier le controler des Errers
cfg = ControlerError()


def inicialiser() -> None:
    """ 
    Cette fonction sert uniquement a inicialiser la valeur
    dans le base de donne avec des valeurs nulles
    elle teste s'il a argent ou operation dans le 
    base de donne sinon il vas inicialiser avec 0-0 ou
    des valeurs nulles
    """
    
    # instancier la Session des operations
    session = cfg.MainSession()
    
    try:
        # si il y a pas d'argent sur la caisse
        if not cfg.ilya_argent_sur_caisse():
            # adicioner des valeur nulle sur les tables
            dt = Caisse(date=datetime.now(), semaine=semaine_act(), description="inicial", dolar=0, francs=0)
            dr = Argent(dolar=0, francs=0)
            
            # adicioner les object 
            session.add(dt)
            session.add(dr)
            
            # actualiser les operations
            session.commit()
            
    except Exception as ex:
        print(ex)
    finally:
        session.close()
        
# POST
def add_argent(date: str, mont: int,  semaine: str, type_money: str, operation: str) -> None:
    """ Cette Fonction sert uniquement a adicioner de l'argent
    à la base de donne : Caisse(ORM) et Argent(ORM) 
                    arguments:
                        
    :date/<str> -> c'est la date numérique actuel ex: 2026-04-15
    :mont/<int> -> c'est le montant d'argent
    :semaine/<str> -> c'est le jour de la semaine ex: Mardi, Mercredi, etc
    :type_money/<str> -> c'est le type d'argent (franc ou dolar)
    :opération/<str> -> c'est la description  de la operation
    
    Et cette fonction retourn  None
     """
    # inicializar la session
    with cfg.MainSession() as session:
            # faire un requete sur la table Caisse(ORM)
            # et filter tout les donnee
            query = session.query(Caisse).all()
            # calculer les dolar et les Francs 
            dolar = query[-1].dolar + mont
            franc = query[-1].francs + mont
                        
            # actualiser la table Caisse(ORM)
            into = Caisse(
               date = date,
               semaine = semaine,
               dolar = query[-1].dolar if type_money == "francs" else dolar,
               francs = query[-1].francs if type_money == "dolar" else franc,
               description = operation
            )
            # actualiser la table Argent(ORM)
            args = session.query(Argent).all()
            dt = Argent(
                dolar = args[-1].dolar if type_money == 'francs' else dolar,
                francs = args[-1].francs if type_money == "dolar" else franc
            )
            # adicionar les object dans la session
            session.add(dt)
            session.add(into)
            # mettre a jour les operation
            session.commit()
            
# GET
def retrait_argent(date: str, mont: int, semaine: str, type_money: str, operation: str) -> None:
    """Cette Fonction sert uniquement a retirer de l'argent
    à la base de donne : Caisse(ORM) et Argent(ORM) 
                    arguments:
                        
    :date/<str> -> c'est la date numérique actuel ex: 2026-04-15
    :mont/<int> -> c'est le montant d'argent
    :semaine/<str> -> c'est le jour de la semaine ex: Mardi, Mercredi, etc
    :type_money/<str> -> c'est le type d'argent (franc ou dolar)
    :opération/<str> -> c'est la description  de la operation
    
    Et cette fonction retiurn : None"""
    # commencer la session sur cet operation
    with cfg.MainSession() as session:
         # faire un requete sur la table Caisse(ORM)
         # et filter tout les donnee
        query = session.query(Caisse).all()
        # calculer les dolar et les Francs 
        dolar = int(query[-1].dolar) - mont
        franc = int(query[-1].francs) - mont
         # actualiser la table Caisse(ORM)
        into = Caisse(
               date = date, 
               semaine = semaine,
               dolar = query[-1].dolar if type_money == "francs" else dolar,
               francs = query[-1].francs if type_money == "dolar" else franc,
               description = operation
        )
        args = session.query(Argent).all()
        # actualiser la table Argent(ORM)
        dt = Argent(
            dolar = args[-1].dolar if type_money == 'francs' else dolar,
            francs = args[-1].francs if type_money == "dolar" else franc
        )
        # adicionar les object dans la session
        session.add(dt)
        session.add(into)
        # mettre a jour les operation
        session.commit()
            
def select_argent() -> dict:
    """ """
    #commencer la session sur cet operation
    with cfg.MainSession() as session:
        # prendre tous les donnes dans le base de donne
        dados = session.query(Argent).all()
        # si la base de donne est vide
        # retourne 0 au FrontEnd
        if len(dados) == 0: 
            # Retourne dolar=0, francs=0
            return {
                 "Dolar": 0,
                 "Francs": 0
            }
        else:
            # Sinon retourne les effectives valeurs de dolar et francs
           return {
                 "Dolar": dados[-1].dolar,
                 "Francs": dados[-1].francs
            }
    
def select_by_index(idx: int) -> list | str:
    """ """
    with cfg.MainSession() as session:
        
        dados = session.query(Caisse).all()
        if idx > len(dados):
            return "ID fora do registro"
            
        if len(dados) == 0:
            return [c-c for c in range(0, 6)]
            
        else:
            return [
                dados[idx-1].id, 
                dados[idx-1].date, 
                dados[idx-1].semaine, 
                dados[idx-1].dolar, 
                dados[idx-1].francs, 
                dados[idx-1].description, 
            ]

def listando() -> object:
    """ """
    with cfg.MainSession() as session:
        data = session.query(Caisse).all()
        return data
        
        
        