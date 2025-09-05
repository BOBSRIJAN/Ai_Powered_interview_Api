from moviepy.editor import VideoFileClip

def video_to_audio_and_video_conversion(FilePath : str | None) -> None:
    if FilePath is None:
        return
    clip = VideoFileClip(FilePath)
    clip.audio.write_audiofile("OnlyAudioData//output_audio.mp3")
    clip.without_audio().write_videofile("OnlyVideoData//output_video.mp4")

''' remove this in Production! '''
# if __name__ == "__main__":
#     video_to_audio_and_video_conversion(f"demoData//sample.mp4")