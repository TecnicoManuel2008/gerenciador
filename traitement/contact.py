from traitement.entidades import Caisse, engine
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime

JOUR_ACTUEL = datetime.now()
JOUR_SEMAINE = JOUR_ACTUEL.strftime("%A")

semaine = {
    "SUNDAY" : "DIMANCHE", "MONDAY": "LUNDI",
    "TUESDAY": "MARDI", "WEDNASDAY": "MERCREDI",
    "THUESDAY": "JEUDI","FRIDAY": "VENDREDI",
    "SATURDAY": "SAMEDI"
}
# configuarar a conexao do banco de dados
Session = sessionmaker(engine)

def inserir_argent(data, mont, semaine, type_money, operation):
    with Session() as session:
        query = session.query(Caisse).all()
        
        dolar = query[-1].dolar + mont
        franc = query[-1].francs + mont
        
        if type_money == "dolar":
            into = Caisse(
                data=data,semana=semaine,
                        dolar=dolar,francs=query[-1].francs,
                        dinscription=operation)
        elif type_money == "francs":
             into = Caisse(
                        data=data, semana=semaine,
                        dolar=query[-1].dolar, francs=franc,
                        dinscription=operation)
        session.add(into)
        session.commit()

def retrait_argent(data, mont, semaine, type_money, operation):
    with Session() as session:
        query = session.query(Caisse).all()
        
        dolar = int(query[-1].dolar) - mont
        franc = int(query[-1].francs) - mont

        if type_money == "dolar":
            into = Caisse(
                        data=data,semana=semaine,
                        dolar=dolar,francs=query[-1].francs,
                        dinscription=operation)
        elif type_money == "francs":
             into = Caisse(
                        data=data, semana=semaine,
                        dolar=query[-1].dolar, francs=franc,
                        dinscription=operation)
                        
        session.add(into)
        session.commit()
            
def selection():
    with Session() as session:
        dados = session.query(Caisse).all()
        return {
             "Dolar":dados[-1].dolar,
             "Francs": dados[-1].francs,
        }
    
def select_by_index(idx: int) -> list or str:
    with Session() as session:
        dados = session.query(Caisse).all()
        if idx > len(dados):
            return "ID fora do registro"
        return [
            dados[idx-1].id, dados[idx-1].data, 
            dados[idx-1].semana, dados[idx-1].dolar, 
            dados[idx-1].francs, dados[idx-1].dinscription, 
        ]
        
def listando():
    with Session() as session:
        data = session.query(Caisse).all()
        return data
        
            
            
             
            
        
        