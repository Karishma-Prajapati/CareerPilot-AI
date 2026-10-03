import streamlit as st

from services.firebase import db


# =========================================================
# FIRESTORE HELPERS
# =========================================================

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


def get_latest_job_score(user_id):

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
        return data.get("score", 0)

    return 0


# =========================================================
# DASHBOARD
# =========================================================

def show_dashboard(user):

    user_id = user["uid"]

    user_name = user.get(
        "displayName",
        "CareerPilot User"
    )

    first_name = (
        user_name.split()[0]
        if user_name
        else "there"
    )

    # -----------------------------------------------------
    # LOAD SCORES
    # -----------------------------------------------------

    try:

        resume_score = get_latest_resume_score(user_id)

        interview_score = get_latest_interview_score(
            user_id
        )

        job_score = get_latest_job_score(
            user_id
        )

    except Exception:

        resume_score = 0
        interview_score = 0
        job_score = 0


    # -----------------------------------------------------
    # CAREER READINESS
    # -----------------------------------------------------

    scores = [
        score
        for score in [
            resume_score,
            interview_score,
            job_score
        ]
        if score > 0
    ]

    career_readiness = (
        round(sum(scores) / len(scores))
        if scores
        else 0
    )


    # =====================================================
    # HERO
    # =====================================================

    st.html(
        f"""
        <div class="cp-hero">

            <div class="cp-hero-title">
                Good evening, {first_name} 👋
            </div>

            <div class="cp-hero-subtitle">
                Your career journey starts here.
                Build a stronger resume, prepare for interviews,
                discover relevant opportunities and grow with
                your personal AI career coach.
            </div>

            <div class="cp-hero-tags">

                <span class="cp-tag cp-tag-purple">
                    🤖 AI Powered
                </span>

                <span class="cp-tag cp-tag-blue">
                    🎯 Personalized
                </span>

                <span class="cp-tag cp-tag-green">
                    📈 Track Progress
                </span>

            </div>

        </div>
        """
    )


    # =====================================================
    # SECTION TITLE
    # =====================================================

    st.html(
        """
        <div class="cp-section-header">

            <h2>
                Your Career Readiness
            </h2>

            <p>
                A quick snapshot of your current preparation.
            </p>

        </div>
        """
    )


    # =====================================================
    # SCORE CARDS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "📄 Resume",
            f"{resume_score}/100"
            if resume_score
            else "—"
        )


    with col2:

        st.metric(
            "🎤 Interview",
            f"{interview_score}/100"
            if interview_score
            else "—"
        )


    with col3:

        st.metric(
            "💼 Job Match",
            f"{job_score}/100"
            if job_score
            else "—"
        )


    with col4:

        st.metric(
            "🚀 Readiness",
            f"{career_readiness}%"
            if career_readiness
            else "—"
        )


    # =====================================================
    # CAREER PROGRESS
    # =====================================================

    if career_readiness:

        st.html(
            f"""
            <div class="cp-card">

                <div class="cp-progress-header">

                    <div>

                        <div class="cp-progress-title">
                            Career Readiness
                        </div>

                        <div class="cp-progress-subtitle">
                            Keep improving your weakest areas.
                        </div>

                    </div>

                    <div class="cp-progress-score">
                        {career_readiness}%
                    </div>

                </div>

            </div>
            """
        )

        st.progress(
            career_readiness / 100
        )

    else:

        st.info(
            "🚀 Complete your first Resume, Interview or "
            "Job assessment to start tracking your "
            "Career Readiness."
        )


    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    st.html(
        """
        <div class="cp-section-header">

            <h2>
                Continue Your Journey
            </h2>

            <p>
                Choose a tool and take the next step.
            </p>

        </div>
        """
    )


    col1, col2, col3 = st.columns(3)


    # -----------------------------------------------------
    # RESUME
    # -----------------------------------------------------

    with col1:

        st.html(
            """
            <div class="cp-feature">

                <div class="cp-feature-icon">
                    📄
                </div>

                <div class="cp-feature-title">
                    Improve Your Resume
                </div>

                <div class="cp-feature-text">
                    Get AI-powered feedback on your
                    resume, ATS compatibility and
                    missing skills.
                </div>

            </div>
            """
        )

        if st.button(
            "Analyze Resume →",
            use_container_width=True,
            key="dashboard_resume"
        ):

            st.session_state[
                "careerpilot_navigation"
            ] = "📄  Resume Analyzer"

            st.rerun()


    # -----------------------------------------------------
    # INTERVIEW
    # -----------------------------------------------------

    with col2:

        st.html(
            """
            <div class="cp-feature">

                <div class="cp-feature-icon">
                    🎤
                </div>

                <div class="cp-feature-title">
                    Practice Interviews
                </div>

                <div class="cp-feature-text">
                    Analyze your communication,
                    speaking speed and interview
                    performance with AI.
                </div>

            </div>
            """
        )

        if st.button(
            "Practice Interview →",
            use_container_width=True,
            key="dashboard_interview"
        ):

            st.session_state[
                "careerpilot_navigation"
            ] = "🎤  Interview Coach"

            st.rerun()


    # -----------------------------------------------------
    # JOB MATCHER
    # -----------------------------------------------------

    with col3:

        st.html(
            """
            <div class="cp-feature">

                <div class="cp-feature-icon">
                    💼
                </div>

                <div class="cp-feature-title">
                    Find Your Match
                </div>

                <div class="cp-feature-text">
                    Compare your profile with a job
                    description and discover your
                    skill gaps.
                </div>

            </div>
            """
        )

        if st.button(
            "Match a Job →",
            use_container_width=True,
            key="dashboard_job"
        ):

            st.session_state[
                "careerpilot_navigation"
            ] = "💼  Job Matcher"

            st.rerun()


    # =====================================================
    # AI INSIGHT
    # =====================================================

    st.html(
        """
        <div class="cp-insight">

            <div class="cp-insight-label">
                ✨ AI CAREER INSIGHT
            </div>

            <div class="cp-insight-title">
                Small improvements create big career progress.
            </div>

            <div class="cp-insight-text">
                Use CareerPilot regularly to identify your
                weak areas, practice consistently and turn
                feedback into measurable improvement.
            </div>

        </div>
        """
    )


    # =====================================================
    # CAREER TOOLKIT
    # =====================================================

    st.html(
        """
        <div class="cp-section-header">

            <h2>
                Your Career Toolkit
            </h2>

            <p>
                Everything you need in one place.
            </p>

        </div>
        """
    )


    col1, col2, col3, col4 = st.columns(4)


    tools = [

        (
            "📄",
            "Resume Analyzer",
            "Optimize your resume"
        ),

        (
            "💼",
            "Job Matcher",
            "Find skill gaps"
        ),

        (
            "🎤",
            "Interview Coach",
            "Practice confidently"
        ),

        (
            "🤖",
            "Career Chat",
            "Ask your AI coach"
        )
    ]


    for col, tool in zip(
        [col1, col2, col3, col4],
        tools
    ):

        icon, title, description = tool

        with col:

            st.html(
                f"""
                <div class="cp-feature cp-tool-card">

                    <div class="cp-feature-icon">
                        {icon}
                    </div>

                    <div class="cp-feature-title">
                        {title}
                    </div>

                    <div class="cp-feature-text">
                        {description}
                    </div>

                </div>
                """
            )