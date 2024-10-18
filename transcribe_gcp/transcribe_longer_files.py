from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech
from pydub import AudioSegment

# Autenticar com o Google Cloud
arquivo_cliente = 'credentials.json'
credenciais = service_account.Credentials.from_service_account_file(arquivo_cliente)
cliente = speech.SpeechClient(credentials=credenciais)

gcp_uri = 'gs://dia-de-escritorio/albuquerque.m4a'

# Configurações do reconhecimento
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=48000,
    language_code="pt-BR",
    use_enhanced=True,
    model='latest_short',
)

audio = speech.RecognitionAudio(uri=gcp_uri)
operation = cliente.long_running_recognize(config=config, audio=audio)

print('Processando áudio...')
response = operation.result(timeout=200)

# Exportar transcrição para um arquivo de texto
arquivo_transcricao = 'entrevista.txt'
with open(arquivo_transcricao, 'w', encoding='utf-8') as f:
    for result in response.results:
        alternative = result.alternatives[0]
        f.write(f"Confiança: {alternative.confidence}\n")
        f.write('-' * 20 + '\n')
        f.write(f"Transcrição\n")
        f.write(alternative.transcript + '\n\n')

print(f"Transcrição exportada para {arquivo_transcricao}.")