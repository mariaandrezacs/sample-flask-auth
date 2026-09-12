# sample-flask-auth

Repositório criado para armazenar o código da API de autenticação com banco de dados MySQL.

## Sobre o projeto

API REST desenvolvida em Flask para autenticação e gerenciamento de usuários, com persistência em banco de dados MySQL. O projeto utiliza Flask-Login para controle de sessão e bcrypt para criptografia de senhas.

## Tecnologias

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- MySQL
- bcrypt

## Funcionalidades

- Cadastro de usuários
- Autenticação de usuários
- Logout
- Consulta de usuário
- Atualização de senha
- Exclusão de usuários (somente admin)
- Controle de acesso baseado em roles (`user` e `admin`)

## Endpoints

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|--------------|
| POST | `/login` | Realiza login do usuário | Não |
| GET | `/logout` | Realiza logout do usuário | Sim |
| POST | `/user` | Cria um novo usuário | Não |
| GET | `/user/<id_user>` | Retorna o nome de usuário pelo ID | Sim |
| PUT | `/user/<id_user>` | Atualiza a senha do usuário | Sim |
| DELETE | `/user/<id_user>` | Deleta um usuário | Sim (admin) |

## Regras de acesso

- Usuários com role `user` só podem atualizar a própria senha.
- Apenas usuários com role `admin` podem deletar outros usuários.
- Um usuário não pode se auto-deletar.

## Como executar

1. Suba o banco de dados com Docker Compose:

```bash
docker-compose up -d
```

2. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Execute a aplicação:

```bash
python app.py
```

A aplicação será iniciada em `http://127.0.0.1:5000`.

## Configuração do banco de dados

A conexão com o MySQL está configurada em `app.py`:

```python
"mysql+pymysql://root:admin123@127.0.0.1:3307/flask-crud"
```

## Estrutura do projeto

```
sample-flask-auth/
├── app.py
├── database.py
├── docker-compose.yml
├── requirements.txt
├── README.md
└── models/
    └── user.py
```
