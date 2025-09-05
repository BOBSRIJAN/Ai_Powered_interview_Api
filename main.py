from Components import CvToText
from Components import geminiAi
from Components import VideoToMp3AndVideoConf
from Components import VoiceTotext
import dotenv
import os

dotenv.load_dotenv()

''' This is the main entry point of all the components '''
if __name__=="__main__":
    '''test done!'''
    cvText = CvToText.CvToSimpleText.extractTextFromPdf(f'demoData\\srijanraycv.pdf')
    cvText += os.getenv('JsonDataFormat')
    data = geminiAi.Era_assistant(cvText)
    print(data.replace("```", "").replace("json", ""))
    
    '''test done!'''
    VideoToMp3AndVideoConf.video_to_audio_and_video_conversion(f"demoData\\sample.mp4")

    '''test done!'''
    result = VoiceTotext.ListenAudioFromFile("OnlyAudioData\\output_audio.wav" )
    print(result)