# Imagem base do Python
FROM python:3.14-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de dependências primeiro (melhor cache)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do projeto
COPY . .

# Expõe a porta do Flask
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Comando para rodar a aplicação
CMD ["python", "app.py"]