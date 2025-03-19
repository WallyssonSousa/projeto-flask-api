from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

dados_professores = {"professores":[]}
dados_turmas = {"turmas": []}
dados_alunos = {"alunos": []}

id_professor = 1 # Contador para incrementação automatica do id_professor

#FUNÇÕES A PARTE ⬇️

# Função para verificar campos obrigatórios
def validar_campos_obrigatorios(dados, campos_obrigatorios):

    campos_recebidos = set(dados.keys())
    campos_faltando = campos_obrigatorios - campos_recebidos
    campos_extras = campos_recebidos - campos_obrigatorios
    
    if campos_faltando:
        return {                            
            "erro": "Faltam campos obrigatórios",   
            "campos_faltando": list(campos_faltando)
        }, 400 # verificação de campos faltando                       
        
    if campos_extras:
        return {
            "erro": "Campos inválidos no JSON",
            "campos_invalidos": list(campos_extras)
        }, 400 #verificação de campos extras
        
    return None, 200 #verificação OK

#função para calcular idade automaticamente
def calcular_idade(data_nascimento):
    today = datetime.today()
    nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
    idade = today.year - nascimento.year -((today.month, today.day)<(nascimento.month, nascimento.day))
    return idade

# Função para validar formato YYYY-MM-DD
def validar_data(data):
    try:
        return datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        return None
    
# ======================================== ROTAS⬇️ =====================================================================#

@app.route('/professores', methods=['POST'])
def createProfessor():
    global id_professor # Puxa o contador global

    dados = request.json

    campos_obrigatórios = {"nome", "data_nascimento", "disciplina", "salario", "observacoes"}
     
    erro, status = validar_campos_obrigatorios(dados, campos_obrigatórios)
    if erro:
        return jsonify(erro), status
    
    data_nascimento = dados["data_nascimento"]
    
    if not isinstance(data_nascimento, str):
        return jsonify({"erro": "A data de nascimento deve ser uma string no formato YYYY-MM-DD"})
    
    if validar_data(data_nascimento) is None:
        return jsonify({"erro": "Formato de data inválido de ser YYYY-MM-DD"})    
    dados["idade"] = calcular_idade(dados["data_nascimento"])

    dados["id"] = id_professor
    
    # Verificação se ID ja cadastrado
    for professor in dados_professores["professores"]:
        if professor["id"] == dados["id"]:
            return jsonify({"erro": "ID de professor já está cadastrado!"}), 400
        
    id_professor += 1

    dados_professores["professores"].append(dados)
    
    return jsonify(dados), 201

@app.route('/professores', methods=['GET'])
def getProfessores():
    return jsonify(dados_professores["professores"])

@app.route('/professores/<int:id>', methods=['PUT'])
def updateProfessor(id):
    dados = request.json
    campos_permitidos = {"nome", "data_nascimento", "disciplina", "salario", "observacoes"}

    # Verifica se há campos inválidos
    campos_invalidos = [chave for chave in dados.keys() if chave not in campos_permitidos]

    # Verifica a tentaiva de alterar ID do professor
    if "id" in dados:
        return jsonify({"erro": "O ID do professor não pode ser alterado"}), 400

    # Verifica se existem campos inválidos
    if campos_invalidos:
        return jsonify({
            "erro": "Os seguintes campos não podem ser alterados",
            "campos_invalidos": campos_invalidos
            }), 400

    # Atualiza os dados do professor
    for professor in dados_professores['professores']:
        if professor['id'] == id:
            dados_filtrados = {chave: valor for chave, valor in dados.items() if chave in campos_permitidos}

            professor.update(dados_filtrados)
            return jsonify(professor), 200
        
    return jsonify({"erro": "Professor não encontrado!"}), 400

@app.route('/professores/<int:id>', methods=['GET'])
def getProfessorById(id):
    dados = [professor for professor in dados_professores["professores"] if professor["id"]==id]
    
    if dados:
        return jsonify(dados), 200
    return jsonify({"erro": "Professor não encontrado"}), 404    

@app.route('/professores/<int:id>', methods=['DELETE'])
def deleteProfessorById(id):
    dados = [professor for professor in dados_professores["professores"] if professor["id"]==id]
    
    if dados:
        dados_professores["professores"].remove(dados[0])
        return jsonify({"erro": "Professor removido"}), 200
    return jsonify({"erro": "Professor não encontrado"})

@app.route('/turmas', methods=['GET'])
def get_turmas():
    return jsonify(dados_turmas)

@app.route('/turmas/<int:turma_id>', methods=['GET'])
def get_turma_por_id(turma_id):
    turma = None
    for i in dados_turmas:
        if i['turma_id'] == turma_id:
            turma = i
            break
    if turma:
        return jsonify(turma), 200
    else:
        return jsonify({"error": "Turma não encontrada"}), 404

@app.route('/turmas', methods=['POST'])
def add_turma():
    nova_turma = request.get_json()
    if not nova_turma:
        return jsonify({"Error": "Nenhum dado foi inserido"}), 400

    campos_obrigatorios = ['descricao', 'professor_id', 'ativo']
    campos_nao_preenchidos = []
    for campo in campos_obrigatorios:
        if campo not in nova_turma:
            campos_nao_preenchidos.append(campo)
    if campos_nao_preenchidos:
        return jsonify({
            "error": "Os seguintes campos estão ausentes:",
            "campos_nao_preenchidos": campos_nao_preenchidos
        }), 400

    # Verificando se o professor_id existe na lista de professores
    professor_existente = False
    for professor in dados_professores['professores']:
        if professor['id'] == nova_turma['professor_id']:
            professor_existente = True
            break
    
    if not professor_existente:
        return jsonify({"error": "Professor com o ID fornecido não encontrado"}), 404

    # Incrementa o ID da turma automaticamente
    if dados_turmas:
        nova_turma['turma_id'] = dados_turmas[-1]['turma_id'] + 1
    else:
        nova_turma['turma_id'] = 1

    # Adados_professoresonando a nova turma
    dados_turmas.append(nova_turma)
    return jsonify({"mensagem": "Nova turma adados_professoresonada!", "turma": nova_turma}), 201

@app.route('/turmas/<int:turma_id>', methods=['PUT'])
def update_turma(turma_id):
    dados = request.get_json()

    campos_permitidos = ['descricao', 'professor_id', 'ativo']

    # Verifica se a turma existe
    turma = next((t for t in dados_turmas if t['turma_id'] == turma_id), None)
    if not turma:
        return jsonify({"error": "Turma não encontrada!"}), 404

    # Verifica se algum campo inválido foi enviado
    campos_invalidos = [chave for chave in dados.keys() if chave not in campos_permitidos]
    if campos_invalidos:
        return jsonify({
            "erro": "Os seguintes campos não podem ser alterados",
            "campos_invalidos": campos_invalidos
        }), 400

    # Atualiza os dados da turma
    turma.update({chave: valor for chave, valor in dados.items() if chave in campos_permitidos})

    return jsonify(turma), 200

@app.route('/turmas/<int:turma_id>', methods=['DELETE'])
def delete_turma(turma_id):
    turma = next((t for t in dados_turmas if t['turma_id'] == turma_id), None)

    if turma:
        dados_turmas.remove(turma)
        return jsonify({"mensagem": "Turma removida com sucesso!"}), 200
    else:
        return jsonify({"error": "Turma não encontrada!"}), 404
#========================================================================================================================#

if __name__ == "__main__":
    app.run(debug=True)