# Usa uma imagem base oficial do Python.
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container.
WORKDIR /app

# Instala as dependências do sistema: FFmpeg (para o Whisper) e Git (para o pip).
RUN apt-get update && apt-get install -y ffmpeg git

# Copia o arquivo de requisitos para o container.
COPY requirements.txt .

# Instala as bibliotecas Python.
# O --no-cache-dir economiza espaço na imagem final.
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto dos arquivos da sua aplicação (no caso, o app.py).
COPY . .

# Expõe a porta que o Flask vai usar dentro do container.
EXPOSE 5000

# O comando que será executado quando o container iniciar.
CMD ["python", "app.py"]
