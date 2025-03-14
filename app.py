from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

dici = {"professores":[]}
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
    
# ROTAS⬇️

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
    for professor in dici["professores"]:
        if professor["id"] == dados["id"]:
            return jsonify({"erro": "ID de professor já está cadastrado!"}), 400
        
    id_professor += 1

    dici["professores"].append(dados)
    
    return jsonify(dados), 201

@app.route('/professores', methods=['GET'])
def getProfessores():
    return jsonify(dici["professores"])

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
    for professor in dici['professores']:
        if professor['id'] == id:
            dados_filtrados = {chave: valor for chave, valor in dados.items() if chave in campos_permitidos}

            professor.update(dados_filtrados)
            return jsonify(professor), 200
        
    return jsonify({"erro": "Professor não encontrado!"}), 400

if __name__ == "__main__":
    app.run(debug=True)