import os
import firebase_admin

from firebase_admin import credentials, firestore
from datetime import datetime


# ---------------------------------------------------------
# INITIALIZE FIREBASE
# ---------------------------------------------------------

if not firebase_admin._apps:

    service_account_file = "firebase-service-account.json"

    # Local development
    if os.path.exists(service_account_file):

        cred = credentials.Certificate(service_account_file)

        firebase_admin.initialize_app(cred)

    # Cloud Run / Google Cloud
    else:

        firebase_admin.initialize_app()


# Firestore database
db = firestore.client()


# ---------------------------------------------------------
# SAVE USER
# ---------------------------------------------------------

def save_user(user):

    uid = user["uid"]

    user_ref = (
        db.collection("users")
        .document(uid)
    )

    user_data = {
        "uid": uid,
        "name": user.get(
            "displayName",
            "CareerPilot User"
        ),
        "email": user.get(
            "email",
            ""
        ),
        "photo": user.get(
            "photoURL",
            ""
        ),
        "lastLogin": datetime.utcnow()
    }

    if not user_ref.get().exists:

        user_data["createdAt"] = datetime.utcnow()

    user_ref.set(
        user_data,
        merge=True
    )

    return True


# ---------------------------------------------------------
# SAVE RESUME ANALYSIS
# ---------------------------------------------------------

def save_resume_analysis(
    user_id,
    file_name,
    analysis,
    score
):

    resume_ref = (
        db.collection("users")
        .document(user_id)
        .collection("resume_analysis")
        .document()
    )

    resume_ref.set({

        "file_name": file_name,

        "analysis": analysis,

        "score": score,

        "createdAt": datetime.utcnow()
    })

    return resume_ref.id


# ---------------------------------------------------------
# SAVE JOB MATCH
# ---------------------------------------------------------

def save_job_match(
    user_id,
    job_title,
    result,
    score
):

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


# ---------------------------------------------------------
# SAVE INTERVIEW RESULT
# ---------------------------------------------------------

def save_interview_result(
    user_id,
    video_name,
    score,
    transcript,
    feedback
):

    interview_ref = (
        db.collection("users")
        .document(user_id)
        .collection("interviews")
        .document()
    )

    interview_ref.set({

        "video_name": video_name,

        "score": score,

        "transcript": transcript,

        "feedback": feedback,

        "createdAt": datetime.utcnow()
    })

    return interview_ref.id


def save_chat_message(user_id, role, message):

    chat_ref = (
        db.collection("users")
        .document(user_id)
        .collection("career_chats")
        .document()
    )

    chat_ref.set({
        "role": role,
        "message": message,
        "createdAt": datetime.utcnow()
    })

    return chat_ref.id