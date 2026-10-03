import streamlit as st
from html import escape


def render_sidebar(auth, user):

    # =====================================================
    # PAGE LIST
    # =====================================================

    pages = [
        "🏠 Dashboard",
        "💬 Career Chat",
        "📄 Resume Analyzer",
        "💼 Job Matcher",
        "🎤 Interview Coach",
        "📈 Career Progress",
    ]

    # =====================================================
    # HANDLE DASHBOARD NAVIGATION
    # =====================================================
    # Dashboard buttons store the requested page in
    # "careerpilot_navigation".
    #
    # We read it BEFORE creating the radio widget.
    # This avoids the Streamlit session-state error.
    # =====================================================

    if "careerpilot_navigation" in st.session_state:

        target_page = st.session_state.pop(
            "careerpilot_navigation"
        )

        if target_page in pages:

            st.session_state[
                "careerpilot_page_selector"
            ] = target_page

    # =====================================================
    # SIDEBAR
    # =====================================================

    with st.sidebar:

        # -------------------------------------------------
        # BRAND
        # -------------------------------------------------

        st.html(
            """
            <div class="cp-side-brand">

                <div class="cp-side-logo">
                    🚀
                </div>

                <div>
                    <div class="cp-side-title">
                        Career<span>Pilot</span>
                    </div>

                    <div class="cp-side-subtitle">
                        AI-powered career companion
                    </div>
                </div>

            </div>

            <div class="cp-side-divider"></div>

            <div class="cp-side-label">
                NAVIGATION
            </div>
            """
        )

        # -------------------------------------------------
        # NAVIGATION
        # -------------------------------------------------

        selected_page = st.radio(
            "Navigation",
            pages,
            key="careerpilot_page_selector",
            label_visibility="collapsed",
        )

        # Store current page separately.
        # DO NOT use "careerpilot_navigation" here.
        st.session_state["current_page"] = selected_page

        # -------------------------------------------------
        # SPACER
        # -------------------------------------------------

        st.html(
            """
            <div class="cp-side-spacer"></div>
            """
        )

        # -------------------------------------------------
        # USER INFORMATION
        # -------------------------------------------------

        name = user.get(
            "displayName",
            "CareerPilot User"
        )

        email = user.get(
            "email",
            ""
        )

        # Escape user information before putting it
        # inside HTML.
        safe_name = escape(str(name))
        safe_email = escape(str(email))

        # -------------------------------------------------
        # ACCOUNT
        # -------------------------------------------------

        st.html(
            f"""
            <div class="cp-side-account">
                ACCOUNT
            </div>

            <div class="cp-side-user">

                <div class="cp-side-avatar">
                    👤
                </div>

                <div class="cp-side-user-info">

                    <div class="cp-side-user-name">
                        {safe_name}
                    </div>

                    <div class="cp-side-user-email">
                        {safe_email}
                    </div>

                </div>

            </div>
            """
        )

        # -------------------------------------------------
        # DIVIDER
        # -------------------------------------------------

        st.markdown("---")

        # -------------------------------------------------
        # LOGOUT
        # -------------------------------------------------

        auth.logout_form()

    # =====================================================
    # RETURN SELECTED PAGE
    # =====================================================

    return selected_page