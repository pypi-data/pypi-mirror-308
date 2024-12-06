import os
import random
from pydub import AudioSegment
from .transcribe import (transcribe)

# segment according to speaker
def wav_file_segmentation(file_name, segments, language, modelSize, quantization):
    audio = AudioSegment.from_file(file_name, format="wav")
    texts = []

    folder_name = "speechlib/segments"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for i, segment in enumerate(segments):
        start = segment[0] * 1000
        end = segment[1] * 1000
        clip = audio[start:end]
        
        distinguisher = str(round(random.random() * 1000))
        file = f"{folder_name}/{distinguisher}segment{i+1}.wav"
        clip.export(file, format="wav")

        try:
            transcription, words = transcribe(file, language, modelSize, quantization)
            # old return -> [[start time, end time, transcript], [start time, end time, transcript], ..]
            texts.append([segment[0], segment[1], transcription, words])
        except Exception as e:
            print(f"Error processing segment {i+1}: {str(e)}")
        
        os.remove(file)

    return texts