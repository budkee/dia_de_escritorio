FROM python:3.12-slim

# Instalar ffmpeg e outras dependências do sistema
RUN apt-get update && apt-get install -y --fix-missing \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Configurar a variável de ambiente do Google Cloud (opcional, se você usar credenciais específicas)
ENV GOOGLE_APPLICATION_CREDENTIALS=./credentials.json

EXPOSE 5001
CMD [ "gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
