from flask import Flask, jsonify, request

app = Flask(__name__)

dici = {"professores":[{ }]}

id_professor = 1

@app.route('/professores', methods=['POST'])

def validar_campos_obrigatorios(dados, campos_obrigatorios):
    if not campos_obrigatorios.isubset(dados.keys()):
        return {"erro": "Faltam campos obrigatórios!"}, 400 #Verificação = campos obrigatório faltando
    if set(dados.keys()) != campos_obrigatorios:
        return {"erro": "Campos inválidos no JSON!"}, 400 # Verificação = os campos
                                                          # são diferentes dos obrigatórios ou a mais
    return None, 200 #verificação = OK

def createProfessor():
    global id_professor
    dados = request.json
    campos_obrigatórios = {"nome", "data_nascimento", "disciplina", "salario", "observacoes"}
     
    erro, status = validar_campos_obrigatorios(dados, campos_obrigatórios)
    if erro:
        return jsonify(erro), status
    
    for professor in dici["professores"]:
        if professor["id"] == dados["id"]:
            return jsonify({"erro": "ID de professor já está cadastrado!"}), 400
        
    dados["id"] = id_professor

    id_professor += 1

    dici["professores"].append(dados)
    return jsonify(dados), 201


if __name__ == "__main__":
    app.run(debug=True)