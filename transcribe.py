import os
from pydub import AudioSegment
import speech_recognition as sr
from multiprocessing import Pool

def split_audio(wav_filename: str, chunk_length: int = 60000) -> list:
    """
    Split an audio file into chunks.
    
    Args:
        wav_filename (str): The path to the wav file.
        chunk_length (int): The length of each chunk in milliseconds.
        
    Returns:
        list: A list of chunk filenames.
    """
    audio = AudioSegment.from_wav(wav_filename)
    chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]
    chunk_filenames = []
    for i, chunk in enumerate(chunks):
        chunk_filename = f'chunk_{i}.wav'
        chunk.export(chunk_filename, format="wav")
        chunk_filenames.append(chunk_filename)
    return chunk_filenames

def transcribe_chunk(chunk_filename: str) -> str:
    """
    Transcribe a chunk of audio.
    
    Args:
        chunk_filename (str): The path to the audio chunk file.
        
    Returns:
        str: The transcription of the audio chunk.
    """
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(chunk_filename)
    with audio_file as source:
        audio = recognizer.record(source)
    transcription = recognizer.recognize_sphinx(audio)
    os.remove(chunk_filename)
    return transcription

def transcribe_audio_locally(wav_filename: str, num_workers: int = os.cpu_count()) -> str:
    """
    Transcribe an entire audio file using local processing.
    
    Args:
        wav_filename (str): The path to the wav file.
        num_workers (int): The number of worker processes to use.
        
    Returns:
        str: The combined transcription of the entire audio file.
    """
    chunk_filenames = split_audio(wav_filename)
    with Pool(num_workers) as pool:
        transcriptions = pool.map(transcribe_chunk, chunk_filenames)
    return ' '.join(transcriptions)