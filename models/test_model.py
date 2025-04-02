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