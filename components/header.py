import streamlit as st


def render_header(user):

    user_name = user.get("displayName", "CareerPilot User")
    user_email = user.get("email", "")

    first_name = user_name.split()[0] if user_name else "there"

    photo = user.get("photoURL", "")

    if photo:
        avatar = f'<img src="{photo}" class="cp-avatar">'
    else:
        avatar = '<div class="cp-avatar cp-avatar-placeholder">👤</div>'

    html = f"""
    <div class="cp-header">

        <div class="cp-brand">

            <div class="cp-logo">
                🚀
            </div>

            <div>
                <div class="cp-brand-name">
                    Career<span>Pilot</span>
                </div>

                <div class="cp-brand-tagline">
                    AI-powered career companion
                </div>
            </div>

        </div>


        <div class="cp-user">

            <div class="cp-user-info">

                <div class="cp-greeting">
                    Welcome back, {first_name} 👋
                </div>

                <div class="cp-email">
                    {user_email}
                </div>

            </div>

            {avatar}

        </div>

    </div>


    <style>

        .cp-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;

            width: 100%;

            padding: 12px 0 18px 0;
            margin-bottom: 25px;

            border-bottom:
                1px solid rgba(148, 163, 184, 0.12);
        }}


        .cp-brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}


        .cp-logo {{
            width: 46px;
            height: 46px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 14px;

            font-size: 22px;

            background:
                linear-gradient(
                    135deg,
                    #4f46e5,
                    #06b6d4
                );

            box-shadow:
                0 8px 25px rgba(79, 70, 229, 0.30);
        }}


        .cp-brand-name {{
            font-size: 21px;
            font-weight: 800;
            color: #f8fafc;
        }}


        .cp-brand-name span {{
            color: #818cf8;
        }}


        .cp-brand-tagline {{
            font-size: 11px;
            color: #64748b;
            margin-top: 2px;
        }}


        .cp-user {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}


        .cp-user-info {{
            text-align: right;
        }}


        .cp-greeting {{
            font-size: 14px;
            font-weight: 600;
            color: #e2e8f0;
        }}


        .cp-email {{
            font-size: 11px;
            color: #64748b;
            margin-top: 3px;
        }}


        .cp-avatar {{
            width: 44px;
            height: 44px;

            border-radius: 50%;

            object-fit: cover;

            border:
                2px solid rgba(129, 140, 248, 0.45);
        }}


        .cp-avatar-placeholder {{
            display: flex;
            align-items: center;
            justify-content: center;

            background:
                linear-gradient(
                    135deg,
                    #312e81,
                    #155e75
                );

            font-size: 18px;
        }}


        @media (max-width: 700px) {{

            .cp-email {{
                display: none;
            }}

            .cp-brand-tagline {{
                display: none;
            }}

            .cp-greeting {{
                font-size: 12px;
            }}

        }}

    </style>
    """

    st.html(html)