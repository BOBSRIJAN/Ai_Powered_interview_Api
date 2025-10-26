from moviepy.editor import VideoFileClip

def video_to_audio_and_video_conversion(FilePath: str | None, Filename: str | None) -> None:
    """
    Converts a video file into:
      1. An audio-only file (WAV)
      2. A video-only file (MP4, without audio)
    Output filenames are based on the input filename:
      example.mp4 → example_Audio.wav  and  example_Video.mp4
    Saves files inside:
      Hendelar/Audio/
      Hendelar/Video/
    """
    if FilePath is None:
        return
    audio_output_path = f"Hendelar/Audio/{Filename}_Audio.wav"
    video_output_path = f"Hendelar/Video/{Filename}_Video.mp4"
    clip = VideoFileClip(FilePath)
    clip.audio.write_audiofile(audio_output_path)
    clip.without_audio().write_videofile(video_output_path)
    print(f"Audio saved at: {audio_output_path}")
    print(f"Video saved at: {video_output_path}")
    clip.close()

''' remove this in Production! '''
# if __name__ == "__main__":
#     video_to_audio_and_video_conversion(f"demoData//sample.mp4")