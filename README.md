# Projeto Flask - Desenvolvimento de API e Microserviços

## Descrição
Este projeto foi desenvolvido como parte da disciplina de **Desenvolvimento de API e Microserviços**. Ele está dividido em quatro fases, e atualmente estamos na primeira fase, que consiste na implementação de um CRUD e testes.

## Tecnologias Utilizadas
- Python 3
- Flask
- Flask SQLAlchemy
- Flask Migrate
- Pytest
- SQLite (ou outro banco de dados configurável)

## Estrutura do Projeto
```
projeto/
|-- venv/
|-- app.py
|-- requirements.txt
|-- README.md
```

## Como Rodar o Projeto

```sh

python app.py

```

### 1. Clonar o Repositório
```sh
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Criar e Ativar um Ambiente Virtual
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### 3. Instalar Dependências
```sh
pip install -r requirements.txt
```

### 4. Configurar o Banco de Dados
```sh
flask db init
flask db migrate -m "Inicialização do banco de dados"
flask db upgrade
```

### 5. Rodar o Servidor Flask
```sh
python app.py
```

O servidor será iniciado em `http://127.0.0.1:5000/`

## Como Executar os Testes
```sh
pytest
```

## Próximas Fases
1. **Fase 1:** Implementação do CRUD e testes ✅ (em andamento)
2. **Fase 2:** 
3. **Fase 3:** 
4. **Fase 4:** 

---
Este README será atualizado conforme o progresso do projeto. 🚀

