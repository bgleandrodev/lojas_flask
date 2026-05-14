#!/bin/bash
echo "🚀 Iniciando projeto LOJAS_FLASK"
echo "📁 Pasta: $(pwd)"

# verificando se o python está instalado
if ! command -v python &> /dev/null; then
    echo "❌ Python não encontrado!"
    exit 1
fi
echo "✅ Python: $(python --version)"

# instala o flask, verifica se a instalação está corrreta e executa a aplicação
echo "📦 Instalando Flask..."
pip install flask

echo "✅ Flask instalado:"
pip show flask | grep Version

echo "🎯 Executando aplicação..."
echo "🌐 Acesse: http://127.0.0.1:5000"
python app.py