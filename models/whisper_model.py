import whisper

# Better accuracy than "base"
model = whisper.load_model("small")


def transcribe_audio(audio_path):

    result = model.transcribe(
        audio_path,
        fp16=False,
        language="en",
        temperature=0,
        condition_on_previous_text=False,
        initial_prompt=(
            "This is a job interview introduction. "
            "The speaker may use terms such as "
            "NIET, Greater Noida, B.Tech CSE, "
            "Data Science, Java, Python, Power BI, "
            "machine learning, artificial intelligence, "
            "and GenAI."
        )
    )

    transcript = result["text"].strip()

    segments = result["segments"]

    if segments:
        duration = segments[-1]["end"]
    else:
        duration = 0

    return transcript, duration