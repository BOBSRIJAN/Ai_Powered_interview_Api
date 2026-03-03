""" Module to convert voice audio files to text using WhisperModel. """
# Import Headers
from faster_whisper import WhisperModel
import io
import threading

_model = None
_model_lock = threading.Lock()

# functions Portion's
def getWhisperModel():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                _model = WhisperModel(
                    "tiny",
                    device="cpu",
                    compute_type="int8_float32"
                )
    return _model

def WhisperAudioToText(audio_bytes: bytes) -> str:
    try:
        model = getWhisperModel()

        audio_stream = io.BytesIO(audio_bytes)

        segments, info = model.transcribe(
            audio_stream,
            beam_size=1,
            best_of=1,
            vad_filter=True
        )

        return " ".join(seg.text for seg in segments).strip()

    except Exception as e:
        return f"Transcription Error: {e}"

# Example usage (remove in production)
# if __name__ == "__main__":
#     result = WhisperAudioToText(bytes)
#     print(result)