import streamlit as st
import re
from pypdf import PdfReader
from services.gemini import ask_gemini
from services.firebase import save_resume_analysis

def extract_text(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def show_resume_analyzer(user):

    st.title("📄 Resume Analyzer")
    st.subheader("Get AI-powered feedback on your resume")

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(f"Uploaded: {uploaded_file.name}")

        if st.button(
            "🔍 Analyze Resume",
            use_container_width=True
        ):

            with st.spinner(
                "Reading and analyzing your resume... 🤖"
            ):

                try:

                    resume_text = extract_text(uploaded_file)

                    if not resume_text.strip():
                        st.error(
                            "Could not extract text from this PDF."
                        )
                        return

                    prompt = f"""
You are CareerPilot AI, an expert career and
resume coach.

Analyze the following resume.

Give the response in this exact structure:

## Resume Score
Give a score out of 100.

## Strengths
List the strongest parts of the resume.

## Weaknesses
List the areas that need improvement.

## Missing Skills
Suggest important skills that appear to be missing.

## ATS Suggestions
Give suggestions to improve ATS compatibility.

## Action Plan
Give 5 specific actions the candidate should take.

Resume:

{resume_text}
"""

                    result = ask_gemini(prompt)
                    score_match = re.search(
                          r"Resume Score\s*[:\-]?\s*(\d+)\s*(?:/100|%)?", result,re.IGNORECASE)
                    resume_score = int(score_match.group(1)) if score_match else 0
                    st.write("Detected Resume Score:", resume_score)
                    save_resume_analysis(user["uid"], uploaded_file.name, result,resume_score)

                    st.markdown("---")
                    st.subheader("🤖 CareerPilot Analysis")

                    st.markdown(result)

                    st.success( "✅ Resume analysis saved to your CareerPilot profile!")
                    

                except Exception as e:

                    st.error(
                        f"Analysis failed: {str(e)}"
                    )