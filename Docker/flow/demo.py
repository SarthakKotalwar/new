






import cv2
import pytesseract
from io import BytesIO
from PIL import Image
import numpy as np
from gtts import gTTS
import pygame
from pygame import mixer
from promptflow import tool

# Set up Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@tool
def extract_text_and_convert_to_speech(image_bytes):
    """
    Tool for extracting text from an image given its bytes and converting it to speech.
    """
    try:
        # Open the image
        img = Image.open(BytesIO(image_bytes))
        
        # Enhance image quality
        img = img.convert('RGB')
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(img, 3)
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Extract text using Tesseract OCR
        text = pytesseract.image_to_string(img).strip()  # Remove leading and trailing whitespace

        if text:
            # Initialize pygame mixer
            pygame.init()
            mixer.init()

            # Convert text to speech
            tts = gTTS(text=text, lang='en')

            # Save speech as an MP3 file
            tts.save("output.mp3")

            # Play the audio
            mixer.music.load("output.mp3")
            mixer.music.play()

            # Wait for the audio to finish playing
            while mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            return "Extracted text has been spoken and saved as output.mp3"
        else:
            return "Failed to extract text from the image."
    except Exception as e:
        return "Error: {}".format(e)

if __name__ == "__main__":
    # Read image file as bytes
    image_path = input("Please provide the path to the image file you want to extract text from: ")
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    # Perform extraction and conversion
    result = extract_text_and_convert_to_speech(image_bytes)

    # Print the result
    print(result)
