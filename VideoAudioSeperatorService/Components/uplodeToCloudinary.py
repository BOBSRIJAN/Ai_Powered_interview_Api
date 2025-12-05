"""
    Documentation:
        VideoAudioSeperatorService Cloudinary Upload Module.
        This module handles the uploading of audio files to Cloudinary.
    Returns:
        dict: A dictionary containing the URLs of the uploaded audio files. 
"""

# Import Headers
import cloudinary
import cloudinary.uploader
import dotenv
import os

dotenv.load_dotenv()

# program configurations
cloudinary.config( 
  cloud_name = os.getenv('cloudinary_CLOUD_NAME'), 
  api_key = os.getenv('cloudinary_API_KEY'), 
  api_secret = os.getenv('cloudinary_API_SECRET'),
  secure = True
)

# functions Portion's
def uplodeAudioAndVideo(AudioFileName: str | None) -> dict:
    """ Uploads audio file to Cloudinary and returns the URL.
    Args:
        AudioFileName (str | None): The path to the audio file to be uploaded.
    Returns:
        dict: A dictionary containing the URL of the uploaded audio file.
    """
    
    if AudioFileName is None:
        return {}
    
    audio_response = cloudinary.uploader.upload(
        AudioFileName,
        resource_type="video"
    )
    dataDict = {
        "audiourl" : audio_response['url']
    }
    return dataDict