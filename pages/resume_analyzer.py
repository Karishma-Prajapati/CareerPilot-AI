import re
import streamlit as st
from pypdf import PdfReader

from services.gemini import ask_gemini
from services.firebase import save_resume_analysis


# =========================================================
# EXTRACT TEXT FROM PDF
# =========================================================

def extract_text(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# =========================================================
# EXTRACT RESUME SCORE
# =========================================================

def extract_resume_score(result):

    if not result:
        return 0

    # Convert response to string
    result = str(result)

    # -----------------------------------------------------
    # Pattern 1
    # Example:
    # Resume Score: 82/100
    # -----------------------------------------------------

    patterns = [

        r"Resume\s+Score\s*[:\-]?\s*\**\s*(\d{1,3})\s*(?:/\s*100|%)?",

        r"##\s*Resume\s+Score\s*\n+\s*\**\s*(\d{1,3})\s*(?:/\s*100|%)?",

        r"\*\*Resume\s+Score\*\*\s*[:\-]?\s*\**\s*(\d{1,3})\s*(?:/\s*100|%)?",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            result,
            re.IGNORECASE
        )

        if match:

            score = int(match.group(1))

            # Make sure score is valid
            if 0 <= score <= 100:
                return score

    # -----------------------------------------------------
    # Fallback:
    # Look for something like 82/100
    # -----------------------------------------------------

    fallback = re.search(
        r"\b(\d{1,3})\s*/\s*100\b",
        result
    )

    if fallback:

        score = int(fallback.group(1))

        if 0 <= score <= 100:
            return score

    return 0


# =========================================================
# RESUME ANALYZER
# =========================================================

def show_resume_analyzer(user):

    st.title("📄 Resume Analyzer")

    st.subheader(
        "Get AI-powered feedback on your resume"
    )

    # -----------------------------------------------------
    # UPLOAD RESUME
    # -----------------------------------------------------

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        # -------------------------------------------------
        # ANALYZE BUTTON
        # -------------------------------------------------

        if st.button(
            "🔍 Analyze Resume",
            use_container_width=True
        ):

            with st.spinner(
                "Reading and analyzing your resume... 🤖"
            ):

                try:

                    # =====================================
                    # EXTRACT PDF TEXT
                    # =====================================

                    resume_text = extract_text(
                        uploaded_file
                    )

                    if not resume_text.strip():

                        st.error(
                            "Could not extract text from this PDF."
                        )

                        return

                    # =====================================
                    # GEMINI PROMPT
                    # =====================================

                    prompt = f"""
You are CareerPilot AI, an expert career and
resume coach.

Analyze the following resume.

IMPORTANT:
Start your response with exactly this format:

## Resume Score
82/100

Replace 82 with the actual score.

Then follow this structure:

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

                    # =====================================
                    # CALL GEMINI
                    # =====================================

                    result = ask_gemini(prompt)

                    if not result:

                        st.error(
                            "AI analysis returned no result."
                        )

                        return

                    # =====================================
                    # EXTRACT SCORE
                    # =====================================

                    resume_score = extract_resume_score(
                        result
                    )

                    # =====================================
                    # DEBUG / SCORE
                    # =====================================

                    st.write(
                        "Detected Resume Score:",
                        resume_score
                    )

                    if resume_score == 0:

                        st.warning(
                            "⚠️ Could not detect the resume score "
                            "from the AI response."
                        )

                    # =====================================
                    # SAVE TO FIRESTORE
                    # =====================================

                    save_resume_analysis(
                        user["uid"],
                        uploaded_file.name,
                        result,
                        resume_score
                    )

                    # =====================================
                    # DISPLAY ANALYSIS
                    # =====================================

                    st.markdown("---")

                    st.subheader(
                        "🤖 CareerPilot Analysis"
                    )

                    st.markdown(result)

                    # =====================================
                    # SUCCESS
                    # =====================================

                    st.success(
                        "✅ Resume analysis saved to your "
                        "CareerPilot profile!"
                    )

                except Exception as e:

                    st.error(
                        f"Analysis failed: {str(e)}"
                    )