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

# Cria diretório de logs (opcional)
RUN mkdir -p /app/logs

# Expõe a porta do Flask
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PORT=5000
ENV LOG_DIR=/app/logs

# Comando para rodar a aplicação
CMD ["python", "main.py"]