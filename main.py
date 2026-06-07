import os
import sys
import sqlite3
import logging
from typing import List, Dict, Any, Optional
from flask import Flask, render_template, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# importa a configuração centralizada
from config import app_config

# ==================== CONFIGURAÇÃO DE LOGGING ====================
# diretório de logs
log_dir = os.environ.get('LOG_DIR', app_config.log_dir if os.path.exists(app_config.log_dir) else '.')
log_file = os.path.join(log_dir, app_config.log_file)

# caso o diretório não exista, tenta criar um
try:
    os.makedirs(log_dir, exist_ok=True)
except (PermissionError, OSError):
    log_dir = '.'
    log_file = app_config.log_file

# configuração dos handlers de log
handlers = [logging.StreamHandler(sys.stdout)]

# adiciona file handler apenas se tiver permissão
try:
    file_handler = logging.FileHandler(log_file)
    handlers.append(file_handler)
except (PermissionError, OSError):
    pass

# usa o formato lido do config
logging.basicConfig(
    level=app_config.get_log_level(),
    format=app_config.log_format,
    handlers=handlers
)
logger = logging.getLogger(__name__)

logger.info("Iniciando aplicação.")

app = Flask(__name__)

# ==================== CONFIGURAÇÕES DE SEGURANÇA ====================
app.secret_key = app_config.secret_key
DEBUG = app_config.debug

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

DATABASE = app_config.database_path


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PRODUTOS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            categoria TEXT NOT NULL,
            estoque INTEGER NOT NULL DEFAULT 0
        )
    ''')

    if app_config.init_products:
        produtos = [
            ('Teclado Mecânico', 250.00, 'Acessórios', 10),
            ('Mouse Gamer', 150.00, 'Acessórios', 5),
            ('Monitor 24"', 1200.00, 'Periféricos', 3),
            ('Headset Bluetooth', 300.00, 'Áudio', 7),
            ('Notebook Gamer', 5000.00, 'Computadores', 2),
            ('SSD 1TB', 600.00, 'Armazenamento', 12),
            ('Kit de Organização de Cabos', 50.00, 'Eletrônicos', 15)
        ]
        cursor.execute('DELETE FROM PRODUTOS')
        for p in produtos:
            cursor.execute('INSERT INTO PRODUTOS (nome, preco, categoria, estoque) VALUES (?, ?, ?, ?)', p)
        logger.info("Banco inicializado com 7 produtos")

    conn.commit()
    conn.close()


# ==================== HEADERS DE SEGURANÇA ====================
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response


# ==================== ROTAS DE DOCUMENTAÇÃO ====================
@app.route('/api/docs')
def api_docs():
    """Documentação interativa da API"""
    return render_template('api_docs.html')


# ==================== ROTAS DE TESTE ====================
@app.route('/teste123')
def teste123():
    return "Teste funcionou!"


@app.route('/apidoc')
def apidoc():
    return "<h1>FUNCIONOU!</h1><p>Rota /apidoc está funcionando.</p>"


@app.route('/api/documentacao')
def api_documentacao():
    return "<h1>Documentação da API</h1><p>Rota alternativa funcionando!</p>"


# ==================== ROTA PRINCIPAL ====================
@app.route('/')
def index():
    conn = get_db_connection()
    asc_products = conn.execute('SELECT nome, preco FROM PRODUTOS ORDER BY preco ASC').fetchall()
    desc_products = conn.execute('SELECT nome, preco FROM PRODUTOS ORDER BY preco DESC').fetchall()
    eq_50 = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco = ?', (50.00,)).fetchall()
    ne_50 = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco != ?', (50.00,)).fetchall()
    gt_50 = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco > ?', (50.00,)).fetchall()
    lt_50 = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco < ?', (50.00,)).fetchall()
    ge_50 = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco >= ?', (50.00,)).fetchall()
    le_50 = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco <= ?', (50.00,)).fetchall()
    logical_and = conn.execute('SELECT nome, preco, estoque FROM PRODUTOS WHERE preco > ? AND estoque > 0', (50.00,)).fetchall()
    logical_or = conn.execute('SELECT nome, preco, categoria FROM PRODUTOS WHERE preco < ? OR categoria = ?', (30.00, 'Eletrônicos')).fetchall()
    avg_price = conn.execute('SELECT AVG(preco) as media_preco FROM PRODUTOS').fetchone()['media_preco']
    total_count = conn.execute('SELECT COUNT(*) as total FROM PRODUTOS').fetchone()['total']
    avg_by_category = conn.execute('SELECT categoria, AVG(preco) as media_preco, COUNT(*) as quantidade FROM PRODUTOS GROUP BY categoria ORDER BY categoria').fetchall()
    count_by_category = conn.execute('SELECT categoria, COUNT(*) as quantidade FROM PRODUTOS GROUP BY categoria ORDER BY categoria').fetchall()
    avg_in_stock = conn.execute('SELECT AVG(preco) as media_preco_estoque FROM PRODUTOS WHERE estoque > 0').fetchone()['media_preco_estoque']
    conn.close()
    avg_price = round(avg_price, 2) if avg_price else 0
    avg_in_stock = round(avg_in_stock, 2) if avg_in_stock else 0
    return render_template('index.html',
                           asc_products=asc_products, desc_products=desc_products,
                           eq_50=eq_50, ne_50=ne_50, gt_50=gt_50, lt_50=lt_50, ge_50=ge_50, le_50=le_50,
                           logical_and=logical_and, logical_or=logical_or,
                           avg_price=avg_price, total_count=total_count,
                           avg_by_category=avg_by_category, count_by_category=count_by_category,
                           avg_in_stock=avg_in_stock)


# ==================== API REST ====================
@app.route('/api/produtos')
@limiter.limit("100 per minute")
def api_produtos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', app_config.pagination_per_page, type=int)
    page = max(1, page)
    per_page = min(max(1, per_page), app_config.max_per_page)
    offset = (page - 1) * per_page
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM PRODUTOS LIMIT ? OFFSET ?', (per_page, offset)).fetchall()
    total = conn.execute('SELECT COUNT(*) as total FROM PRODUTOS').fetchone()['total']
    conn.close()
    return jsonify({
        'page': page, 'per_page': per_page, 'total': total,
        'total_pages': (total + per_page - 1) // per_page,
        'data': [dict(row) for row in produtos]
    })


@app.route('/api/produtos/buscar')
@limiter.limit("100 per minute")
def buscar_produtos():
    nome = request.args.get('nome', '')
    categoria = request.args.get('categoria', '')
    min_preco = request.args.get('min_preco', type=float)
    max_preco = request.args.get('max_preco', type=float)
    min_estoque = request.args.get('min_estoque', type=int)
    query = 'SELECT * FROM PRODUTOS WHERE 1=1'
    params = []
    if nome:
        query += ' AND nome LIKE ?'
        params.append(f'%{nome}%')
    if categoria:
        query += ' AND categoria = ?'
        params.append(categoria)
    if min_preco is not None:
        query += ' AND preco >= ?'
        params.append(min_preco)
    if max_preco is not None:
        query += ' AND preco <= ?'
        params.append(max_preco)
    if min_estoque is not None:
        query += ' AND estoque >= ?'
        params.append(min_estoque)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', app_config.pagination_per_page, type=int)
    page = max(1, page)
    per_page = min(max(1, per_page), app_config.max_per_page)
    offset = (page - 1) * per_page
    conn = get_db_connection()
    count_query = query.replace('SELECT *', 'SELECT COUNT(*) as total')
    total = conn.execute(count_query, params).fetchone()['total']
    query += ' LIMIT ? OFFSET ?'
    params.extend([per_page, offset])
    produtos = conn.execute(query, params).fetchall()
    categorias = conn.execute('SELECT DISTINCT categoria FROM PRODUTOS ORDER BY categoria').fetchall()
    conn.close()
    return jsonify({
        'filters': {'nome': nome or None, 'categoria': categoria or None,
                    'min_preco': min_preco, 'max_preco': max_preco, 'min_estoque': min_estoque},
        'pagination': {'page': page, 'per_page': per_page, 'total': total,
                       'total_pages': (total + per_page - 1) // per_page},
        'categorias_disponiveis': [c['categoria'] for c in categorias],
        'data': [dict(row) for row in produtos]
    })


@app.route('/api/consultas/order_by')
@limiter.limit("100 per minute")
def api_order_by():
    conn = get_db_connection()
    asc = conn.execute('SELECT nome, preco FROM PRODUTOS ORDER BY preco ASC').fetchall()
    desc = conn.execute('SELECT nome, preco FROM PRODUTOS ORDER BY preco DESC').fetchall()
    conn.close()
    return jsonify({'crescente': [dict(row) for row in asc], 'decrescente': [dict(row) for row in desc]})


@app.route('/api/consultas/relacionais')
@limiter.limit("100 per minute")
def api_relacionais():
    conn = get_db_connection()
    eq = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco = 50.00').fetchall()
    ne = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco != 50.00').fetchall()
    gt = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco > 50.00').fetchall()
    lt = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco < 50.00').fetchall()
    ge = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco >= 50.00').fetchall()
    le = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco <= 50.00').fetchall()
    conn.close()
    return jsonify({
        'igual': [dict(row) for row in eq], 'diferente': [dict(row) for row in ne],
        'maior': [dict(row) for row in gt], 'menor': [dict(row) for row in lt],
        'maior_igual': [dict(row) for row in ge], 'menor_igual': [dict(row) for row in le]
    })


@app.route('/api/consultas/logicas')
@limiter.limit("100 per minute")
def api_logicas():
    conn = get_db_connection()
    and_op = conn.execute('SELECT nome, preco, estoque FROM PRODUTOS WHERE preco > 50 AND estoque > 0').fetchall()
    or_op = conn.execute('SELECT nome, preco, categoria FROM PRODUTOS WHERE preco < 30 OR categoria = "Eletrônicos"').fetchall()
    conn.close()
    return jsonify({'and': [dict(row) for row in and_op], 'or': [dict(row) for row in or_op]})


@app.route('/api/consultas/agregacoes')
@limiter.limit("100 per minute")
def api_agregacoes():
    conn = get_db_connection()
    media_total = conn.execute('SELECT AVG(preco) as media FROM PRODUTOS').fetchone()['media']
    contagem = conn.execute('SELECT COUNT(*) as total FROM PRODUTOS').fetchone()['total']
    media_estoque = conn.execute('SELECT AVG(preco) as media FROM PRODUTOS WHERE estoque > 0').fetchone()['media']
    media_categoria = conn.execute('SELECT categoria, AVG(preco) as media, COUNT(*) as qtd FROM PRODUTOS GROUP BY categoria').fetchall()
    conn.close()
    return jsonify({
        'media_total': round(media_total, 2) if media_total else 0,
        'contagem_total': contagem,
        'media_estoque': round(media_estoque, 2) if media_estoque else 0,
        'media_por_categoria': [dict(row) for row in media_categoria]
    })


# ==================== IA - RECOMENDAÇÃO DE PRODUTOS ====================
from ai_service import ai_service


@app.route('/api/recomendar', methods=['POST'])
@limiter.limit("10 per minute")
def recomendar_produtos():
    """Recomenda produtos baseado em uma consulta em linguagem natural"""
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({"erro": "Campo 'query' é obrigatório"}), 400

    user_query = data['query'].strip()
    if not user_query:
        return jsonify({"erro": "Consulta não pode estar vazia"}), 400

    conn = get_db_connection()
    products = conn.execute('SELECT id, nome, preco, categoria, estoque FROM PRODUTOS').fetchall()
    conn.close()

    products_list = [dict(p) for p in products]

    if not ai_service.is_available():
        return jsonify({
            "consulta": user_query,
            "recomendacao": "Serviço de IA não configurado. Configure OPENROUTER_API_KEY no arquivo .env",
            "produtos_disponiveis": len(products_list),
            "aviso": "IA não disponível"
        })

    recommendation = ai_service.recommend_products(user_query, products_list)

    return jsonify({
        "consulta": user_query,
        "recomendacao": recommendation,
        "produtos_disponiveis": len(products_list)
    })


@app.route('/api/produto/descricao/<int:product_id>', methods=['GET'])
@limiter.limit("20 per minute")
def gerar_descricao_produto(product_id: int):
    """Gera uma descrição criativa para um produto específico"""

    conn = get_db_connection()
    produto = conn.execute(
        'SELECT id, nome, preco, categoria FROM PRODUTOS WHERE id = ?',
        (product_id,)
    ).fetchone()
    conn.close()

    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    try:
        if ai_service.is_available():
            descricao = ai_service.generate_description(
                produto['nome'],
                produto['categoria'],
                produto['preco']
            )
            aviso = None
        else:
            descricao = f"{produto['nome']} - {produto['categoria']} - R${produto['preco']:.2f}"
            aviso = "IA não configurada. Configure OPENROUTER_API_KEY no arquivo .env"

        return jsonify({
            "produto": dict(produto),
            "descricao_gerada": descricao,
            "aviso": aviso
        })
    except Exception as e:
        logger.error(f"Erro ao gerar descrição: {e}")
        return jsonify({
            "produto": dict(produto),
            "descricao_gerada": f"{produto['nome']} - {produto['categoria']} - R${produto['preco']:.2f}",
            "erro": str(e)
        })


@app.route('/teste-ia')
def teste_ia():
    return render_template('teste_ia.html')


@app.route('/api/memoria/limpar', methods=['POST'])
def limpar_memoria():
    """Limpa a memória da conversa (inicia nova sessão)"""
    ai_service.clear_memory()
    return jsonify({"status": "sucesso", "mensagem": "Memória de conversa reiniciada"})


if __name__ == '__main__':
    init_db()
    logger.info(f"Iniciando servidor Flask em modo {'DEBUG' if DEBUG else 'PRODUÇÃO'}")
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)