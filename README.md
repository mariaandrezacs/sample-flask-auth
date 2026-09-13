# sample-flask-auth 2.0.0

API REST de autenticação e gerenciamento de usuários em Flask, refatorada com princípios de engenharia de software, arquitetura em camadas, padrões de projeto e boas práticas.

## Sobre a v2.0.0

A nova versão separa responsabilidades em camadas claras:

- **Domain**: entidades, value objects, exceções de domínio e contratos de repositório.
- **Application**: casos de uso / serviços e DTOs.
- **Infrastructure**: banco de dados (SQLAlchemy), repositórios concretos e criptografia (bcrypt).
- **Interfaces**: rotas Flask e tratamento de erros.

Padrões aplicados: Repository, Injeção de Dependências manual, DTOs, Factory de aplicação, separação por camadas e tratamento centralizado de erros.

## Conceitos e padrões

- **Arquitetura em camadas**: separação entre Domain, Application, Infrastructure e Interfaces, onde cada camada tem uma responsabilidade única.
- **Clean Architecture / Ports and Adapters**: o domínio não depende de frameworks ou detalhes de banco, apenas de contratos abstratos.
- **Repository Pattern**: `UserRepository` define a interface e `SqlAlchemyUserRepository` implementa o acesso ao banco, permitindo trocar a fonte de dados sem alterar regras de negócio.
- **Injeção de Dependências**: `Container` orquestra as instâncias de repositório, hasher e serviços, desacoplando as camadas.
- **Data Transfer Objects (DTOs)**: objetos imutáveis (`dataclasses`) que transportam dados entre as camadas sem expor as entidades de domínio.
- **Factory Pattern**: `create_app` monta a aplicação Flask, registrando extensões, blueprints e handlers de erro de forma centralizada.
- **Value Objects**: `Role` é um `Enum` que representa os papéis válidos do sistema, garantindo consistência.
- **Tratamento centralizado de erros**: exceções de domínio são mapeadas para códigos HTTP uniformes em `interfaces/errors.py`.

## Tecnologias

- Python 3.11+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- MySQL
- bcrypt

## Estrutura do projeto

```
sample-flask-auth/
├── .env.example
├── wsgi.py
├── run.py
├── docker-compose.yml
├── requirements.txt
├── README.md
├── src/
│   └── sample_flask_auth/
│       ├── __init__.py
│       ├── config.py
│       ├── container.py
│       ├── domain.py
│       ├── dto.py
│       ├── services.py
│       ├── infrastructure/
│       │   ├── database.py
│       │   ├── models.py
│       │   ├── repositories.py
│       │   └── security.py
│       └── interfaces/
│           ├── api.py
│           └── errors.py
└── tests/
    ├── conftest.py
    └── test_domain.py
```

## Endpoints

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|--------------|
| POST | `/login` | Realiza login do usuário | Não |
| GET | `/logout` | Realiza logout do usuário | Sim |
| POST | `/user` | Cria um novo usuário | Não |
| GET | `/user/<id_user>` | Retorna os dados do usuário pelo ID | Sim |
| PUT | `/user/<id_user>` | Atualiza a senha do usuário | Sim |
| DELETE | `/user/<id_user>` | Deleta um usuário | Sim (admin) |

## Regras de acesso

- Usuários com role `user` só podem atualizar a própria senha.
- Apenas usuários com role `admin` podem deletar outros usuários.
- Um usuário não pode se auto-deletar.

## Como executar

1. Copie e ajuste as variáveis de ambiente:

```bash
cp .env.example .env
```

2. Suba o banco de dados com Docker Compose:

```bash
docker-compose up -d
```

3. Ative o ambiente virtual e instale as dependências:

```bash
venv\Scripts\activate
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
python run.py
```

A aplicação será iniciada em `http://127.0.0.1:5000`.

## Testes

```bash
pytest
```
