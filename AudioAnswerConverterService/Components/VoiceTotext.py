""" Module to convert voice audio files to text using WhisperModel. """
# Import Headers
from faster_whisper import WhisperModel
import os
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

# def WhisperAudioToText(filePath: str) -> str:
#     """ Converts an audio file to text using the WhisperModel.
#             Args:
#                 filePath (str): The path to the audio file to be transcribed.
#             Returns:    
#                 str: The transcribed text from the audio file or an error message.
#     """
#     if not os.path.exists(filePath):
#         return "File not found"
#     try:
#         model = WhisperModel("tiny", device="cpu",compute_type="int8_float32")
#         segments, info = model.transcribe(
#             filePath,
#             beam_size=1,
#             best_of=1,
#             vad_filter=True,
#         )
#         final_text = ""
#         for seg in segments:
#             final_text += seg.text + " "
#         return final_text.strip()
#     except Exception as e:
#         return f"Transcription Error: {e}"

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
#     result = WhisperAudioToText("OnlyAudioData\\output_audio.wav")
#     print(result)