"""
  Documentation:
      VideoAudioSeperatorService Video to MP3 and Video Conversion Module. This module provides functionality
      to convert a video file into an audio-only file (WAV) and a video-only file (MP4 without audio).
    Returns:
        str: The path to the generated audio file (WAV).
"""

# Import Headers
import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger: logging = logging.getLogger("python")

# functions Portion's
def videoToAudioConverter (video_path: str, audio_path: str) -> str:
    """ Converts a video file into an audio-only file (WAV) and a video-only file (MP4 without audio).
    Args:
        FilePath (str | None): The path to the input video file.
        Filename (str | None): The base name for the output files (without extension).
    Returns:
        str: The path to the generated audio file (WAV).  
    """
    
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Input video file does not exist: {video_path}")
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)

    logger.info(f"Extracting Whisper-compatible audio from: {video_path}")
    command = ["ffmpeg", "-y", "-i", video_path, "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", audio_path]
    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed:\n{result.stderr.decode()}")

    logger.info(f"Audio ready for Whisper: {audio_path}")
    return audio_path

# Example usage (remove in production)
# if __name__ == "__main__":
#     videoToAudioConverter(f"demoData//sample.mp4")