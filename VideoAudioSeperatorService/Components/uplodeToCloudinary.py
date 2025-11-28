"""
    Documentation:
        VideoAudioSeperatorService Cloudinary Upload Module.
        This module handles the uploading of video and audio files to Cloudinary.
    Returns:
        dict: A dictionary containing the URLs of the uploaded video and audio files. 
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
def uplodeAudioAndVideo(VideoFileName: str | None, AudioFileName: str | None) -> dict:
    """Uploads video and audio files to Cloudinary and returns their URLs.
        Args:
            VideoFileName (str | None): Path to the video file to be uploaded.
            AudioFileName (str | None): Path to the audio file to be uploaded.
        Returns:
            dict: A dictionary containing the URLs of the uploaded video and audio files.
        """
    video_response = cloudinary.uploader.upload(
        VideoFileName,
        resource_type="video"
    )
    audio_response = cloudinary.uploader.upload(
        AudioFileName,
        resource_type="video"
    )
    dataDict = {
        "videourl" : video_response['url'],
        "audiourl" : audio_response['url']
    }
    return dataDict