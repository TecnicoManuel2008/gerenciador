from traitement.entidades import Caisse, Argent, engine

from traitement.test_operation import ControlerError
from datetime import date, datetime

# LES CONSTANTS
JOUR_ACTUEL = datetime.now()
JOUR_SEMAINE = JOUR_ACTUEL.strftime("%A")

semaine = {
    "SUNDAY" : "DIMANCHE", "MONDAY": "LUNDI",
    "TUESDAY": "MARDI", "WEDNESDAY": "MERCREDI",
    "THUESDAY": "JEUDI","FRIDAY": "VENDREDI",
    "SATURDAY": "SAMEDI"
}

semaine_act = lambda: semaine[JOUR_SEMAINE.upper()]
    
# instancier le controler des Errers
cfg = ControlerError()

def inicialiser():
    session = cfg.MainSession()
    try:
        if not cfg.ilya_argent_sur_caisse():
            dt = Caisse(date=datetime.now(), semaine=semaine_act(), description="inicial", dolar=0, francs=0)
            dr = Argent(dolar=0, francs=0)
            
            session.add(dt)
            session.add(dr)
            
            session.commit()
            
    except Exception as ex: 
        print(ex)
    finally:
        session.close()


    
def add_argent(date: str, mont: int,  semaine: str, type_money: str, operation: str) -> None:
    with cfg.MainSession() as session:
            
            query = session.query(Caisse).all()
            dolar = query[-1].dolar + mont
            franc = query[-1].francs + mont
                        
            into = Caisse(
               date=date, 
               semaine=semaine,
               dolar=query[-1].dolar if type_money == "francs" else dolar,
               francs=query[-1].francs if type_money == "dolar" else franc,
               description=operation
            )
            args = session.query(Argent).all()
            dt = Argent(
                dolar= args[-1].dolar if type_money == 'francs' else dolar,
                francs=args[-1].francs if type_money == "dolar" else franc
            )
        
            session.add(dt)
            session.add(into)
            session.commit()
            
            
def retrait_argent(date: str, mont: int, semaine: str, type_money: str, operation: str) -> None:
    with cfg.MainSession() as session:
        
        query = session.query(Caisse).all()
        dolar = int(query[-1].dolar) - mont
        franc = int(query[-1].francs) - mont
        
        into = Caisse(
               date=date, 
               semaine=semaine,
               dolar=query[-1].dolar if type_money == "francs" else dolar,
               francs=query[-1].francs if type_money == "dolar" else franc,
               description=operation
        )
        args = session.query(Argent).all()
        dt = Argent(
            dolar= args[-1].dolar if type_money == 'francs' else dolar,
            francs=args[-1].francs if type_money == "dolar" else franc
        )
        session.add(dt)
        session.add(into)
        
        session.commit()
            
            
            
def select_argent() -> dict:
    with cfg.MainSession() as session:
        
        dados = session.query(Argent).all()
        
        if len(dados) == 0: 
            return {
                 "Dolar": 0,
                 "Francs": 0
            }
        else: 
           return {
                 "Dolar": dados[-1].dolar,
                 "Francs": dados[-1].francs
            }
    
def select_by_index(idx: int) -> list or str:
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
    with cfg.MainSession() as session:
        data = session.query(Caisse).all()
        return data
        
        
        