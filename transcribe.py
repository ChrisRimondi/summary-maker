import os
from pydub import AudioSegment
import speech_recognition as sr
from multiprocessing import Pool
#import time

def split_audio(wav_filename, chunk_length=60000):
    audio = AudioSegment.from_wav(wav_filename)
    chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]
    chunk_filenames = []
    for i, chunk in enumerate(chunks):
        chunk_filename = f'chunk_{i}.wav'
        chunk.export(chunk_filename, format="wav")
        chunk_filenames.append(chunk_filename)
    return chunk_filenames

def transcribe_chunk(chunk_filename):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(chunk_filename)
    with audio_file as source:
        audio = recognizer.record(source)
    transcription = recognizer.recognize_sphinx(audio)
    os.remove(chunk_filename)
    return transcription

def transcribe_audio_locally(wav_filename, num_workers=os.cpu_count()):
    chunk_filenames = split_audio(wav_filename)
    with Pool(num_workers) as pool:
        transcriptions = pool.map(transcribe_chunk, chunk_filenames)
    return ' '.join(transcriptions)
