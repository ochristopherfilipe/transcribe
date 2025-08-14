# ===================================================================
# SCRIPT PARA RODAR EM UM SERVIDOR VPS
# ===================================================================

import os
import whisper
from flask import Flask, request, jsonify

# --- CONFIGURAÇÕES ---
# Define o modelo a ser usado. "large-v3" oferece a melhor qualidade.
# Para servidores com menos RAM, considere "medium" ou "base".
MODEL_SIZE = "large-v3"
# Define a porta em que o servidor irá rodar.
PORT = 5000
# Define o dispositivo para o processamento ('cuda' para GPU, 'cpu' para CPU).
# Se sua VPS não tem GPU NVIDIA, use 'cpu'.
DEVICE = "cpu" 

# --- INICIALIZAÇÃO ---
# Inicializa a aplicação do servidor Flask.
app = Flask(__name__)

# Carrega o modelo Whisper na memória (isso pode demorar alguns minutos na primeira vez).
print(f"Carregando o modelo Whisper '{MODEL_SIZE}' no dispositivo '{DEVICE}'...")
try:
    model = whisper.load_model(MODEL_SIZE, device=DEVICE)
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    print("Verifique se o FFmpeg está instalado (sudo apt install ffmpeg) e se o dispositivo está correto.")
    exit()

# --- DEFINIÇÃO DA API ---
# Define a rota '/transcribe' que o n8n irá chamar.
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        # Verifica se um arquivo foi enviado na requisição.
        if 'file' not in request.files:
            return jsonify({"error": "Nenhum arquivo de áudio foi enviado."}), 400

        audio_file = request.files['file']
        
        # Define um caminho temporário para salvar o áudio.
        temp_audio_path = f"/tmp/audio_temp_from_n8n.mp3"
        audio_file.save(temp_audio_path)
        
        print("Arquivo recebido. Iniciando a transcrição com o Whisper...")

        # Executa a transcrição do áudio.
        result = model.transcribe(temp_audio_path, language="pt", fp16=False)
        full_text = result["text"]
        
        print("Transcrição finalizada com sucesso!")

        # Remove o arquivo de áudio temporário.
        os.remove(temp_audio_path)

        # Retorna o texto transcrito para o n8n.
        return jsonify({"transcription": full_text})

    except Exception as e:
        print(f"[ERRO] Ocorreu um problema: {e}")
        return jsonify({"error": str(e)}), 500

# --- EXECUÇÃO DO SERVIDOR ---
if __name__ == '__main__':
    print(f"Servidor iniciado. Escutando em http://0.0.0.0:{PORT}")
    # O host '0.0.0.0' torna o servidor acessível externamente pelo IP da VPS.
    app.run(host='0.0.0.0', port=PORT)
