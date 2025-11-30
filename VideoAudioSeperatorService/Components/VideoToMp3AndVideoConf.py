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
    """
    Converts a video file into:
      1. An audio-only file (WAV)
      2. A video-only file (MP4, without audio)
    Output filenames are based on the input filename:
      example.mp4 → example_Audio.wav  and  example_Video.mp4
    Saves files inside:
      Audio/
      Video/
    """
    if FilePath is None:
        return
    audio_output_path = f"Audio/{Filename}Audio.wav"
    video_output_path = f"Video/{Filename}Video.mp4"
    
    clip = VideoFileClip(FilePath)
    clip.audio.write_audiofile(audio_output_path)
    clip.without_audio().write_videofile(video_output_path)
    
    print(f"Audio saved at: {audio_output_path}")
    print(f"Video saved at: {video_output_path}")
    clip.close()

# Example usage (remove in production)
# if __name__ == "__main__":
#     video_to_audio_and_video_conversion(f"demoData//sample.mp4")