import os
import sqlite3
from typing import List, Dict, Any, Optional
from flask import Flask, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
# debug mode
DEBUG = os.getenv('FLASK_ENV') == 'development'

# rate limiting (CORRIGIDO)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

DATABASE = 'lojas.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create table and ensure exactly 7 products exist."""
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
        cursor.execute('''
            INSERT INTO PRODUTOS (nome, preco, categoria, estoque)
            VALUES (?, ?, ?, ?)
        ''', p)
    
    conn.commit()
    conn.close()

@app.after_request
def add_security_headers(response):
    """Adiciona headers HTTP para mitigar vulnerabilidades comuns."""
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
    
    return render_template(
        'index.html',
        asc_products=asc_products,
        desc_products=desc_products,
        eq_50=eq_50,
        ne_50=ne_50,
        gt_50=gt_50,
        lt_50=lt_50,
        ge_50=ge_50,
        le_50=le_50,
        logical_and=logical_and,
        logical_or=logical_or,
        avg_price=avg_price,
        total_count=total_count,
        avg_by_category=avg_by_category,
        count_by_category=count_by_category,
        avg_in_stock=avg_in_stock
    )

@app.route('/api/produtos')
@limiter.limit("100 per minute")
def api_produtos():
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM PRODUTOS').fetchall()
    conn.close()
    return jsonify([dict(row) for row in produtos])

@app.route('/api/consultas/order_by')
@limiter.limit("100 per minute")
def api_order_by():
    conn = get_db_connection()
    asc = conn.execute('SELECT nome, preco FROM PRODUTOS ORDER BY preco ASC').fetchall()
    desc = conn.execute('SELECT nome, preco FROM PRODUTOS ORDER BY preco DESC').fetchall()
    conn.close()
    return jsonify({
        'crescente': [dict(row) for row in asc],
        'decrescente': [dict(row) for row in desc]
    })

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
        'igual': [dict(row) for row in eq],
        'diferente': [dict(row) for row in ne],
        'maior': [dict(row) for row in gt],
        'menor': [dict(row) for row in lt],
        'maior_igual': [dict(row) for row in ge],
        'menor_igual': [dict(row) for row in le]
    })

@app.route('/api/consultas/logicas')
@limiter.limit("100 per minute")
def api_logicas():
    conn = get_db_connection()
    and_op = conn.execute('SELECT nome, preco, estoque FROM PRODUTOS WHERE preco > 50 AND estoque > 0').fetchall()
    or_op = conn.execute('SELECT nome, preco, categoria FROM PRODUTOS WHERE preco < 30 OR categoria = "Eletrônicos"').fetchall()
    conn.close()
    return jsonify({
        'and': [dict(row) for row in and_op],
        'or': [dict(row) for row in or_op]
    })

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
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)