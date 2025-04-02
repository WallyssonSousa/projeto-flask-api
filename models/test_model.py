import requests
import unittest

class TestStringMethods(unittest.TestCase):
    
    def test_001_professores_GET(self):
        r = requests.get('http://localhost:5000/professores')
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /professores no seu server")
        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")
        self.assertEqual(type(obj_retornado),type([]))
        
    def test_002_professores_POST(self):
        r = requests.post('http://localhost:5000/professores',json={
            'nome':"Nicolas",
            'data_nascimento':"2006-04-11",
            'disciplina': "ADS",
            'salario': 1900,
            'observacoes': "Nenhuma"
            })
        
        r = requests.post('http://localhost:5000/professores',json={
            'nome':"Enrico",
            'data_nascimento':"2006-04-11",
            'disciplina': "CB",
            'salario': 2900,
            'observacoes': "Nenhuma"
        })

        r_lista = requests.get('http://localhost:5000/professores')
        lista_retornada = r_lista.json()     

        achei_nicolas = False
        achei_enrico = False
        for professor in lista_retornada:
            if professor['nome'] == 'Nicolas':
                achei_nicolas = True
            if professor['nome'] == 'Enrico':
                achei_enrico = True
        
        #se algum desses "achei" nao for True, dou uma falha
        if not achei_nicolas:
            self.fail('aluno Nicolas nao apareceu na lista de professores')
        if not achei_enrico:
            self.fail('aluno Enrico nao apareceu na lista de professores')
            
    def test_003_professores_GetById(self):
        r = requests.get('http://localhost:5000/professores/1')
        if r.status_code == 404:
            self.fail("voce nao definiu uma rota para dar get pelo id do professor")
        try:
            obj_retornado = r.json()
        except:
            self.fail("voce não retornou um JSON")
        self.assertEqual(type(obj_retornado), type({}))
        
    def test_004_professores_PUT(self):
        
        def calcular_idade(data_nascimento):
            today = datetime.today()
            nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
            idade = today.year - nascimento.year - ((today.month, today.day) < (nascimento.month, nascimento.day))
            return idade
        
        # Define os novos dados para o professor ID 1
        novos_dados = {
            "nome": "Kaique", 
            "data_nascimento": "2000-09-18", 
            "disciplina": "SI", 
            "salario": 2500, 
            "observacoes": "Nenhuma"
        }

        # Faz a requisição PUT para atualizar o professor ID 1
        r = requests.put('http://localhost:5000/professores/1', json=novos_dados)

        # Verifica se a atualização foi bem-sucedida (status code 200 ou 204)
        self.assertIn(r.status_code, [200, 204], "Falha ao atualizar o professor")

        # Faz uma nova requisição GET para verificar se os dados foram atualizados
        r_get = requests.get('http://localhost:5000/professores/1')

        # Verifica se o professor ainda existe
        self.assertEqual(r_get.status_code, 200, "Professor não encontrado após atualização")

        # Obtém o JSON retornado
        professor_atualizado = r_get.json()

        # Compara os dados atualizados com os esperados
        self.assertEqual(professor_atualizado["nome"], novos_dados["nome"])
        self.assertEqual(professor_atualizado["id"], 1)
        self.assertEqual(professor_atualizado["idade"],calcular_idade((novos_dados["data_nascimento"])))
        self.assertEqual(professor_atualizado["data_nascimento"], novos_dados["data_nascimento"])
        self.assertEqual(professor_atualizado["disciplina"], novos_dados["disciplina"])
        self.assertEqual(professor_atualizado["salario"], novos_dados["salario"])
        self.assertEqual(professor_atualizado["observacoes"], novos_dados["observacoes"])
        
    def test_005_professores_DELETE(self):
        
        r = requests.delete('http://localhost:5000/professores/1')

        self.assertEqual(r.status_code, 200, "Falha ao excluir o professor")

        # Verifica se a mensagem de sucesso está correta
        resposta = r.json()
        self.assertIn("mensagem", resposta)
        self.assertEqual(resposta["mensagem"], "Professor removido")

        # Faz uma nova requisição GET para verificar se o professor foi realmente excluído
        r_get = requests.get('http://localhost:5000/professores/1')

        # Verifica se o professor não é encontrado (status code 404)
        self.assertEqual(r_get.status_code, 404, "O professor não foi excluído corretamente")
        
    def test_006_turmas_GET(self):
        r = requests.get('http://localhost:5000/turmas')
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /turmas no seu server")
        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")
        self.assertEqual(type(obj_retornado),type([]))
        
    def test_007_turmas_POST(self):
        r = requests.post('http://localhost:5000/turmas',json={
            "descricao": "Nenhuma",
            "materia": "API",
            "turno": "Matutino",
            "professor_id": 1
            })
        
        r = requests.post('http://localhost:5000/turmas',json={
            "descricao": "Nenhuma",
            "materia": "CYBER",
            "turno": "Noturno",
            "professor_id": 2
        })

        r_lista = requests.get('http://localhost:5000/turmas')
        lista_retornada = r_lista.json()
                                        
        achei_turma1 = False
        achei_turma2 = False
        
        for turma in lista_retornada:
            if turma['materia'] == 'API':
                achei_turma1 = True
            if turma['materia'] == 'CYBER':
                achei_turma2 = True
        
        #se algum desses "achei" nao for True, dou uma falha
        if not achei_turma1:
            self.fail('Turma API não foi encontrada')
        if not achei_turma2:
            self.fail('Turma CYBER não foi encontrada')
            
    def test_008_turmas_GetById(self):
        r = requests.get('http://localhost:5000/turmas/1')
        if r.status_code == 404:
            self.fail("voce nao definiu uma rota para dar get pelo id da turma")
        try:
            obj_retornado = r.json()
        except:
            self.fail("voce não retornou um JSON")
        self.assertEqual(type(obj_retornado), type({}))
        
    def test_009_turmas_PUT(self):
        # Define os novos dados para a turma ID 1
        novos_dados = {
            "descricao": "Turma de Matemática",
            "professor_id": 2,
            "ativo": False
        }
        # Faz a requisição PUT para atualizar a turma ID 1
        r = requests.put('http://localhost:5000/turmas/1', json=novos_dados)
        # Verifica se a atualização foi bem-sucedida (status code 200)
        self.assertEqual(r.status_code, 200, "Falha ao atualizar a turma")
        # Faz uma nova requisição GET para verificar se os dados foram atualizados
        r_get = requests.get('http://localhost:5000/turmas/1')
        # Verifica se a turma ainda existe
        self.assertEqual(r_get.status_code, 200, "Turma não encontrada após atualização")
        # Obtém o JSON retornado
        turma_atualizada = r_get.json()
        # Compara os dados atualizados com os esperados
        self.assertEqual(turma_atualizada["descricao"], novos_dados["descricao"])
        self.assertEqual(turma_atualizada["professor_id"], novos_dados["professor_id"])
        self.assertEqual(turma_atualizada["ativo"], novos_dados["ativo"])
        
    def test_010_turmas_DELETE(self):
        # Faz a requisição DELETE para excluir o professor ID 1
        r = requests.delete('http://localhost:5000/turmas/1')

        # Verifica se a exclusão foi bem-sucedida (status code 200)
        self.assertEqual(r.status_code, 200, "Falha ao excluir a turma")

        # Verifica se a mensagem de sucesso está correta
        resposta = r.json()
        self.assertIn("mensagem", resposta)
        self.assertEqual(resposta["mensagem"], "Turma removida")

        # Faz uma nova requisição GET para verificar se o professor foi realmente excluído
        r_get = requests.get('http://localhost:5000/turma/1')

        # Verifica se o professor não é encontrado (status code 404)
        self.assertEqual(r_get.status_code, 404, "O professor não foi excluído corretamente")