from flask_restx import Namespace, Resource, fields
from services.ProfessorService import get_todos_professores, get_professor_por_id, adicionar_professor, atualizar_professor, deletar_professor

professores_ns = Namespace("professores", description="Operações relacionadas aos professores")

professor_model = professores_ns.model("Professor", {
    "nome": fields.String(required=True, description="Nome do professor"),
    "data_nascimento": fields.String(required=True, description="Data de nascimento (YYYY-MM-DD)"),
    "disciplina": fields.Float(required=True, description="Disciplina"),
    "salario": fields.Float(required=True, description="Salario"),
    "observacoes": fields.Integer(required=True, description="Obsevacoes"),
})

professor_output_model = professores_ns.model("ProfessorOutput", {
    "id": fields.Integer(description="ID do professor"),
    "nome": fields.String(description="Nome do professor"),
    "idade": fields.Integer(description="Idade do professor"),
    "data_nascimento": fields.String(description="Data de nascimento (YYYY-MM-DD)"),
    "disciplina": fields.Float(description="Disciplina do professor"),
    "salario": fields.Float(description="Salario do professor"),
    "observacoes": fields.Float(description="Obeservacoes do professor")
})

@professores_ns.route("/")
class ProfessorResource(Resource):
    @professores_ns.marshal_list_with(professor_output_model)
    def get(self):
        """Lista todos os professores"""
        return get_todos_professores()

    @professores_ns.expect(professor_model)
    def post(self):
        """Cria um nono professor"""
        data = professores_ns.payload
        response, status_code = adicionar_professor(data)
        return response, status_code

@professores_ns.route("/<int:id_professor>")
class ProfessorIdResource(Resource):
    @professores_ns.marshal_with(professor_output_model)
    def get(self, id_professor):
        """Obtém um professor pelo ID"""
        return get_professor_por_id(id_professor)

    @professores_ns.expect(professor_model)
    def put(self, id_professor):
        """Atualiza um professor pelo ID"""
        data = professores_ns.payload
        atualizar_professor(id_professor, data)
        return data, 200

    def delete(self, id_professor):
        """Exclui um professor pelo ID"""
        deletar_professor(id_professor)
        return {"message": "professor excluído com sucesso"}, 200