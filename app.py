from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

dados_professores = {"professores": []}
dados_turmas = {"turmas": []}
dados_alunos = {"alunos": []}

id_professor = 1
id_turma = 1
id_aluno = 1

# ======================================== FUNÇÕES AUXILIARES ============================================================#

def validar_campos_obrigatorios(dados, campos_obrigatorios):
    campos_recebidos = set(dados.keys())
    campos_faltando = campos_obrigatorios - campos_recebidos
    campos_extras = campos_recebidos - campos_obrigatorios

    if campos_faltando:
        return {
            "erro": "Faltam campos obrigatórios",
            "campos_faltando": list(campos_faltando)
        }, 400

    if campos_extras:
        return {
            "erro": "Campos inválidos no JSON",
            "campos_invalidos": list(campos_extras)
        }, 400

    return None, 200

def calcular_idade(data_nascimento):
    today = datetime.today()
    nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
    idade = today.year - nascimento.year - ((today.month, today.day) < (nascimento.month, nascimento.day))
    return idade

def validar_data(data):
    try:
        return datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        return None

# ======================================== ROTAS PROFESSORES ============================================================#

@app.route('/professores', methods=['POST'])
def createProfessor():
    global id_professor

    dados = request.json
    campos_obrigatorios = {"nome", "data_nascimento", "disciplina", "salario", "observacoes"}

    erro, status = validar_campos_obrigatorios(dados, campos_obrigatorios)
    if erro:
        return jsonify(erro), status

    if not validar_data(dados["data_nascimento"]):
        return jsonify({"erro": "Formato de data inválido, use YYYY-MM-DD"}), 400

    dados["idade"] = calcular_idade(dados["data_nascimento"])
    dados["id"] = id_professor

    dados_professores["professores"].append(dados)
    id_professor += 1  # Só incrementa após adicionar

    return jsonify(dados), 201

@app.route('/professores/<int:id>', methods=['PUT'])
def updateProfessor(id):
    dados = request.json
    campos_permitidos = {"nome", "data_nascimento", "disciplina", "salario", "observacoes"}

    # Verifica se há campos inválidos
    campos_invalidos = [chave for chave in dados.keys() if chave not in campos_permitidos]
    
    # Verifica a tentativa de alterar ID ou idade
    if "id" in dados or "idade" in dados:
        return jsonify({"erro": "O ID e a idade do professor não podem ser alterados"}), 400

    # Verifica se existem campos inválidos
    if campos_invalidos:
        return jsonify({
            "erro": "Os seguintes campos não podem ser alterados",
            "campos_invalidos": campos_invalidos
        }), 400

    # Busca o professor para atualizar
    professor = next((p for p in dados_professores["professores"] if p["id"] == id), None)
    
    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404

    # Se a data de nascimento foi atualizada, recalcula a idade
    if "data_nascimento" in dados:
        nova_data_nascimento = dados["data_nascimento"]
        if not validar_data(nova_data_nascimento):
            return jsonify({"erro": "Formato de data inválido, use YYYY-MM-DD"}), 400
        
        dados["idade"] = calcular_idade(nova_data_nascimento)

    # Atualiza os dados do professor com os campos permitidos
    for chave, valor in dados.items():
        if chave in campos_permitidos:
            professor[chave] = valor

    return jsonify(professor), 200

@app.route('/professores', methods=['GET'])
def getProfessores():
    for professor in dados_professores["professores"]:
        professor["turmas"] = [
            turma for turma in dados_turmas["turmas"] if turma["professor_id"] == professor["id"]
        ]
    
    return jsonify(dados_professores["professores"])

@app.route('/professores/<int:id>', methods=['GET'])
def getProfessorById(id):
    professor = next((p for p in dados_professores["professores"] if p["id"] == id), None)
    return jsonify(professor) if professor else (jsonify({"error": "Professor não encontrado"}), 404)

@app.route('/professores/<int:id>', methods=['DELETE'])
def deleteProfessorById(id):
    professor = next((p for p in dados_professores["professores"] if p["id"] == id), None)
    if professor:
        dados_professores["professores"].remove(professor)
        return jsonify({"mensagem": "Professor removido"}), 200
    return jsonify({"erro": "Professor não encontrado"}), 404

# =========================================== ROTAS TURMAS ============================================================#

@app.route('/turmas', methods=['GET'])
def get_turmas():
    return jsonify(dados_turmas)

@app.route('/turmas/<int:turma_id>', methods=['GET'])
def get_turma_por_id(turma_id):
    turma = next((t for t in dados_turmas["turmas"] if t["id"] == turma_id), None)
    return jsonify(turma) if turma else (jsonify({"error": "Turma não encontrada"}), 404)

@app.route('/turmas', methods=['POST'])
def add_turma():
    global id_turma  

    nova_turma = request.get_json()
    if not nova_turma:
        return jsonify({"error": "Nenhum dado foi inserido"}), 400

    campos_obrigatorios = {'descricao', 'materia', 'turno', 'professor_id'}
    erro, status = validar_campos_obrigatorios(nova_turma, campos_obrigatorios)
    if erro:
        return jsonify(erro), status

    if not any(p["id"] == nova_turma["professor_id"] for p in dados_professores["professores"]):
        return jsonify({"error": "Professor com ID fornecido não encontrado"}), 404

    nova_turma_formatada = {
        "id": id_turma,
        "descricao": nova_turma["descricao"],
        "materia": nova_turma["materia"],
        "turno": nova_turma["turno"],
        "professor_id": nova_turma["professor_id"],
        "ativo": True  
    }

    dados_turmas["turmas"].append(nova_turma_formatada)
    id_turma += 1  

    return jsonify({"mensagem": "Nova turma adicionada!", "turma": nova_turma_formatada}), 201

@app.route('/turmas/<int:turma_id>', methods=['PUT'])
def update_turma(turma_id):
    dados = request.get_json()
    campos_permitidos = {'descricao', 'professor_id', 'ativo'}

    turma = next((t for t in dados_turmas["turmas"] if t['id'] == turma_id), None)
    if not turma:
        return jsonify({"error": "Turma não encontrada!"}), 404

    campos_invalidos = [chave for chave in dados.keys() if chave not in campos_permitidos]
    if campos_invalidos:
        return jsonify({"erro": "Campos inválidos", "campos_invalidos": campos_invalidos}), 400

    turma.update({chave: valor for chave, valor in dados.items() if chave in campos_permitidos})
    return jsonify(turma), 200

@app.route('/turmas/<int:turma_id>', methods=['DELETE'])
def delete_turma(turma_id):
    turma = next((t for t in dados_turmas["turmas"] if t['id'] == turma_id), None)
    if turma:
        dados_turmas["turmas"].remove(turma)
        return jsonify({"mensagem": "Turma removida com sucesso!"}), 200
    return jsonify({"error": "Turma não encontrada!"}), 404

# ========================================== EXECUÇÃO ============================================================#

if __name__ == "__main__":
    app.run(debug=True)
