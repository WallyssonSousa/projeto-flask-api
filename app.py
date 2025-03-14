from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

dici = {"professores":[]}

id_professor = 1


def validar_campos_obrigatorios(dados, campos_obrigatorios):
    if not campos_obrigatorios.issubset(dados.keys()):
        return {"erro": "Faltam campos obrigatórios!"}, 400 #Verificação = campos obrigatório faltando
    if set(dados.keys()) != campos_obrigatorios:
        return {"erro": "Campos inválidos no JSON!"}, 400 # Verificação = os campos
                                                          # são diferentes dos obrigatórios ou a mais
    return None, 200 #verificação = OK

def calcular_idade(data_nascimento):
    today = datetime.today()
    nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
    idade = today.year - nascimento.year -((today.month, today.day)<(nascimento.month, nascimento.day))
    return idade


@app.route('/professores', methods=['POST'])
def createProfessor():
    global id_professor
    dados = request.json
    campos_obrigatórios = {"nome", "data_nascimento", "disciplina", "salario", "observacoes"}
     
    erro, status = validar_campos_obrigatorios(dados, campos_obrigatórios)
    if erro:
        return jsonify(erro), status
    
    dados["idade"] = calcular_idade(dados["data_nascimento"])

    dados["id"] = id_professor
    
    for professor in dici["professores"]:
        if professor["id"] == dados["id"]:
            return jsonify({"erro": "ID de professor já está cadastrado!"}), 400
        
    id_professor += 1

    dici["professores"].append(dados)
    
    return jsonify(dados), 201

@app.route('/professores', methods=['GET'])
def getProfessores():
    return jsonify(dici["professores"])


if __name__ == "__main__":
    app.run(debug=True)