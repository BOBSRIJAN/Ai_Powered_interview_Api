import speech_recognition as sr

def ListenAudioFromFile(file_path: str|None) -> str:
    """
    this in the ListenAudioFromFile function working explanation
    first we load the audio file and use the speech_recognition library to transcribe it,
    then we return the transcribed text as a string.
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
    
''' remove this in Production! '''
# if __name__ == "__main__":
#     result = ListenAudioFromFile("OnlyAudioData\\output_audio.wav" )
#     print(result)