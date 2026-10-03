import os
import streamlit as st
from pathlib import Path

from dotenv import load_dotenv
from streamlit_firebase_auth import FirebaseAuth

from services.firebase import save_user

from pages.dashboard import show_dashboard
from pages.career_chat import show_career_chat
from pages.resume_analyzer import show_resume_analyzer
from pages.job_matcher import show_job_matcher
from pages.interview_coach import show_interview_coach
from pages.progress import show_progress

from components.header import render_header
from components.sidebar import render_sidebar


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# LOAD GLOBAL CSS
# =========================================================

def load_css():

    css_path = Path("styles/theme.css")

    if css_path.exists():

        with open(
            css_path,
            "r",
            encoding="utf-8"
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


load_css()


# =========================================================
# FIREBASE CONFIG
# =========================================================

firebase_config = {

    "apiKey": os.getenv(
        "FIREBASE_API_KEY"
    ),

    "authDomain": os.getenv(
        "FIREBASE_AUTH_DOMAIN"
    ),

    "projectId": os.getenv(
        "FIREBASE_PROJECT_ID"
    ),

    "storageBucket": os.getenv(
        "FIREBASE_STORAGE_BUCKET"
    ),

    "messagingSenderId": os.getenv(
        "FIREBASE_MESSAGING_SENDER_ID"
    ),

    "appId": os.getenv(
        "FIREBASE_APP_ID"
    ),
}


# =========================================================
# FIREBASE AUTH
# =========================================================

auth = FirebaseAuth(firebase_config)

user = auth.check_session()


# =========================================================
# LOGIN PAGE
# =========================================================

if not user:

    st.title("🚀 CareerPilot AI")

    st.subheader(
        "Your Personal AI Career Coach"
    )

    st.write(
        "Prepare for your dream career with AI-powered "
        "resume analysis, job matching, mock interviews "
        "and personalized career guidance."
    )

    st.markdown("---")

    st.info(
        "🔐 Sign in to continue"
    )

    result = auth.login_form()

    if result and result.get("success"):

        st.rerun()

    if result and not result.get("success"):

        st.error(
            result.get(
                "message",
                "Login failed"
            )
        )


# =========================================================
# AUTHENTICATED APPLICATION
# =========================================================

else:

    # -----------------------------------------------------
    # SAVE USER
    # -----------------------------------------------------

    save_user(user)


    # -----------------------------------------------------
    # TOP HEADER
    # -----------------------------------------------------

    render_header(user)


    # -----------------------------------------------------
    # SIDEBAR
    # -----------------------------------------------------

    selected_page = render_sidebar(
        auth,
        user
    )


    # =====================================================
    # PAGE ROUTING
    # =====================================================

    if selected_page == "🏠 Dashboard":

        show_dashboard(user)


    elif selected_page == "💬 Career Chat":

        show_career_chat(user)


    elif selected_page == "📄 Resume Analyzer":

        show_resume_analyzer(user)


    elif selected_page == "💼 Job Matcher":

        show_job_matcher(user)


    elif selected_page == "🎤 Interview Coach":

        show_interview_coach(user)


    elif selected_page == "📈 Career Progress":

        show_progress(user)