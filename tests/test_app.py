import unittest
import json
import sys
import os

# adiciona o diretório pai ao path para importar o app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestLojasAPI(unittest.TestCase):
    """Testes para a API LOJAS"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_page(self):
        """Testa se a página inicial carrega"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'LOJAS', response.data)
    
    def test_api_produtos(self):
        """Testa endpoint /api/produtos"""
        response = self.app.get('/api/produtos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 7)
        self.assertIn('nome', data[0])
        self.assertIn('preco', data[0])
    
    def test_api_order_by_asc(self):
        """Testa ORDER BY crescente"""
        response = self.app.get('/api/consultas/order_by')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        precos = [p['preco'] for p in data['crescente']]
        self.assertEqual(precos, sorted(precos))
    
    def test_api_order_by_desc(self):
        """Testa ORDER BY decrescente"""
        response = self.app.get('/api/consultas/order_by')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        precos = [p['preco'] for p in data['decrescente']]
        self.assertEqual(precos, sorted(precos, reverse=True))
    
    def test_api_relacionais_igual(self):
        """Testa operador igual (=) com 50.00"""
        response = self.app.get('/api/consultas/relacionais')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        produtos_igual = data['igual']
        self.assertTrue(any(p['nome'] == 'Produto Preço 50' for p in produtos_igual))
    
    def test_api_logicas_and(self):
        """Testa operador lógico AND"""
        response = self.app.get('/api/consultas/logicas')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        for p in data['and']:
            self.assertGreater(p['preco'], 50)
            self.assertGreater(p['estoque'], 0)
    
    def test_api_agregacoes(self):
        """Testa endpoints de agregações"""
        response = self.app.get('/api/consultas/agregacoes')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('media_total', data)
        self.assertIn('contagem_total', data)
        self.assertEqual(data['contagem_total'], 7)

if __name__ == '__main__':
    unittest.main()