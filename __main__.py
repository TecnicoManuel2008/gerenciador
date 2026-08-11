# importer les modules pour le programe
# importer le module flask pour le app-web

from flask import Flask, render_template, request, redirect

""" 
importer les modules personalise pour les traitements

:contact -> pour le traitement d'argent et du temps
:test_operation -> pour tester et eviter les errer cause par le user

c'est un application web que sert a gerer la caisse

"""
from traitement.contact import add_argent, retrait_argent, select_argent, listando
from traitement.contact import semaine, datetime, JOUR_SEMAINE, inicialiser
from traitement.test_operation import ControlerError


# cree un app flask
app = Flask(__name__)

# cree la page or rote initial du web
@app.route('/')
def index():
    inicialiser() 
    dados = select_argent()
    # inicialiser la page initial
    return render_template('index.html', dados=dados)


# Rota ajuntar dinheiro
@app.route('/ajoute', methods=["GET", "POST"])
def ajuntar():
    response = ""
    if request.method == "POST":
       type_argent = request.form.get('din')
       montant = abs(int(request.form.get('mont')))
       discription = str(request.form.get('libelle'))
       
       add_argent(
           date=datetime.now(), semaine=semaine[JOUR_SEMAINE.upper()], 
           type_money=type_argent, mont=montant, 
           operation=discription
       )
       
       response = "Operation faite avec sucess! "
    return render_template("paginas/ajuntar.html", data=select_argent(), response=response)


# Rote pour retirer de l'argent
@app.route('/retrait', methods=["GET", "POST"])
def retrait():
    response = ""
    test = ControlerError()
    
    if request.method == "POST":
        
       type_argent = request.form.get('din')
       montant = abs(int(request.form.get('mont')))
       discription = str(request.form.get('libelle'))
       
       if test.verifier_operation(mont=montant, type_mon=type_argent):
          if type_argent == "dolar":
              response = (f"Ce {montant}$ le Montant est tres eleve!", 0)
          else:
              response = (f"Ce {montant}FC est tres eleve!", 0)
       else:
          retrait_argent(
                  date=datetime.now(), semaine=semaine[JOUR_SEMAINE.upper()], 
                  type_money=type_argent, mont=montant, 
                  operation=discription
          )

          response = ("Operation faite avec sucess! ", 1)

    return render_template("paginas/retirar.html", data=select_argent(), response=response)


@app.route('/listing', methods=['GET'])
def listing():
    data = listando()
    tamanho = len(data)
    return render_template('paginas/listar.html', tabela=data, tam=tamanho)


@app.route('/return', methods=['GET', 'POST'])
def returne():
    return redirect("/")
    
# inicialozar conexao
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
    
    