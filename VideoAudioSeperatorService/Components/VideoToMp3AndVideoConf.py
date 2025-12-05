"""
  Documentation:
      VideoAudioSeperatorService Video to MP3 and Video Conversion Module. This module provides functionality
      to convert a video file into an audio-only file (WAV) and a video-only file (MP4 without audio).
    Returns:
        None: This function does not return any value.
"""

# Import Headers
from moviepy.editor import VideoFileClip

# functions Portion's
def video_to_audio_and_video_conversion(FilePath: str | None, Filename: str | None) -> None:
    """ Converts a video file into an audio-only file (WAV) and a video-only file (MP4 without audio).
    Args:
        FilePath (str | None): The path to the input video file.
        Filename (str | None): The base name for the output files (without extension).
    Returns:
        None: This function does not return any value.  
    """
    if FilePath is None:
        return
    audio_output_path = f"Audio/{Filename}Audio.wav"
    clip = VideoFileClip(FilePath)
    clip.audio.write_audiofile(audio_output_path)
    
    print(f"Audio saved at: {audio_output_path}")
    clip.close()

# Example usage (remove in production)
# if __name__ == "__main__":
#     video_to_audio_and_video_conversion(f"demoData//sample.mp4")