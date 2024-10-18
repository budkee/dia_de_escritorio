import os
from flask import Flask, request, jsonify, send_from_directory
from google.cloud import speech
from werkzeug.utils import secure_filename
from pydub import AudioSegment

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 60 * 1024 * 1024  # Limite de 60MB

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

    
@app.route('/uploads', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Converter para .wav se o arquivo não for .wav
        if not filename.lower().endswith('.wav'):
            wav_file_path = os.path.splitext(file_path)[0] + '.wav'
            convert_m4a_to_wav(file_path, wav_file_path)
            file_path = wav_file_path
        
        transcription = transcribe_audio(file_path)
        return jsonify({'transcription': transcription}), 200


def convert_m4a_to_wav(m4a_file_path, wav_file_path):
    audio = AudioSegment.from_file(m4a_file_path, format="m4a")
    audio.export(wav_file_path, format="wav")
    print(f"Conversão concluída: {wav_file_path}")

def transcribe_audio(file_path):
    client = speech.SpeechClient()
    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="pt-BR",
    )

    response = client.recognize(config=config, audio=audio)

    return '\n'.join([result.alternatives[0].transcript for result in response.results])

if __name__ == '__main__':
    app.run(debug=True)
