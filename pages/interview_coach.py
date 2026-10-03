import streamlit as st
import tempfile
import os

from services.audio import extract_audio
from models.whisper_model import transcribe_audio
from utils.text_analysis import analyze_text
from utils.scoring import calculate_communication_score
from services.gemini import ask_gemini
from services.firebase import save_interview_result


def show_interview_coach(user):

    st.title("🎤 AI Interview Coach")

    st.subheader(
        "Practice interviews and get AI-powered feedback"
    )

    uploaded_video = st.file_uploader(
        "Upload your interview video",
        type=["mp4", "mov", "avi", "mkv"]
    )

    if uploaded_video:

        st.success(
            f"Uploaded: {uploaded_video.name}"
        )

        if st.button(
            "🚀 Analyze Interview",
            use_container_width=True
        ):

            try:

                # -------------------------
                # Save uploaded video
                # -------------------------

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=os.path.splitext(
                        uploaded_video.name
                    )[1]
                ) as temp_video:

                    temp_video.write(
                        uploaded_video.getbuffer()
                    )

                    video_path = temp_video.name

                # -------------------------
                # Audio path
                # -------------------------

                audio_path = video_path + ".wav"

                # -------------------------
                # Extract audio
                # -------------------------

                with st.spinner(
                    "Extracting audio... 🎧"
                ):

                    success = extract_audio(
                        video_path,
                        audio_path
                    )

                    if not success:
                        st.error(
                            "Could not extract audio."
                        )
                        return

                # -------------------------
                # Whisper transcription
                # -------------------------

                with st.spinner(
                    "Transcribing with Whisper... 🤖"
                ):

                    transcript, duration = transcribe_audio(
                        audio_path
                    )

                st.markdown("---")

                st.subheader("📝 Transcript")

                st.write(transcript)

                # -------------------------
                # Speaking duration
                # -------------------------

                minutes = int(duration // 60)
                seconds = int(duration % 60)

                st.info(
                    f"⏱️ Speaking Duration: "
                    f"{minutes} min {seconds} sec"
                )

                # -------------------------
                # Text analysis
                # -------------------------

                analysis = analyze_text(
                    transcript
                )

                total_words = analysis["total_words"]
                total_fillers = analysis["total_fillers"]
                repeated_words = analysis["repeated_words"]

                # -------------------------
                # Speaking speed
                # -------------------------

                if duration > 0:

                    speaking_speed = (
                        total_words / duration
                    ) * 60

                else:

                    speaking_speed = 0

                # -------------------------
                # Communication score
                # -------------------------

                score = calculate_communication_score(
                    speaking_speed,
                    total_fillers,
                    total_words,
                    repeated_words
                )

                st.markdown("---")

                st.subheader(
                    "📊 Communication Score"
                )

                st.metric(
                    "Interview Score",
                    f"{score}/100"
                )

                # -------------------------
                # Communication metrics
                # -------------------------

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Words",
                        total_words
                    )

                with col2:
                    st.metric(
                        "Filler Words",
                        total_fillers
                    )

                with col3:
                    st.metric(
                        "Speaking Speed",
                        f"{speaking_speed:.1f} WPM"
                    )

                # -------------------------
                # Gemini feedback
                # -------------------------

                prompt = f"""
You are an expert interview coach.

Analyze this interview transcript and
communication performance.

Give practical and honest feedback.

Include:

## Overall Feedback

## Communication Strengths

## Communication Problems

## Answer Quality

## Filler Words

## Confidence

## How to Improve

## Final Recommendation

Interview Transcript:

{transcript}

Speaking Speed:
{speaking_speed:.1f} words per minute

Total Filler Words:
{total_fillers}

Repeated Words:
{repeated_words}

Communication Score:
{score}/100
"""

                with st.spinner(
                    "Generating AI feedback... 🧠"
                ):
                    try:
                        feedback = ask_gemini(
                        prompt
                        )
                    except Exception as e:
                        feedback = (
                        "AI feedback is temporarily unavailable. "
                        "Please try again later."
                        )
                        st.warning(
                       "Gemini feedback could not be generated right now."
                        )

                st.markdown("---")

                st.subheader(
                    "🤖 CareerPilot AI Feedback"
                )

                st.markdown(feedback)

                # -------------------------
                # Save to Firestore
                # -------------------------

                save_interview_result(
                    user["uid"],
                    uploaded_video.name,
                    score,
                    transcript,
                    feedback
                )

                st.success(
                    "✅ Interview result saved to your profile!"
                )

            except Exception as e:

                st.error(
                    f"Interview analysis failed: {str(e)}"
                )

            finally:

                # Cleanup temporary files
                try:

                    if os.path.exists(video_path):
                        os.remove(video_path)

                    if os.path.exists(audio_path):
                        os.remove(audio_path)

                except Exception:
                    pass