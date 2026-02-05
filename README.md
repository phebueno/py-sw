# 🌟 PY-SW API

Uma API completa e robusta para explorar o universo Star Wars, construída com FastAPI e integrada ao Google Cloud Run.

[![Python](https://img.shields.io/badge/Python-3.12+-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Cloud Run](https://img.shields.io/badge/Google_Cloud-Run-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/run)

---

## 🚀 Demo

A API está hospedada no Google Cloud Run:

```
https://star-wars-api-64517826580.us-central1.run.app
```

Acesse a documentação interativa em:

```
https://star-wars-api-64517826580.us-central1.run.app/docs
```

---

## 📋 Características

✅ **6 Módulos Completos**
- People (Personagens)
- Planets (Planetas)
- Species (Espécies)
- Starships (Naves)
- Vehicles (Veículos)
- Films (Filmes)

✅ **Funcionalidades**
- Busca por nome (search parameter)
- Paginação automática
- Tratamento robusto de erros
- Documentação OpenAPI/Swagger
- Testes unitários completos (58+ testes)

✅ **Infraestrutura**
- Containerização com Docker
- Deployment automático no Google Cloud Run
- Code quality com Black, isort e Pylint
- Integração com SWAPI (Star Wars API oficial)

---

## 📦 Requisitos

- **Python 3.12+**
- **Docker & Docker Compose** (opcional, para containerização)
- **Google Cloud SDK** (opcional, para deploy no GCP)
- **uv** (gerenciador de pacotes Python moderno)

---

## 🛠️ Instalação

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd py-sw
```

### 2. Instale as dependências

```bash
make install
# ou
uv sync
```

---

## 🏃 Como Executar

### Desenvolvimento Local

```bash
make dev
```

OU

```bash
uv run -- fastapi dev app/main.py
```

A API estará disponível em: `http://localhost:8000`

### Modo Produção

```bash
make start
```

OU

```bash
uv run -- uvicorn app.main:app
```

---

## 🐳 Docker

### Build da Imagem

```bash
docker build -t star-wars-api:latest .
```

### Rodar Container

```bash
docker run -p 8000:8000 star-wars-api:latest
```

### Usar Docker Compose (Recomendado)

```bash
docker-compose up --build
```

Acesse em: `http://localhost:8000/docs`

---

## 🧪 Testes

### Rodar Todos os Testes

```bash
uv run pytest -v
```

### Rodar Testes de um Módulo Específico

```bash
uv run pytest tests/films/test_service.py -v
uv run pytest tests/starships/test_service.py -v
```

### Com Cobertura

```bash
uv run pytest --cov=app --cov-report=html
```

Visualize em: `htmlcov/index.html`

---
## 📚 Endpoints

### People (Personagens)

```bash
# Listar com busca e paginação
GET /people/?search=luke&page=1

# Buscar por ID
GET /people/1
```

### Planets (Planetas)

```bash
# Listar
GET /planets/?search=tatooine&page=1

# Buscar por ID
GET /planets/1
```

### Species (Espécies)

```bash
GET /species/?search=human&page=1
GET /species/1
```

### Starships (Naves)

```bash
GET /starships/?search=x-wing&page=1
GET /starships/12
```

### Vehicles (Veículos)

```bash
GET /vehicles/?search=speeder&page=1
GET /vehicles/4
```

### Films (Filmes)

```bash
GET /films/?search=hope&page=1
GET /films/1
```

### Endpoint Genérico

Acesse qualquer recurso via:

```bash
GET /swapi/{resource}/?search=query&page=1
```

Onde `{resource}` pode ser: `people`, `planets`, `species`, `starships`, `vehicles`, `films`

---

## 📝 Query Parameters

Todos os endpoints de busca suportam:

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `search` | string | null | Buscar por nome |
| `page` | integer | 1 | Número da página (≥ 1) |

### Exemplos

```bash
# Buscar personagem pelo nome
GET /people/?search=Luke

# Segunda página de planetas
GET /planets/?page=2

# Buscar e paginar
GET /starships/?search=Falcon&page=1
```

---

## 📊 Resposta Padrão

### Listar Recursos

```json
{
  "count": 82,
  "next": "https://...",
  "previous": null,
  "results": [
    {
      "name": "Luke Skywalker",
      "height": "172",
      "mass": "77",
      ...
    }
  ]
}
```

### Buscar por ID

```json
{
  "name": "Luke Skywalker",
  "height": "172",
  "mass": "77",
  "hair_color": "blond",
  "skin_color": "fair",
  ...
}
```

---

## 🏗️ Arquitetura

```
app/
├── main.py                 # Ponto de entrada
├── config.py              # Configurações
├── core/
│   └── swapi_client.py    # Cliente SWAPI compartilhado
├── models/
│   └── schemas.py
├── modules/
│   ├── people/
│   │   ├── router.py      # Rotas HTTP
│   │   ├── service.py     # Lógica de negócio
│   │   └── schema.py      # Validação (Pydantic)
│   ├── planets/
│   ├── species/
│   ├── starships/
│   ├── vehicles/
│   └── films/
└──────
```

---

## ☁️ Deploy no Google Cloud Run

### 1. Setup Inicial

```bash
gcloud auth login
gcloud config set project py-sw-api
gcloud services enable cloudbuild.googleapis.com run.googleapis.com
```

### 2. Deploy Manual

```bash
gcloud run deploy star-wars-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi
```

### 3. Deploy com CI/CD (Cloud Build)

```bash
gcloud builds submit
```

Ou configure um trigger automático no Console GCP que faz deploy a cada push no repositório.

*Obs.: São necessárias configurações adicionais do ambiente do Gooogle Cloud Run, como a configuração do Faturamento e permissões de acesso.* 

---

## 📖 Documentação Interativa

Acesse a documentação Swagger em:

```
http://localhost:8000/docs
```

Ou ReDoc em:

```
http://localhost:8000/redoc
```

---

## ✅ Code Quality

### Formatação com Black e isort

```bash
make format
```

### Verificação com Linter

```bash
make lint
```

### Apenas Verificar (sem modificar)

```bash
make format-check
```

---

## 📋 Makefile Commands

```bash
make help              # Ver todos os comandos
make install           # Instalar dependências
make dev               # Rodar em desenvolvimento
make format            # Formatar código
make lint              # Verificar código
make test              # Rodar testes
make test-cov          # Testes com cobertura
make docker-build      # Build Docker
make docker-up         # Rodar com docker-compose
make docker-down       # Parar containers
make deploy-manual     # Deploy no Cloud Run
```

---

## 🧬 Stack Técnico

| Componente | Tecnologia |
|-----------|-----------|
| **Language** | Python 3.12+ |
| **Framework** | FastAPI |
| **Package Manager** | uv |
| **API Client** | httpx |
| **Validation** | Pydantic |
| **Testing** | pytest, pytest-asyncio |
| **Code Quality** | Black, isort, Pylint |
| **Containerization** | Docker, Docker Compose |
| **Cloud** | Google Cloud Run |
| **CI/CD** | Cloud Build |
| **Data Source** | SWAPI (Star Wars API) |

---

## 📊 Testes

O projeto inclui **58+ testes unitários** cobrindo:

- ✅ Busca de recursos
- ✅ Paginação
- ✅ Validação de parâmetros
- ✅ Tratamento de erros
- ✅ Mocking de cliente SWAPI

### Cobertura por Módulo

| Módulo | Testes |
|--------|--------|
| People | 3 |
| Planets | 3 |
| Species | 10 |
| Starships | 12 |
| Vehicles | 14 |
| Films | 16 |
| **Total** | **58+** |

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'app'"

Certifique-se de estar na pasta raiz do projeto:

```bash
cd /seu/caminho/py-sw
```

### "Port 8000 already in use"

Mude a porta:

```bash
uv run -- uvicorn app.main:app --port 8001
```

### Docker build falha

Certifique-se de que `requirements.txt` existe:

```bash
pip freeze > requirements.txt
```

### GCP deployment falha

Ative as APIs necessárias:

```bash
gcloud services enable cloudbuild.googleapis.com run.googleapis.com
```

---

## 📝 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (opcional):

```bash
# Exemplo
DEBUG=true
LOG_LEVEL=INFO
```

---

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📜 Licença

Este projeto é um exercício técnico baseado no universo Star Wars.

---

## 🔗 Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SWAPI - Star Wars API](https://swapi.dev/)
- [Google Cloud Run](https://cloud.google.com/run)
- [Docker Documentation](https://docs.docker.com/)
- [pytest Documentation](https://docs.pytest.org/)

---

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Desenvolvido com ❤️ para os fãs de Star Wars**

⭐ Se curtiu, deixa uma star! 🌟