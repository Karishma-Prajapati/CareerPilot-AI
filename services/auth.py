import streamlit as st


def set_user(user):
    st.session_state["logged_in"] = True
    st.session_state["user"] = user


def logout():
    st.session_state.clear()
    st.rerun()


def is_logged_in():
    return st.session_state.get("logged_in", False)


def get_current_user():
    return st.session_state.get("user")