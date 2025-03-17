from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulação de banco de dados
alunos = []

# ------------------- ALUNOS -------------------

# Rota de listagem de alunos
@app.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(alunos), 200

# Rota de detalhes do aluno
@app.route('/alunos/<int:idAluno>', methods=['GET'])
def get_aluno(idAluno):
    aluno = next((a for a in alunos if a['id'] == idAluno), None)
    if aluno:
        return jsonify(aluno), 200
    return jsonify({"error": "Aluno não encontrado!"}), 404

# Rota de criação de aluno
@app.route('/alunos', methods=['POST'])
def add_aluno():
    data = request.json
    if not data or 'id' not in data or 'nome' not in data:
        return jsonify({"error": "Dados inválidos!"}), 400
    
    # Verifica se já existe um aluno com esse ID
    if any(aluno['id'] == data['id'] for aluno in alunos):
        return jsonify({"error": "ID já cadastrado!"}), 400

    alunos.append(data)
    return jsonify({"message": "Aluno adicionado!"}), 201

# Rota de atualização de aluno
@app.route('/alunos/<int:idAluno>', methods=['PUT'])
def update_aluno(idAluno):
    data = request.json
    for aluno in alunos:
        if aluno['id'] == idAluno:
            aluno.update(data)
            return jsonify({"message": "Aluno atualizado!"}), 200
    return jsonify({"error": "Aluno não encontrado!"}), 404

# Rota de deletar aluno
@app.route('/alunos/<int:idAluno>', methods=['DELETE'])
def delete_aluno(idAluno):
    global alunos
    alunos = [aluno for aluno in alunos if aluno['id'] != idAluno]
    return jsonify({"message": "Aluno removido!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
