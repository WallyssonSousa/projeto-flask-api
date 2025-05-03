from swagger.namespace import alunos_ns, professores_ns, turmas_ns

# Função para registrar os namespaces
def configure_swagger(app):
    app.init_app(app)
    app.add_namespace(alunos_ns, path="/alunos")
    app.add_namespace(professores_ns, path="/professores")
    app.add_namespace(turmas_ns, path="/turmas")
    #app.add_namespace(turmas_ns, path="/turmas")# implementar ainda o namespace turmas
    app.mask_swagger = False