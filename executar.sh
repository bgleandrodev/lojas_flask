#!/bin/bash

echo "🚀 Iniciando projeto LOJAS_FLASK"
echo "📁 Pasta: $(pwd)"
echo ""

if ! command -v python &> /dev/null; then
    echo "❌ Python não encontrado!"
    echo "   Instale o Python em: https://www.python.org/downloads/"
    exit 1
fi
echo "✅ Python: $(python --version)"
echo ""

if ! command -v pip &> /dev/null; then
    echo "❌ Pip não encontrado!"
    echo "   Execute: python -m ensurepip"
    exit 1
fi
echo "✅ Pip: $(pip --version)"
echo ""

# instalador de todas dependências do requirements.txt
echo "📦 Instalando dependências do projeto..."
echo "   (Flask, python-dotenv, flask-limiter, pytest, flask-swagger-ui)"
pip install -r requirements.txt

echo ""
echo "✅ Dependências instaladas:"
pip list | grep -E "Flask|dotenv|limiter|pytest|swagger"
echo ""

if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado! Criando arquivo padrão..."
    echo "SECRET_KEY=dev-key-change-in-production" > .env
    echo "FLASK_ENV=development" >> .env
    echo "✅ Arquivo .env criado com configurações padrão"
    echo ""
fi

if [ -f lojas.db ]; then
    echo "📦 Banco de dados existente detectado. Será recriado automaticamente."
    echo ""
fi

echo "🎯 Iniciando servidor Flask..."
echo "🌐 Acesse: http://127.0.0.1:5000"
echo "📚 Documentação da API: http://127.0.0.1:5000/api/docs"
echo ""
echo "⚠️  Pressione Ctrl+C para parar o servidor"
echo ""

python app.py