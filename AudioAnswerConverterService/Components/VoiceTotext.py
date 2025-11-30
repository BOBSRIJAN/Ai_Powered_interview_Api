""" Module to convert voice audio files to text using speech recognition. """
# Import Headers
import speech_recognition as sr

# functions Portion's
def ListenAudioFromFile(file_path: str|None) -> str:
    """
    Converts an audio file to text using Google's speech recognition.
        Args:
            file_path (str|None): Path to the audio file to be converted.
        Returns:
            str: The transcribed text from the audio file.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        return text
    
    except sr.UnknownValueError:
        print("System could not understand the audio in the file.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; check internet connection: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage (remove in production)
# if __name__ == "__main__":
#     result = ListenAudioFromFile("OnlyAudioData\\output_audio.wav" )
#     print(result)