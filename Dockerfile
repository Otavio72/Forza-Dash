# Base leve
FROM python:3.11-slim

# Evita buffering do Python
ENV PYTHONUNBUFFERED=1

# Cria diretório e define como pasta de trabalho
WORKDIR /app

# Copia os arquivos de dependência e instala
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do projeto
COPY . .

# Expõe a porta usada pelo FastAPI
EXPOSE 8000

# Roda as migrações automaticamente antes de iniciar o app
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000

