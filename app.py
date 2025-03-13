from flask import Flask, jsonify, request

app = Flask(__name__)

dici = {
    "professores":[
        {   "id" : 1,
            "nome" : "Caio Ireno",
            "idade" : 27,
            "materia" : "String",
            "observacoes" : "String"
            }
    ]
}

@app.route('/professores', methods=['GET'])
def getProfessor():
    dados = dici["professores"] 
    return jsonify(dados)

@app.route('/professores', methods=['POST'])
def createProfessor():
    dados = request.json
    professor = dici['professores']
    professor.append(dados)
    return jsonify(dados)

@app.route('/professores/<int:idProfessor>', methods=['PUT'])
def updateProfessor(idProfessor):
    professores = dici['professores']
    for professor in professores:
        if professor['id'] == idProfessor:
            r = request.json
            professor['nome'] = r['nome']
            return jsonify(r),201
        

if __name__ == "__main__":
    app.run(debug=True)