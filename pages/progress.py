import streamlit as st
from services.firebase import db
import re


# ---------------------------------------------------------
# GET LATEST RESUME SCORE
# ---------------------------------------------------------
def get_latest_resume(user_id):
    docs = (
        db.collection("users")
        .document(user_id)
        .collection("resume_analysis")
        .order_by("createdAt", direction="DESCENDING")
        .limit(1)
        .stream()
    )

    for doc in docs:
        return doc.to_dict()

    return None


# ---------------------------------------------------------
# GET LATEST INTERVIEW
# ---------------------------------------------------------
def get_latest_interview(user_id):
    docs = (
        db.collection("users")
        .document(user_id)
        .collection("interviews")
        .order_by("createdAt", direction="DESCENDING")
        .limit(1)
        .stream()
    )

    for doc in docs:
        return doc.to_dict()

    return None


# ---------------------------------------------------------
# GET LATEST JOB MATCH
# ---------------------------------------------------------
def get_latest_job_match(user_id):
    docs = (
        db.collection("users")
        .document(user_id)
        .collection("job_matches")
        .order_by("createdAt", direction="DESCENDING")
        .limit(1)
        .stream()
    )

    for doc in docs:
        return doc.to_dict()

    return None


# ---------------------------------------------------------
# PROGRESS PAGE
# ---------------------------------------------------------
def show_progress(user):

    st.title("📈 Career Progress")

    st.subheader(
        f"Track your growth, {user.get('displayName', 'CareerPilot User')}! 🚀"
    )

    st.write(
        "Monitor your resume, interview and job-matching performance "
        "in one place."
    )

    user_id = user["uid"]

    # -----------------------------------------------------
    # FETCH DATA
    # -----------------------------------------------------

    resume = get_latest_resume(user_id)
    interview = get_latest_interview(user_id)
    job_match = get_latest_job_match(user_id)

    resume_score = resume.get("score", 0) if resume else 0
    interview_score = interview.get("score", 0) if interview else 0
    job_score = job_match.get("score", 0) if job_match else 0

    # -----------------------------------------------------
    # SCORE OVERVIEW
    # -----------------------------------------------------

    st.markdown("---")
    st.subheader("📊 Performance Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📄 Resume",
            f"{resume_score}/100" if resume_score else "—"
        )

    with col2:
        st.metric(
            "🎤 Interview",
            f"{interview_score}/100" if interview_score else "—"
        )

    with col3:
        st.metric(
            "💼 Job Match",
            f"{job_score}/100" if job_score else "—"
        )

    # -----------------------------------------------------
    # INDIVIDUAL PROGRESS
    # -----------------------------------------------------

    st.markdown("---")
    st.subheader("📈 Skill & Career Indicators")

    if resume_score:
        st.write(f"📄 **Resume Score — {resume_score}/100**")
        st.progress(resume_score / 100)
    else:
        st.info("Analyze your resume to see your Resume Score.")

    if interview_score:
        st.write(f"🎤 **Interview Score — {interview_score}/100**")
        st.progress(interview_score / 100)
    else:
        st.info("Analyze an interview to see your Interview Score.")

    if job_score:
        st.write(f"💼 **Job Match Score — {job_score}/100**")
        st.progress(job_score / 100)
    else:
        st.info("Analyze a job to see your Job Match Score.")

    # -----------------------------------------------------
    # OVERALL PROGRESS
    # -----------------------------------------------------

    st.markdown("---")
    st.subheader("🎯 Overall Career Progress")

    scores = [
        score
        for score in [
            resume_score,
            interview_score,
            job_score
        ]
        if score > 0
    ]

    if scores:

        overall = round(sum(scores) / len(scores))

        st.progress(overall / 100)

        st.metric(
            "Career Progress",
            f"{overall}%"
        )

        if overall >= 80:
            st.success(
                "Your current assessment scores show strong progress. "
                "Keep improving consistently."
            )

        elif overall >= 60:
            st.warning(
                "You have a good foundation. Focus on improving "
                "your weaker areas."
            )

        else:
            st.info(
                "Keep practicing and use CareerPilot's feedback "
                "to improve your scores."
            )

    else:

        st.info(
            "Complete at least one assessment to start tracking "
            "your career progress."
        )

    # -----------------------------------------------------
    # RECENT ACTIVITY
    # -----------------------------------------------------

    st.markdown("---")
    st.subheader("🕒 Recent Activity")

    activity_found = False

    if interview:

        activity_found = True

        st.write(
            f"🎤 **Interview analyzed:** "
            f"{interview.get('video_name', 'Interview')}"
        )

        st.caption(
            f"Interview Score: {interview.get('score', 0)}/100"
        )

    if resume:

        activity_found = True

        st.write(
            f"📄 **Resume analyzed:** "
            f"{resume.get('file_name', 'Resume')}"
        )

        st.caption(
            f"Resume Score: {resume.get('score', 0)}/100"
        )

    if job_match:

        activity_found = True

        st.write(
            f"💼 **Job analyzed:** "
            f"{job_match.get('job_title', 'Job')}"
        )

        st.caption(
            f"Job Match Score: {job_score}/100"
        )

    if not activity_found:

        st.info(
            "No activity yet. Start with Resume Analyzer, "
            "Job Matcher or Interview Coach."
        )