import streamlit as st
from services.firebase import db


# ---------------------------------------------------------
# GET LATEST RESUME SCORE
# ---------------------------------------------------------

def get_latest_resume_score(user_id):

    docs = (
        db.collection("users")
        .document(user_id)
        .collection("resume_analysis")
        .order_by("createdAt", direction="DESCENDING")
        .limit(1)
        .stream()
    )

    for doc in docs:
        data = doc.to_dict()
        return data.get("score", 0)

    return 0


# ---------------------------------------------------------
# GET LATEST INTERVIEW SCORE
# ---------------------------------------------------------

def get_latest_interview_score(user_id):

    docs = (
        db.collection("users")
        .document(user_id)
        .collection("interviews")
        .order_by("createdAt", direction="DESCENDING")
        .limit(1)
        .stream()
    )

    for doc in docs:
        data = doc.to_dict()
        return data.get("score", 0)

    return 0


# ---------------------------------------------------------
# GET LATEST JOB MATCH SCORE
# ---------------------------------------------------------

def get_latest_job_match_score(user_id):

    docs = (
        db.collection("users")
        .document(user_id)
        .collection("job_matches")
        .order_by("createdAt", direction="DESCENDING")
        .limit(1)
        .stream()
    )

    for doc in docs:
        data = doc.to_dict()

        # Read the score directly from Firestore
        return data.get("score", 0)

    return 0


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

def show_dashboard(user):

    st.title("🚀 CareerPilot AI")

    st.subheader(
        f"Welcome back, {user.get('displayName', 'CareerPilot User')}! 👋"
    )

    st.write("Your AI-powered personal career coach.")

    st.markdown("---")

    # -----------------------------------------------------
    # USER ID
    # -----------------------------------------------------

    user_id = user["uid"]

    # -----------------------------------------------------
    # GET ALL SCORES
    # -----------------------------------------------------

    resume_score = get_latest_resume_score(user_id)

    interview_score = get_latest_interview_score(user_id)

    job_match_score = get_latest_job_match_score(user_id)

    # -----------------------------------------------------
    # CAREER OVERVIEW
    # -----------------------------------------------------

    st.subheader("📊 Career Overview")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📄 Resume Score",
            f"{resume_score}/100" if resume_score else "—",
            help="Your latest resume analysis score"
        )

    with col2:

        st.metric(
            "🎤 Interview Score",
            f"{interview_score}/100" if interview_score else "—",
            help="Your latest interview score"
        )

    with col3:

        st.metric(
            "💼 Job Match",
            f"{job_match_score}/100" if job_match_score else "—",
            help="Your latest job match score"
        )

    # -----------------------------------------------------
    # CAREER PROGRESS
    # -----------------------------------------------------

    st.markdown("---")

    st.subheader("🎯 Career Progress")

    completed = sum([
        resume_score > 0,
        interview_score > 0,
        job_match_score > 0
    ])

    if completed == 3:

        career_progress = round(
            (
                resume_score
                + interview_score
                + job_match_score
            ) / 3
        )

        st.progress(career_progress / 100)

        st.metric(
            "Overall Career Progress",
            f"{career_progress}%"
        )

        st.caption(
            "Based on your latest Resume, Interview and Job Match scores."
        )

    else:

        st.progress(completed / 3)

        st.write(
            f"📈 Assessments completed: **{completed}/3**"
        )

        st.info(
            "Complete all three assessments to calculate your "
            "overall Career Progress."
        )

    # -----------------------------------------------------
    # QUICK ACTIONS
    # -----------------------------------------------------

    st.markdown("---")

    st.subheader("⚡ Quick Actions")

    col1, col2 = st.columns(2)

    with col1:

        st.write("### 📄 Resume")

        st.write(
            "Analyze your resume and get AI-powered suggestions "
            "to improve your profile."
        )

    with col2:

        st.write("### 💼 Job Matching")

        st.write(
            "Compare your resume with a job description and "
            "identify missing skills."
        )

    col1, col2 = st.columns(2)

    with col1:

        st.write("### 🎤 Interview Coach")

        st.write(
            "Practice your interview and get feedback on "
            "communication and speaking performance."
        )

    with col2:

        st.write("### 💬 Career Chat")

        st.write(
            "Ask CareerPilot AI about careers, DSA, interviews, "
            "skills and internships."
        )

    # -----------------------------------------------------
    # RECENT ACTIVITY
    # -----------------------------------------------------

    st.markdown("---")

    st.subheader("🕒 Recent Activity")

    activity_found = False

    # -----------------------------------------------------
    # LATEST INTERVIEW
    # -----------------------------------------------------

    interview_docs = (
        db.collection("users")
        .document(user_id)
        .collection("interviews")
        .order_by("createdAt", direction="DESCENDING")
        .limit(1)
        .stream()
    )

    for doc in interview_docs:

        data = doc.to_dict()

        activity_found = True

        st.write(
            f"🎤 **Interview analyzed:** "
            f"{data.get('video_name', 'Interview')}"
        )

        st.caption(
            f"Score: {data.get('score', 0)}/100"
        )

    # -----------------------------------------------------
    # LATEST RESUME
    # -----------------------------------------------------

    resume_docs = (
        db.collection("users")
        .document(user_id)
        .collection("resume_analysis")
        .order_by("createdAt", direction="DESCENDING")
        .limit(1)
        .stream()
    )

    for doc in resume_docs:

        data = doc.to_dict()

        activity_found = True

        st.write(
            f"📄 **Resume analyzed:** "
            f"{data.get('file_name', 'Resume')}"
        )

        st.caption(
            f"Score: {data.get('score', 0)}/100"
        )

    # -----------------------------------------------------
    # LATEST JOB MATCH
    # -----------------------------------------------------

    job_docs = (
        db.collection("users")
        .document(user_id)
        .collection("job_matches")
        .order_by("createdAt", direction="DESCENDING")
        .limit(1)
        .stream()
    )

    for doc in job_docs:

        data = doc.to_dict()

        activity_found = True

        st.write(
            f"💼 **Job matched:** "
            f"{data.get('job_title', 'Job')}"
        )

        st.caption(
            f"Score: {data.get('score', 0)}/100"
        )

    # -----------------------------------------------------
    # NO ACTIVITY
    # -----------------------------------------------------

    if not activity_found:

        st.info(
            "No activity yet. Start by analyzing your resume!"
        )