ORDER_BY_ASC = "SELECT nome, preco FROM PRODUTOS ORDER BY preco ASC"
ORDER_BY_DESC = "SELECT nome, preco FROM PRODUTOS ORDER BY preco DESC"

REL_EQ = "SELECT nome, preco FROM PRODUTOS WHERE preco = ?"
REL_NE = "SELECT nome, preco FROM PRODUTOS WHERE preco != ?"
REL_GT = "SELECT nome, preco FROM PRODUTOS WHERE preco > ?"
REL_LT = "SELECT nome, preco FROM PRODUTOS WHERE preco < ?"
REL_GE = "SELECT nome, preco FROM PRODUTOS WHERE preco >= ?"
REL_LE = "SELECT nome, preco FROM PRODUTOS WHERE preco <= ?"

LOGICAL_AND = """
    SELECT nome, preco, estoque FROM PRODUTOS 
    WHERE preco > ? AND estoque > 0
"""
LOGICAL_OR = """
    SELECT nome, preco, categoria FROM PRODUTOS 
    WHERE preco < ? OR categoria = ?
"""

AVG_PRICE_ALL = "SELECT AVG(preco) as media_preco FROM PRODUTOS"
TOTAL_COUNT = "SELECT COUNT(*) as total FROM PRODUTOS"
AVG_BY_CATEGORY = """
    SELECT categoria, AVG(preco) as media_preco, COUNT(*) as quantidade 
    FROM PRODUTOS GROUP BY categoria ORDER BY categoria
"""
COUNT_BY_CATEGORY = """
    SELECT categoria, COUNT(*) as quantidade FROM PRODUTOS 
    GROUP BY categoria ORDER BY categoria
"""
AVG_IN_STOCK = "SELECT AVG(preco) as media_preco_estoque FROM PRODUTOS WHERE estoque > 0"

ALL_PRODUCTS = "SELECT * FROM PRODUTOS"