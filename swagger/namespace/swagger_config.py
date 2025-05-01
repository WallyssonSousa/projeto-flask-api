from swagger.namespaces.aluno_namespace import alunos_ns

# Função para registrar os namespaces
def configure_swagger(app):
    api.init_app(app)
    api.add_namespace(alunos_ns, path="/alunos")
    api.add_namespace(professores_ns, path="/professores")
    api.add_namespace(turmas_ns, path="/turmas")
    api.mask_swagger = False