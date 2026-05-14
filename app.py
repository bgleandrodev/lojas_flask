import sqlite3
from flask import Flask, render_template

app = Flask(__name__)
DATABASE = 'lojas.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create table and ensure exactly 7 products exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PRODUTOS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            categoria TEXT NOT NULL,
            estoque INTEGER NOT NULL DEFAULT 0
        )
    ''')
    
    # Define the 7 products
    produtos = [
        ('Teclado Mecânico', 250.00, 'Acessórios', 10),
        ('Mouse Gamer', 150.00, 'Acessórios', 5),
        ('Monitor 24"', 1200.00, 'Periféricos', 3),
        ('Headset Bluetooth', 300.00, 'Áudio', 7),
        ('Notebook Gamer', 5000.00, 'Computadores', 2),
        ('SSD 1TB', 600.00, 'Armazenamento', 12),
        ('Produto Preço 50', 50.00, 'Eletrônicos', 15)
    ]
    
    # Reset to exactly these 7 products
    cursor.execute('DELETE FROM PRODUTOS')
    for p in produtos:
        cursor.execute('''
            INSERT INTO PRODUTOS (nome, preco, categoria, estoque)
            VALUES (?, ?, ?, ?)
        ''', p)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    
    # 1. ORDER BY queries
    asc_products = conn.execute('SELECT nome, preco FROM PRODUTOS ORDER BY preco ASC').fetchall()
    desc_products = conn.execute('SELECT nome, preco FROM PRODUTOS ORDER BY preco DESC').fetchall()
    
    # 2. Relational operators (comparison with 50.00)
    eq_50 = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco = ?', (50.00,)).fetchall()
    ne_50 = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco != ?', (50.00,)).fetchall()
    gt_50 = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco > ?', (50.00,)).fetchall()
    lt_50 = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco < ?', (50.00,)).fetchall()
    ge_50 = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco >= ?', (50.00,)).fetchall()
    le_50 = conn.execute('SELECT nome, preco FROM PRODUTOS WHERE preco <= ?', (50.00,)).fetchall()
    
    # 3. Logical operators
    logical_and = conn.execute('''
        SELECT nome, preco, estoque FROM PRODUTOS 
        WHERE preco > ? AND estoque > 0
    ''', (50.00,)).fetchall()
    
    logical_or = conn.execute('''
        SELECT nome, preco, categoria, estoque FROM PRODUTOS 
        WHERE preco < ? OR categoria = ?
    ''', (30.00, 'Eletrônicos')).fetchall()
    
    # 4. Aggregate functions
    avg_price = conn.execute('SELECT AVG(preco) as media_preco FROM PRODUTOS').fetchone()['media_preco']
    total_count = conn.execute('SELECT COUNT(*) as total FROM PRODUTOS').fetchone()['total']
    
    avg_by_category = conn.execute('''
        SELECT categoria, AVG(preco) as media_preco, COUNT(*) as quantidade 
        FROM PRODUTOS GROUP BY categoria ORDER BY categoria
    ''').fetchall()
    
    count_by_category = conn.execute('''
        SELECT categoria, COUNT(*) as quantidade FROM PRODUTOS 
        GROUP BY categoria ORDER BY categoria
    ''').fetchall()
    
    avg_in_stock = conn.execute('''
        SELECT AVG(preco) as media_preco_estoque FROM PRODUTOS WHERE estoque > 0
    ''').fetchone()['media_preco_estoque']
    
    conn.close()
    
    # Format averages for display
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)