import os
import io
from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech
from pydub import AudioSegment

# Autenticar com o Google Cloud
arquivo_cliente = 'credentials.json'
credenciais = service_account.Credentials.from_service_account_file(arquivo_cliente)
cliente = speech.SpeechClient(credentials=credenciais)

# Transformar m4a em wav
arquivo_audio = 'albuquerque.m4a'
audio = AudioSegment.from_file(arquivo_audio, format='m4a')
arquivo_wav = arquivo_audio.replace('.m4a', '.wav')

# Verificar se o arquivo .wav não existe
if not os.path.exists(arquivo_wav):
    audio.export(arquivo_wav, format='wav')
    print(f"Arquivo exportado como {arquivo_wav}.")

# Carregar o arquivo de áudio
with io.open(arquivo_wav, 'rb') as arq:
    conteudo = arq.read()

audio = speech.RecognitionAudio(content=conteudo)

# Configurações do reconhecimento
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=48000,
    language_code="pt-BR",
    use_enhanced=True,
    model='latest_short',
)

response = cliente.recognize(config=config, audio=audio)
# print('\n'.join([result.alternatives[0].transcript for result in response.results]))
# print(response)

# Exportar transcrição para um arquivo de texto
arquivo_transcricao = 'transcricao.txt'
with open(arquivo_transcricao, 'w', encoding='utf-8') as f:
    for result in response.results:
        alternative = result.alternatives[0]
        f.write(f"Confiança: {alternative.confidence}\n")
        f.write('-' * 20 + '\n')
        f.write(f"Transcrição\n")
        f.write(alternative.transcript + '\n\n')

print(f"Transcrição exportada para {arquivo_transcricao}.")