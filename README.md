# ReSkill API 🚀

API FastAPI para desenvolvimento de carreira com roadmaps personalizados powered by AI.

## 📋 Sobre

A ReSkill API é uma plataforma de desenvolvimento profissional que gera roadmaps de carreira personalizados usando Inteligência Artificial. O sistema analisa o perfil do usuário (profissão atual, nível de experiência, interesses e qualidades) para criar um plano de desenvolvimento estruturado com 7 etapas acionáveis.

### ✨ Recursos Principais

- **🤖 Roadmaps Personalizados com IA**: Geração automática de planos de carreira usando Llama3
- **👥 Gestão Completa de Usuários**: CRUD completo com validação de dados
- **📊 Acompanhamento de Progresso**: Sistema de status para cada etapa do roadmap
- **🔐 Autenticação JWT**: Segurança com tokens e controle de acesso por roles
- **💾 Banco de Dados Flexível**: Suporte para PostgreSQL e SQLite
- **📖 Documentação Automática**: OpenAPI/Swagger integrado
- **🧪 Testes Completos**: Suíte de testes para validação

---

## 🛠 Stack de Tecnologias

- **FastAPI 0.121.2** - Framework web moderno e assíncrono
- **SQLAlchemy** - ORM para banco de dados
- **Pydantic** - Validação e serialização de dados
- **PostgreSQL/SQLite** - Banco de dados
- **JWT (python-jose)** - Autenticação baseada em tokens
- **bcrypt** - Hash de senhas
- **Llama3** - Geração de roadmaps com IA
- **Python 3.11+** - Linguagem principal

---

## 🚀 endpoints da API

### Usuários

#### `POST /users`
Cria um novo usuário no sistema.

**Request Body:**
```json
{
  "name": "João Silva",
  "email": "joao@email.com",
  "currentProfession": "Operador de Caixa",
  "experienceLevel": "iniciante",
  "weeklyStudyTime": 5.0,
  "interests": "Tecnologia, Gestão de Projetos",
  "qualities": ["Dedicado", "Proativo"]
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@email.com",
  "currentProfession": "Operador de Caixa",
  "experienceLevel": "iniciante",
  "weeklyStudyTime": 5.0,
  "interests": "Tecnologia, Gestão de Projetos",
  "qualities": ["Dedicado", "Proativo"]
}
```

#### `GET /users/{user_id}`
Retorna os dados de um usuário específico.

**Response (200):**
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@email.com",
  "currentProfession": "Operador de Caixa",
  "experienceLevel": "iniciante",
  "weeklyStudyTime": 5.0,
  "interests": "Tecnologia, Gestão de Projetos",
  "qualities": ["Dedicado", "Proativo"]
}
```

#### `PUT /users/{user_id}`
Atualiza dados de um usuário (atualização parcial permitida).

**Request Body:**
```json
{
  "name": "João Silva Atualizado",
  "qualities": ["Dedicado", "Proativo", "Organizado"]
}
```

#### `DELETE /users/{user_id}`
Remove um usuário do sistema.

**Response (200):**
```json
{
  "message": "Usuário deletado com sucesso",
  "success": true
}
```

### Roadmaps

#### `GET /roadmap?user_id={user_id}`
Gera um roadmap personalizado baseado no perfil do usuário.

**Response (200):**
```json
{
  "roadmapSteps": [
    {
      "id": "1",
      "title": "Autoconhecimento e Análise de Mercado",
      "description": "Pesquisar tendências e identificar áreas em crescimento no mercado atual",
      "completed": false,
      "order": 1
    },
    {
      "id": "2",
      "title": "Desenvolver Habilidades Técnicas Fundamentais",
      "description": "Fazer cursos online e praticar as habilidades essenciais para sua área",
      "completed": false,
      "order": 2
    }
  ]
}
```

#### `PUT /roadmap/steps/{step_id}/toggle?user_id={user_id}`
Atualiza o status de conclusão de uma etapa do roadmap.

**Request Body:**
```json
{
  "status": "concluido"
}
```

**Status possíveis:**
- `"pendente"`
- `"em_andamento"`
- `"concluido"`

**Response (200):**
```json
{
  "message": "Status atualizado com sucesso",
  "success": true
}
```

### Autenticação

#### `POST /login`
Autentica usuário e retorna token JWT.

**Request Body:**
```json
{
  "email": "joao@email.com",
  "password": "senha123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "João Silva",
    "email": "joao@email.com"
  }
}
```

---

## 📦 Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- PostgreSQL (produção) ou SQLite (desenvolvimento)
- pip e venv

### 1. Clonar o Repositório

```bash
git clone <repository-url>
cd reskill-api
```

### 2. Criar Ambiente Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Ambiente (Opcional)

Crie um arquivo `.env` na raiz do projeto se quiser personalizar:

```env
# Usar PostgreSQL em vez de SQLite (opcional)
DATABASE_URL=postgresql://seu_user:sua_senha@localhost:5432/seu_db

# IA Service (opcional - usa mock se não configurado)
GROQ_API_KEY=sua_chave_groq_aqui
```

**Observação:** Se não criar `.env`, usa SQLite automaticamente (`reskill.db`)

### 5. Iniciar o Servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em `http://localhost:8000`

### 6. Acessar Documentação

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 🧪 Testes

### Executar Todos os Testes

```bash
python -m pytest app/tests/ -v
```

### Executar Testes Específicos

```bash
# Testes de usuários
python -m pytest app/test/test_usuarios_api.py -v

# Testes de login e autenticação
python -m pytest app/test/test_login.py -v

# Todos os testes
python -m pytest app/test/ -v
```

---

## 🏗 Arquitetura

### Estrutura do Projeto

```
reskill-api/
├── app/
│   ├── controllers/
│   │   └── controller.py          # Camada de      controle HTTP
│   ├── services/
│   │   ├── service.py            # Lógica de negócio
│   │   └── ai_roadmap.py         # Serviço de IA
│   ├── models/
│   │   └── database.py           # Models e configuração do DB
│   ├── schemas/
│   │   └── pydantic.py           # Schemas de validação
│   ├── tests/
│   │   ├── test_usuario.py       # Testes de usuários
│   │   └── test_roadmap.py       # Testes de roadmaps
│   ├── main.py                   # Aplicação FastAPI
│   └── login.py                  # Endpoints de autenticação
├── requirements.txt              # Dependências
└── README.md                     # Este arquivo
```

### Camadas da Arquitetura

1. **Controller Layer**: Gerencia requisições HTTP, validação e respostas
2. **Service Layer**: Contém a lógica de negócio e regras de domínio
3. **Data Layer**: Models SQLAlchemy e configuração do banco de dados
4. **Schemas**: Validação de dados com Pydantic

### Models do Banco de Dados

- **Usuario**: Perfil do usuário com qualidades em JSON
- **Steps**: Definições genéricas de etapas
- **UsuarioStep**: Associação usuário-etapa
- **StatusStep**: Status individual por usuário/etapa

---

## 🤖 Integração com IA

### Como Funciona

A API utiliza a Groq API com o modelo Llama3-8b para gerar roadmaps personalizados:

1. **Análise do Perfil**: Considera profissão, experiência, interesses e qualidades
2. **Geração Estruturada**: Sempre retorna 7 etapas numeradas
3. **Contexto Personalizado**: Adapta sugestões ao perfil do usuário
4. **Fallback Automático**: Usa mock se a API não estiver disponível

### Configuração da IA

```env
GROQ_API_KEY=gsk_...
```

Sem a chave, o sistema usa roadmaps mockados.

---

## 🔒 Segurança

- **JWT Tokens**: 30 minutos de expiração
- **Hash de Senhas**: bcrypt com salt
- **Validação de Input**: Pydantic schemas
- **Controle de Acesso**: Roles (admin/user)
- **CORS Configurável**: Restrito em produção
- **SQL Injection Protection**: SQLAlchemy ORM

---

## 📈 Monitoramento e Logs

- **Database Echo**: Logs SQL em desenvolvimento
- **HTTP Status Codes**: Padrão RESTful
- **Error Handling**: Tratamento centralizado de exceções
- **Request Logging**: Middleware FastAPI
