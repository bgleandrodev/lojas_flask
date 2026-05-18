import os
import sqlite3
import logging
from typing import List, Dict, Any, Optional
from flask import Flask, render_template, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ==================== ROTAS DE DOCUMENTAÇÃO ====================
@app.route('/api/docs')
def api_docs():
    """Documentação interativa da API"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>LOJAS API - Documentação</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 40px; }
            .container { max-width: 1200px; margin: 0 auto; }
            h1 { color: white; text-align: center; margin-bottom: 10px; font-size: 2.5em; }
            .subtitle { text-align: center; color: rgba(255,255,255,0.9); margin-bottom: 40px; }
            .endpoint { background: white; margin: 20px 0; padding: 20px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); transition: transform 0.2s; }
            .endpoint:hover { transform: translateX(10px); }
            .method { display: inline-block; padding: 5px 12px; border-radius: 6px; font-weight: bold; font-size: 14px; margin-right: 15px; }
            .get { background: #28a745; color: white; }
            .url { font-family: monospace; font-size: 18px; color: #333; font-weight: bold; }
            .description { color: #666; margin: 10px 0 10px 0; padding-left: 10px; border-left: 3px solid #28a745; }
            pre { background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 8px; overflow-x: auto; font-family: monospace; font-size: 14px; margin-top: 10px; }
            .badge { display: inline-block; background: #3498db; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-left: 10px; }
            footer { text-align: center; color: rgba(255,255,255,0.7); margin-top: 40px; padding: 20px; }
            @media (max-width: 768px) { body { padding: 20px; } .url { font-size: 14px; } }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 LOJAS API</h1>
            <div class="subtitle">API REST para gerenciamento de produtos | Rate Limit: 100 req/min</div>
            
            <div class="endpoint">
                <div><span class="method get">GET</span> <span class="url">/api/produtos</span> <span class="badge">Paginação</span></div>
                <div class="description">Lista todos os produtos com suporte a paginação</div>
                <pre>curl "http://127.0.0.1:5000/api/produtos?page=1&per_page=5"</pre>
            </div>
            
            <div class="endpoint">
                <div><span class="method get">GET</span> <span class="url">/api/produtos/buscar</span> <span class="badge">Filtros</span></div>
                <div class="description">Busca produtos por nome, categoria, faixa de preço e estoque mínimo</div>
                <pre>curl "http://127.0.0.1:5000/api/produtos/buscar?nome=teclado"</pre>
            </div>
            
            <div class="endpoint">
                <div><span class="method get">GET</span> <span class="url">/api/consultas/order_by</span></div>
                <div class="description">ORDER BY - Produtos ordenados por preço (crescente e decrescente)</div>
                <pre>curl "http://127.0.0.1:5000/api/consultas/order_by"</pre>
            </div>
            
            <div class="endpoint">
                <div><span class="method get">GET</span> <span class="url">/api/consultas/relacionais</span></div>
                <div class="description">Operadores relacionais - Comparações com o valor R$ 50,00</div>
                <pre>curl "http://127.0.0.1:5000/api/consultas/relacionais"</pre>
            </div>
            
            <div class="endpoint">
                <div><span class="method get">GET</span> <span class="url">/api/consultas/logicas</span></div>
                <div class="description">Operadores lógicos - AND (preço > 50 AND estoque > 0) e OR (preço < 30 OR categoria = 'Eletrônicos')</div>
                <pre>curl "http://127.0.0.1:5000/api/consultas/logicas"</pre>
            </div>
            
            <div class="endpoint">
                <div><span class="method get">GET</span> <span class="url">/api/consultas/agregacoes</span></div>
                <div class="description">Funções de agregação - Média total, contagem, média por categoria, GROUP BY</div>
                <pre>curl "http://127.0.0.1:5000/api/consultas/agregacoes"</pre>
            </div>
            
            <footer>
                🔒 Headers de segurança ativos | 📝 Desenvolvido por saturnbells | 🐍 Flask + SQLite
            </footer>
        </div>
    </body>
    </html>
    '''

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

# ==================== CONFIGURAÇÕES ====================
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
DEBUG = os.getenv('FLASK_ENV') == 'development'

limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"], storage_uri="memory://")

DATABASE = 'lojas.db'

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
    produtos = [
        ('Teclado Mecânico', 250.00, 'Acessórios', 10),
        ('Mouse Gamer', 150.00, 'Acessórios', 5),
        ('Monitor 24"', 1200.00, 'Periféricos', 3),
        ('Headset Bluetooth', 300.00, 'Áudio', 7),
        ('Notebook Gamer', 5000.00, 'Computadores', 2),
        ('SSD 1TB', 600.00, 'Armazenamento', 12),
        ('Produto Preço 50', 50.00, 'Eletrônicos', 15)
    ]
    cursor.execute('DELETE FROM PRODUTOS')
    for p in produtos:
        cursor.execute('INSERT INTO PRODUTOS (nome, preco, categoria, estoque) VALUES (?, ?, ?, ?)', p)
    conn.commit()
    conn.close()
    logger.info("Banco inicializado com 7 produtos")

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

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
        avg_in_stock=avg_in_stock
    )

@app.route('/api/produtos')
@limiter.limit("100 per minute")
def api_produtos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    page = max(1, page)
    per_page = min(max(1, per_page), 50)
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
    per_page = request.args.get('per_page', 10, type=int)
    page = max(1, page)
    per_page = min(max(1, per_page), 50)
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

if __name__ == '__main__':
    init_db()
    logger.info(f"Iniciando servidor Flask em modo {'DEBUG' if DEBUG else 'PRODUÇÃO'}")
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)