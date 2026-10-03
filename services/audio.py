import ffmpeg

def extract_audio(video_path,audio_path):
    try:
        (
            ffmpeg.input(video_path)
            .output(audio_path,
                    acodec="pcm_s16le",
                    ac=1,
                    ar="16000"
            )
            .overwrite_output()
            .run(quiet=True)
        )
        return True

    except ffmpeg.Error as e:
        print("FFmpeg error:")
        print(e.stderr.decode()if e.stdrr else "Unknown error")
        return False