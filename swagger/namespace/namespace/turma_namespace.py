from flask_restx import Namespace, Resource, fields
from services.TurmaService import get_todas_turmas, get_turma_por_id, adicionar_turma, atualizar_turma, deletar_turma

turma_ns = Namespace("turmas", description="Operações relacionadas aos turmas")

turma_model = turma_ns.model("turma", {
    "nome": fields.String(required=True, description="Nome da turma"),
    "turno": fields.String(required=True, description="Turno da turma"),
    "ativo": fields.Float(required=True, description="Estado da turma"),
    "id_professor": fields.Float(required=True, description="ID do professor vinculado a turma")
})

turma_output_model = turma_ns.model("turmaOutput", {
    "id": fields.Integer(description="ID da turma"),
    "nome": fields.String(description="Nome da turma"),
    "turno": fields.Integer(description="Turno da turma"),
    "ativo": fields.String(description="Estado da turma"),
    "id_professor": fields.Float(description="ID do professor vinculado a turma")
})

@turma_ns.route("/")
class TurmaResource(Resource):
    @turma_ns.marshal_list_with(turma_output_model)
    def get(self):
        """Lista todas as turma"""
        return get_todas_turmas()

    @turma_ns.expect(turma_model)
    def post(self):
        """Cria uma nova turma"""
        data = turma_ns.payload
        response, status_code = adicionar_turma(data)
        return response, status_code

@turma_ns.route("/<int:id_turma>")
class TurmaIdResource(Resource):
    @turma_ns.marshal_with(turma_output_model)
    def get(self, id_turma):
        """Obtém uma turma pelo ID"""
        return get_turma_por_id(id_turma)

    @turma_ns.expect(turma_model)
    def put(self, id_turma):
        """Atualiza uma turma pelo ID"""
        data = turma_ns.payload
        atualizar_turma(id_turma, data)
        return data, 200

    def delete(self, id_turma):
        """Exclui uma turma pelo ID"""
        deletar_turma(id_turma)
        return {"message": "turma excluído com sucesso"}, 200