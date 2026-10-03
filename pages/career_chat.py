import streamlit as st

from services.gemini import ask_gemini
from services.firebase import db, save_chat_message


# ---------------------------------------------------------
# LOAD CHAT HISTORY
# ---------------------------------------------------------

def load_chat_history(user_id):

    docs = (
        db.collection("users")
        .document(user_id)
        .collection("career_chats")
        .order_by("createdAt")
        .stream()
    )

    messages = []

    for doc in docs:

        data = doc.to_dict()

        messages.append({
            "role": data.get("role"),
            "content": data.get("message", "")
        })

    return messages


# ---------------------------------------------------------
# CAREER CHAT
# ---------------------------------------------------------

def show_career_chat(user):

    st.title("💬 CareerPilot AI")

    st.subheader("Your Personal Career Assistant")

    st.write(
        "Ask me anything about resumes, interviews, "
        "skills, jobs, career paths or placements."
    )

    user_id = user["uid"]

    # -----------------------------------------------------
    # LOAD CHAT HISTORY
    # -----------------------------------------------------

    if "career_chat_loaded" not in st.session_state:

        st.session_state.career_messages = load_chat_history(
            user_id
        )

        st.session_state.career_chat_loaded = True

    # -----------------------------------------------------
    # DISPLAY CHAT HISTORY
    # -----------------------------------------------------

    for message in st.session_state.career_messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

    # -----------------------------------------------------
    # USER MESSAGE
    # -----------------------------------------------------

    prompt = st.chat_input(
        "Ask your career question..."
    )

    if prompt:

        # Save user message locally
        st.session_state.career_messages.append({
            "role": "user",
            "content": prompt
        })

        # Save user message to Firestore
        save_chat_message(
            user_id,
            "user",
            prompt
        )

        with st.chat_message("user"):

            st.write(prompt)

        # -------------------------------------------------
        # GEMINI PROMPT
        # -------------------------------------------------

        user_name = user.get(
            "displayName",
            "CareerPilot User"
        )

        ai_prompt = f"""
You are CareerPilot AI, a helpful and practical
career coach.

User name:
{user_name}

Give clear, actionable and beginner-friendly advice.

Focus on:

- Career planning
- Resume improvement
- Interview preparation
- DSA and coding preparation
- Skills to learn
- Job preparation
- Internship preparation

User's question:

{prompt}
"""

        # -------------------------------------------------
        # GEMINI RESPONSE
        # -------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "CareerPilot is thinking... 🤖"
            ):

                try:

                    response = ask_gemini(
                        ai_prompt
                    )

                    st.write(response)

                    # Save assistant message locally
                    st.session_state.career_messages.append({
                        "role": "assistant",
                        "content": response
                    })

                    # Save assistant response to Firestore
                    save_chat_message(
                        user_id,
                        "assistant",
                        response
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {str(e)}"
                    )