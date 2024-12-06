import torch
from .whisper_sinhala import (whisper_sinhala)
from faster_whisper import WhisperModel, BatchedInferencePipeline

def transcribe(file, language, model_size, quantization):
    transcription = ""
    words = []
    if language == "si" or language == "Si":
        transcription = whisper_sinhala(file)
        return transcription
    elif model_size in ["tiny", "small", "medium", "large", "large-v1", "large-v2", "large-v3"]:
        if torch.cuda.is_available():
            device = "cuda"
            compute_type = "int8_float16" if quantization else "float16"
        else:
            device = "cpu"
            compute_type = "int8" if quantization else "float32"
        
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        batched_model = BatchedInferencePipeline(model=model)


        if language in model.supported_languages:
            segments, info = batched_model.transcribe(file, language=language, beam_size=5, word_timestamps=True, batch_size=16)
            for segment in segments:
                transcription += segment.text + " "
                for word in segment.words:
                    words.append({
                        "word": word.word,
                        "start": word.start,
                        "end": word.end
                    })
            
            return transcription, words
        else:
            raise Exception("Language code not supported.\nThese are the supported languages:\n", model.supported_languages)
    else:
        raise Exception("only 'tiny', 'small', 'medium', 'large', 'large-v1', 'large-v2', 'large-v3' models are available.")
