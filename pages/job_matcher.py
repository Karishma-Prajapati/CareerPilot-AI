import streamlit as st
from pypdf import PdfReader
import re

from services.gemini import ask_gemini
from services.firebase import db
from datetime import datetime


def extract_resume_text(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def save_job_match(user_id, job_title, result, score):

    match_ref = (
        db.collection("users")
        .document(user_id)
        .collection("job_matches")
        .document()
    )

    match_ref.set({
        "job_title": job_title,
        "analysis": result,
        "score": score,
        "createdAt": datetime.utcnow()
    })

    return match_ref.id


def show_job_matcher(user):

    st.title("💼 AI Job Matcher")

    st.subheader(
        "Find out how well your resume matches a job"
    )

    st.write(
        "Upload your resume and paste a Job Description. "
        "CareerPilot will identify your strengths, skill gaps "
        "and why you may not be getting shortlisted."
    )

    st.markdown("---")

    # Resume
    uploaded_file = st.file_uploader(
        "📄 Upload your Resume",
        type=["pdf"]
    )

    # Job title
    job_title = st.text_input(
        "💼 Job Title",
        placeholder="e.g. Software Engineer Intern"
    )

    # Job description
    job_description = st.text_area(
        "📋 Paste Job Description",
        height=250,
        placeholder="Paste the complete job description here..."
    )

    if st.button(
        "🚀 Analyze Job Match",
        use_container_width=True
    ):

        if not uploaded_file:
            st.warning("Please upload your resume.")

            return

        if not job_description.strip():
            st.warning("Please enter the job description.")

            return

        with st.spinner(
            "Comparing your resume with the job... 🤖"
        ):

            try:

                resume_text = extract_resume_text(
                    uploaded_file
                )

                prompt = f"""
You are CareerPilot AI, an expert recruitment
and career coach.

Compare the candidate's resume with the job
description.

Give a practical and honest analysis.

Use exactly this structure:

## 🎯 Job Match Score
Give a percentage score from 0 to 100.

## ✅ Matching Skills
List the skills and experience from the resume
that match the job.

## ❌ Missing Skills
List important skills required by the job that
are missing from the resume.

## ⚠️ Resume Gaps
Explain weaknesses in the resume that could
reduce the chance of shortlisting.

## 🔍 Why You May Not Be Getting Shortlisted
Give the most likely reasons based ONLY on the
resume and job description.

## 💡 Improvement Plan
Give 5 specific actions to improve the chances
of getting shortlisted.

## 🚀 Skills to Learn
Suggest the most important technical or
professional skills to learn.

### RESUME

{resume_text}

### JOB TITLE

{job_title}

### JOB DESCRIPTION

{job_description}
"""

                result = ask_gemini(prompt)
                score_match = re.search(
                    r"Job Match Score[\s:\-*#]*([0-9]{1,3})",
                    result,re.IGNORECASE)
                job_match_score = int(score_match.group(1)) if score_match else 0

                st.write("Detected Job Match Score:", job_match_score)

                # Save result
                match_id= save_job_match(
                    user["uid"],
                    job_title or "Unknown Job",
                    result,
                    job_match_score,

                )
                st.success(f"✅ Job match saved! Document ID: {match_id}")

                st.markdown("---")

                st.subheader(
                    "🤖 CareerPilot Job Analysis"
                )

                st.markdown(result)

                st.success(
                    "✅ Job match saved to your profile!"
                )

            except Exception as e:

                st.error(
                    f"Job analysis failed: {str(e)}"
                )