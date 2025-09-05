from moviepy.editor import VideoFileClip

def video_to_audio_and_video_conversion(FilePath : str | None) -> None:
    """
        this in the video_to_audio_and_video_conversion function working explanation
        This function takes a video file as input and converts it into two separate files: 
        one audio file (MP3) and one video file (MP4) without audio.
    """
    if FilePath is None:
        return
    clip = VideoFileClip(FilePath)
    clip.audio.write_audiofile("OnlyAudioData//output_audio.wav")
    clip.without_audio().write_videofile("OnlyVideoData//output_video.mp4")

''' remove this in Production! '''
# if __name__ == "__main__":
#     video_to_audio_and_video_conversion(f"demoData//sample.mp4")