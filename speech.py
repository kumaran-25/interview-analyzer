import speech_recognition as sr
from moviepy import VideoFileClip
import os

def extract_audio(video_path):
    """Converts video to a temporary wav file and closes the file handle."""
    audio_path = "temp_audio.wav"
    
    # Using 'with' ensures the video file is closed as soon as we are done
    with VideoFileClip(video_path) as video:
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
    
    return audio_path

def speech_to_text(audio_path):
    """Transcribes audio file to text using Google Speech Recognition."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Audio was detected but could not be understood."
    except sr.RequestError:
        return "Could not request results from the speech recognition service."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def count_filler_words(text):
    """Analyzes text for common filler words."""
    fillers = ["um", "uh", "like", "actually", "basically", "you know"]
    words = text.lower().split()
    report = {word: words.count(word) for word in fillers if words.count(word) > 0}
    return report