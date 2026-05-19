# 🏬 SaturnTech - Sistema de Gerenciamento de Produtos

## 📋 Sobre o Projeto

Sistema web desenvolvido em **Flask** para gerenciamento de produtos de uma loja. O projeto foi desenvolvido como atividade acadêmica técnica para demonstrar conhecimentos em:

- Banco de dados SQLite
- Consultas SQL (ORDER BY, operadores relacionais, operadores lógicos)
- Funções de agregação (AVG, COUNT, GROUP BY)
- Desenvolvimento web com Flask
- Interface responsiva com HTML5 e CSS3
- API REST para consumo dos dados
- Segurança com rate limiting e headers HTTP
- Testes automatizados com pytest
- Containerização com Docker
- Documentação interativa da API

## 🚀 Funcionalidades

### 📊 Consultas SQL Implementadas

| Tipo | Consultas |
|------|-----------|
| **ORDER BY** | Ordenação crescente e decrescente por preço |
| **Operadores Relacionais** | `=`, `≠`, `>`, `<`, `≥`, `≤` (comparação com R$ 50,00) |
| **Operadores Lógicos** | `AND` (preço > 50 AND estoque > 0) / `OR` (preço < 30 OR categoria = 'Eletrônicos') |
| **Agregações** | Média total, contagem total, média por categoria, contagem por categoria |

### 🎨 Interface Web

- Listagem completa de produtos
- Exibição de todas as consultas em tabelas organizadas
- Design responsivo (funciona em desktop e mobile)
- Cards interativos com métricas
- Modo Escuro (respeita preferência do sistema)
- Botão "voltar ao topo" em dispositivos móveis
- Favicon personalizado

### 📦 Consultas Implementadas
- Produto	Preço	Categoria	Estoque
- Teclado Mecânico	R$ 250,00	Acessórios	10
- Mouse Gamer	R$ 150,00	Acessórios	5
- Monitor 24	R$ 1.200,00	Periféricos	3
- Headset Bluetooth	R$ 300,00	Áudio	7
- Notebook Gamer	R$ 5.000,00	Computadores	2
- SSD 1TB	R$ 600,00	Armazenamento	12
- Produto Preço 50	R$ 50,00	Eletrônicos	15

### 🔒 Segurança

- Variáveis de ambiente: Chave secreta e modo debug via `.env`
- Rate limiting: 100 requisições/minuto por IP nas rotas API
- Headers de segurança: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy
- SQL Injection: Parâmetros sanitizados (uso de `?` no SQL)
- .gitignore: Arquivos sensíveis (.env, venv, *.db, app.log) não são versionados

### 📡 API REST

O sistema expõe endpoints para consumo programático:

| Endpoint | Método | Descrição | Paginação |
|----------|--------|-----------|-----------|
| `/api/produtos` | GET | Lista todos os produtos | ✅ Sim |
| `/api/produtos/buscar` | GET | Busca produtos com filtros | ✅ Sim |
| `/api/consultas/order_by` | GET | ORDER BY crescente/decrescente | ❌ |
| `/api/consultas/relacionais` | GET | Operadores relacionais com 50.00 | ❌ |
| `/api/consultas/logicas` | GET | Operadores lógicos (AND/OR) | ❌ |
| `/api/consultas/agregacoes` | GET | Médias, contagens e agrupamentos | ❌ |

**Parâmetros de busca (`/api/produtos/buscar`):**
- `nome` - Busca parcial por nome
- `categoria` - Filtro por categoria exata
- `min_preco` / `max_preco` - Filtro por faixa de preço
- `min_estoque` - Estoque mínimo
- `page` / `per_page` - Paginação

**Exemplo de resposta:**
```json
{
  "page": 1,
  "per_page": 5,
  "total": 7,
  "total_pages": 2,
  "data": [
    {"id": 1, "nome": "Teclado Mecânico", "preco": 250.0, "categoria": "Acessórios", "estoque": 10}
  ]
}
```
### 📚 Documentação da API

> 📚 **Documentação da API disponível em** [`/api/docs`](http://127.0.0.1:5000/api/docs)

- Lista completa de todos os endpoints
- Exemplos de uso com **curl**
- Descrição detalhada de cada consulta
- Informações sobre rate limiting

## 🧪 Testes Automatizados

O projeto inclui testes unitários com pytest para garantir a qualidade do código:

```bash
pytest tests/ -v
```

```bash
pytest tests/test_app.py -v
```

## 🐳 Docker

O projeto pode ser executado em container para fácil implantação:

### Construir a imagem
```bash
docker build -t lojas-flask .
```

### Executar o container
```bash
docker run -d -p 5000:5000 --name lojas-app lojas-flask
```

### Visualizar logs
```bash
docker logs lojas-app
```

### Parar o container
```bash
docker stop lojas-app
```

### Remover o container
```bash
docker rm lojas-app
```

## 🧩 Arquitetura Modular

O projeto foi organizado de forma modular para facilitar manutenção e escalabilidade como descrito abaixo na estrutura do projeto:

### 📁 Estrutura do Projeto

```text
lojas_flask/
├── main.py                     # Aplicação principal (rotas + segurança)
├── queries.py                 # Todas as consultas SQL centralizadas
├── requirements.txt           # Dependências do projeto
├── .env                       # Variáveis de ambiente (não versionado)
├── .gitignore                 # Arquivos ignorados pelo Git
├── Dockerfile                 # Configuração do container Docker
├── .dockerignore              # Arquivos ignorados pelo Docker
├── tests/                     # Testes automatizados
│   └── test_app.py            # Testes da API
├── static/
│   ├── main.css               # Estilos principais
│   ├── mobile.css             # Responsividade e adaptabilidade
│   ├── async_loading.js       # JavaScript assíncrono
│   ├── swagger.json           # Documentação OpenAPI/Swagger manual
│   └── baturno_web_icon.ico   # Favicon
├── templates/
│   ├── index.html             # Template principal (monta os partials)
│   └── partials/              # Componentes reutilizáveis
│       ├── header.html
│       ├── lista_produtos.html
│       ├── order_by.html
│       ├── operadores_relacionais.html
│       ├── logicos.html
│       ├── agregacoes.html
│       └── footer.html
├── app.log                    # Logs da aplicação (gerado automaticamente)
└── lojas.db                   # Banco de dados (criado automaticamente)
```

# 💻 Pré-requisitos
Antes de começar, você vai precisar ter instalado em sua máquina:
- Python 3.8+
- Git
- Pip (gerenciador de pacotes Python - já vem com o Python)
- Docker Desktop (Opcional)

# 🔧 Como Executar o Projeto?

## 1. Clone o repositório

### via HTTPS
```bash
git clone https://github.com/saturnbells/lojas_flask.git
```

### Via SSH (se configurado)
```bash
git clone git@github.com:saturnbells/lojas_flask.git
```

### Acesse a pasta do projeto
```bash
cd lojas_flask
```

## 2. Crie um ambiente virtual

### Windows (via Git Bash)
```bash
python -m venv venv
source venv/Scripts/activate
```

### Windows (via CMD ou PowerShell)
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux ou Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Instale as dependências

### Caso tenha o ambiente virtual ativado
```bash
pip install -r requirements.txt
```

### Caso queira instalar o Flask diretamente
```bash
pip install flask
```

## 4. Execute a aplicação

### Usando o launcher do Python (Windows)
```bash
py main.py
```

### Ou com python padrão
```bash
python main.py
```

### Ou com python3 (Linux ou Mac)
```bash
python3 main.py
```

## 5. Acesse no navegador
Após executar, você verá uma mensagem como:

* Running on http://127.0.0.1:5000
* Running on http://192.168.0.103:5000
Abra seu navegador e acesse qualquer um destes endereços:

Endereço	Descrição
http://127.0.0.1:5000	Localhost (apenas seu computador)
http://localhost:5000	Mesmo que o endereço acima
http://192.168.0.X:5000	IP da sua rede local

## 🔧 Comandos Úteis

```bash
py main.py
```

```bash
pytest tests/ -v
```

```bash
tail -f app.log
```

```bash
docker build -t lojas-flask .
docker run -d -p 5000:5000 --name lojas-app lojas-flask
docker logs lojas-app
docker stop lojas-app
```

```bash
rm -rf __pycache__/
find . -name "*.pyc" -delete
```

## 🐳 Comandos Úteis (Docker)

### Construir a imagem
```bash
docker run -d -p 5000:5000 --name lojas-app lojas-flask
```

### Rodar o container
```bash
docker run -d -p 5000:5000 --name lojas-app lojas-flask
```

### Ver logs
```bash
docker logs lojas-app
```

### Ver logs
```bash
docker rm -f lojas-app
```

### Remover o container existente em caso de erro
```bash
docker logs lojas-app
```

### Executar um novo container
```bash
docker run -d -p 5000:5000 --name lojas-app lojas-flask
```

### Ver todos os containers (ativos e parados)
```bash
docker ps -a
```

### Ver apenas os containers ativos
```bash
docker ps
```

### Parar um container (Sem remover)
```bash
docker stop lojas-app
```

### Remover um container parado
```bash
docker rm lojas-app
```

### Forçar remoção (mesmo se estiver rodando)
```bash
docker rm -f lojas-app
```

### Ver logs do container
```bash
docker logs lojas-app
```

### Ver logs em tempo real
```bash
docker logs -f lojas-app
```

### Comando completo para reconstruir imagem e rodar o Docker

```bash
docker rm -f lojas-app 2>/dev/null; docker build -t lojas-flask . && docker run -d -p 5000:5000 --name lojas-app lojas-flask
```

## 🛠️ Tecnologias Utilizadas

- Backend: Python 3.14+ / Flask 3.1.3
- Banco de Dados: SQLite3
- Frontend: HTML5, CSS3, JavaScript
- API: REST (JSON)
- Segurança: python-dotenv, flask-limiter
- Tests: pytest
- Containerização: Docker
- Documentação: Swagger/OpenAPI (manual)
- Versionamento: Git, Github

## 📊 Exemplos de Consultas SQL Implementadas

```sql
-- ORDER BY crescente
SELECT nome, preco FROM PRODUTOS ORDER BY preco ASC;

-- ORDER BY decrescente
SELECT nome, preco FROM PRODUTOS ORDER BY preco DESC;

-- Operador igual (=)
SELECT * FROM PRODUTOS WHERE preco = 50.00;

-- Operador diferente (≠)
SELECT * FROM PRODUTOS WHERE preco != 50.00;

-- Operador maior que (>)
SELECT * FROM PRODUTOS WHERE preco > 50.00;

-- Operador menor que (<)
SELECT * FROM PRODUTOS WHERE preco < 50.00;

-- Operador maior ou igual (>=)
SELECT * FROM PRODUTOS WHERE preco >= 50.00;

-- Operador menor ou igual (<=)
SELECT * FROM PRODUTOS WHERE preco <= 50.00;

-- Operador lógico AND
SELECT * FROM PRODUTOS WHERE preco > 50 AND estoque > 0;

-- Operador lógico OR
SELECT * FROM PRODUTOS WHERE preco < 30 OR categoria = 'Eletrônicos';

-- Média de preço de todos os produtos
SELECT AVG(preco) as media_preco FROM PRODUTOS;

-- Contagem total de produtos
SELECT COUNT(*) as total FROM PRODUTOS;

-- Média de preço por categoria
SELECT categoria, AVG(preco) as media_preco, COUNT(*) as quantidade 
FROM PRODUTOS GROUP BY categoria;

-- Média de preço dos produtos em estoque
SELECT AVG(preco) as media_preco_estoque FROM PRODUTOS WHERE estoque > 0;
```

## 🗄️ Estrutura do Banco de Dados

```sql
CREATE TABLE PRODUTOS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    categoria TEXT NOT NULL,
    estoque INTEGER NOT NULL DEFAULT 0
);
```

## 👨‍💻 Autor

[![GitHub](https://img.shields.io/badge/GitHub-saturnbells-181717?logo=github)](https://github.com/saturnbells)

# 📝 Licença
Este projeto está sob a licença MIT - veja o arquivo LICENSE para detalhes

Desenvolvido com ❤️🪐 usando Flask e SQLite