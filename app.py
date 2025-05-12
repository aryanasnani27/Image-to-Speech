from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import pytesseract
from gtts import gTTS
from playsound import playsound
import os
import pygame
import numpy as np
import threading
import signal
import sys

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize pygame audio
pygame.mixer.init()

app = Flask(__name__)

# Function to extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    # Open the image file
    image = Image.open(image_path)
    # Use pytesseract to extract text
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

# Function to convert text into speech using gTTS and pygame
def convert_text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    # Save the audio file
    audio_file = 'output.mp3'
    tts.save(audio_file)
    # Load and play the audio file with pygame
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Function to stop the audio playback
def stop_audio():
    pygame.mixer.music.stop()

# Function to restart the Flask server
def restart_server():
    python = sys.executable
    os.execl(python, python, *sys.argv)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return redirect(request.url)

    # Get the image file
    image_file = request.files['image']
    if image_file.filename == '':
        return redirect(request.url)

    # Save the image file temporarily
    image_path = 'temp_image.jpg'
    image_file.save(image_path)

    # Extract text from the image
    extracted_text = extract_text_from_image(image_path)

    # Convert extracted text to speech
    convert_text_to_speech(extracted_text)

    return redirect(url_for('index'))

@app.route('/end_task', methods=['POST'])
def end_task():
    stop_audio()
    restart_server()
    return 'Server restarting...'

if __name__ == '__main__':
    app.run(debug=True)
