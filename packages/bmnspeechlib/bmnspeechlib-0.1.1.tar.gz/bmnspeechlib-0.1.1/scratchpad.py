from bmnspeechlib import Transcriptor
from IPython import embed

transcribe = Transcriptor(
    file="/home/bmarsh/TRUE/bmnspeechlib/audio_for_testing/audio_chunks_local_post_live/audio_chunk_086.wav",
    log_folder="transcripts",
    language="en",
    modelSize="medium",
    pyannote_model = "pyannote/speaker-diarization-3.1",
    max_speakers = 4,
    voices_folder="/home/bmarsh/TRUE/bmnspeechlib/audio_for_testing/voices_LIVE",
    hf_token = "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"
)

results, transcript_string, possible_overlaps = transcribe.transcribe()
embed()