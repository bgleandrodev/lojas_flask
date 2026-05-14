# 🏬 LOJAS - Sistema de Gerenciamento de Produtos

## 📋 Sobre o Projeto

Sistema web desenvolvido em **Flask** para gerenciamento de produtos de uma loja. O projeto foi desenvolvido como atividade acadêmica técnica para demonstrar conhecimentos em:

- Banco de dados SQLite
- Consultas SQL (ORDER BY, operadores relacionais, operadores lógicos)
- Funções de agregação (AVG, COUNT, GROUP BY)
- Desenvolvimento web com Flask
- Interface responsiva com HTML5 e CSS3

## 🚀 Funcionalidades

## 📊 Consultas Implementadas

| Tipo | Consultas |
|------|-----------|
| **ORDER BY** | Ordenação crescente e decrescente por preço |
| **Operadores Relacionais** | `=`, `≠`, `>`, `<`, `≥`, `≤` (comparação com R$ 50,00) |
| **Operadores Lógicos** | `AND` (preço > 50 AND estoque > 0) / `OR` (preço < 30 OR categoria = 'Eletrônicos') |
| **Agregações** | Média total, contagem total, média por categoria, contagem por categoria |

## 🎨 Interface Web

- Listagem completa de produtos
- Exibição de todas as consultas em tabelas organizadas
- Design responsivo (funciona em desktop e mobile)
- Cards interativos com métricas
- Cores e hover effects para melhor experiência

### 📦 Consultas Implementadas
- Produto	Preço	Categoria	Estoque
- Teclado Mecânico	R$ 250,00	Acessórios	10
- Mouse Gamer	R$ 150,00	Acessórios	5
- Monitor 24	R$ 1.200,00	Periféricos	3
- Headset Bluetooth	R$ 300,00	Áudio	7
- Notebook Gamer	R$ 5.000,00	Computadores	2
- SSD 1TB	R$ 600,00	Armazenamento	12
- Produto Preço 50	R$ 50,00	Eletrônicos	15

## 💻 Pré-requisitos
Antes de começar, você vai precisar ter instalado em sua máquina:
- Python 3.8+
- Git
- Pip (gerenciador de pacotes Python - já vem com o Python)

🔧 Como Executar o Projeto
### 1. Clone o repositório

# via HTTPS
```bash
git clone https://github.com/saturnbells/lojas_flask.git
```

# via SSH (se configurado)
```bash
git clone git@github.com:saturnbells/lojas_flask.git
```

# acesse a pasta do projeto
```bash
cd lojas_flask
```

### 2. Crie um ambiente virtual

# Windows (via Git Bash)
```bash
`python -m venv venv`
`source venv/Scripts/activate`
```

# Windows (via CMD ou PowerShell)
```bash
`python -m venv venv`
`venv\Scripts\activate`
```

# linux ou mac
```bash
`python3 -m venv venv`
`source venv/bin/activate`
```

### 3. Instale as dependências

# Caso tenha o ambiente virtual ativado
```bash
`pip install -r requirements.txt`
```

# Caso queira instalar o Flask diretamente
```bash
`pip install flask`
```

### 4. Execute a aplicação

# Usando o launcher do Python (Windows)
```bash
`py app.py`
```

# Ou com python padrão
```bash
`python app.py`
```

# Ou com python3 (Linux ou Mac)
```bash
`python3 app.py`
```

### 5. Acesse no navegador
Após executar, você verá uma mensagem como:

* Running on http://127.0.0.1:5000
* Running on http://192.168.0.103:5000
Abra seu navegador e acesse qualquer um destes endereços:

Endereço	Descrição
http://127.0.0.1:5000	Localhost (apenas seu computador)
http://localhost:5000	Mesmo que o endereço acima
http://192.168.0.X:5000	IP da sua rede local

# 📁 Estrutura do Projeto

lojas_flask/
├── app.py              # Aplicação principal Flask
├── requirements.txt    # Dependências do projeto
├── executar.sh         # Script de inicialização
├── .gitignore         # Arquivos ignorados pelo Git
├── static/
│   └── style.css       # Estilos CSS
├── templates/
│   └── index.html      # Template principal
└── lojas.db            # Banco de dados (criado automaticamente)

## 🛠️ Tecnologias Utilizadas

- Backend: Python 3.14+ / Flask 3.1.3
- Banco de Dados: SQLite3
- Frontend: HTML5, CSS3
- Versionamento: Git
- Ambiente: Windows / Linux / Mac

## 📊 Exemplos de Consultas SQL Implementadas

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

# 👨‍💻 Autor
saturnbells - GitHub

Desenvolvido para atividade da UNIFAVIP - Curso de Ciências da Computação

# 📝 Licença
Este projeto está sob a licença MIT - veja o arquivo LICENSE para detalhes

Desenvolvido com ❤️🪐 usando Flask e SQLite