# 
from flask import Flask, render_template, request, redirect

from traitement.contact import inserir_argent, retrait_argent, selection, listando
from traitement.contact import semaine, datetime, JOUR_SEMAINE

from traitement.test_operation import verifier_montant

# criar a app flask
app = Flask(__name__)

response = ""

# criar a pagina inicial
@app.route('/')
def index():
    dados = selection()
    return render_template('index.html', dados=dados)

# Rota ajuntar dinheiro
@app.route('/ajoute', methods=["GET", "POST"])
def ajuntar():
    if request.method == "POST":
        
       type_argent = request.form.get('din')
       montant = abs(int(request.form.get('mont')))
       discription = str(request.form.get('libelle'))
       inserir_argent(
       data=datetime.now(), 
       semaine=semaine[DIA_SEMAINE.upper()], 
       type_money=type_argent, 
       mont=montant, 
       operation=discription)
       response = "Operacao feita com sucesso! "
       
    return render_template("paginas/ajuntar.html", data=selection(), response=response)

# Rote pour retirer de l'argent
@app.route('/retrait', methods=["GET", "POST"])
def retrait():
    if request.method == "POST":
        
       type_argent = request.form.get('din')
       montant = abs(int(request.form.get('mont')))
       discription = str(request.form.get('libelle'))
       if verifier_montant(mont=montant, type_mon=type_argent):
          if type_argent == "dolar":response = (f"C\'est {montant}$ le Montant est tres eleve!", 0)
          else: response = (f"C\'est {montant}FC est tres eleve!", 0)
       else:
          retrait_argent(
          data=datetime.now(), 
          semaine=semaine[DIA_SEMAINE.upper()], 
          type_money=type_argent, 
          mont=montant, 
          operation=discription)
          reponse = ("Operacao feita com sucesso! ", 1)

    return render_template("paginas/retirar.html", data=selection(), response=response)

@app.route('/listing/<int:id>', methods=["GET"])
@app.route('/listing', methods=['GET'])
def listing(): 
    data = listando()
    tam = len(data)
    return render_template('paginas/listar.html', tabela=data, tam=tam)

@app.route('/return', methods=['GET', 'POST'])
def returne():
    return redirect("/")
    
# inicialozar conexao
if __name__ == '__main__':
    app.run(debug=True)
    
    