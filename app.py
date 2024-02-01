from flask import Flask, render_template, Response
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate_audio():
    command = "parec --device=alsa_output.platform-bcm2835_audio.analog-stereo.monitor | sox -t raw -r 44100 -e signed -b 16 -c 2 - -t wav -"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        # Read audio data in chunks
        audio_chunk = process.stdout.read(1024)
        if not audio_chunk:
            break
        yield audio_chunk

@app.route('/audio')
def audio():
    return Response(generate_audio(), mimetype='audio/x-wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
