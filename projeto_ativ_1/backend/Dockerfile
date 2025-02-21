# Imagem base para o FastAPI
FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código fonte para dentro do container
COPY . .

# Expor a porta que o FastAPI usará
EXPOSE 8000

# Comando para iniciar o FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
