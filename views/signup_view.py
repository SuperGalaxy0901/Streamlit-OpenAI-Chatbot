import streamlit as st
from database.user_manager import create_user, verify_user, create_google_user
from helpers.validators import is_valid_email, is_valid_password
from views.capcha_plugin import captcha_control
from views.login_view import init_login_session
from utils.google_authenticate import authenticator

def signup_page():
    st.title("🔐 Sign Up")
    
    new_email = st.text_input("Email")
    new_password = st.text_input("New Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')

    # SignUp By Google
    authenticator.check_authentification()
    authorization_url = authenticator.get_authorization_url()

    if not st.session_state.get('connected', False):
        st.link_button('Sign Up With Google', authorization_url, use_container_width=True)
    else:
        email = st.session_state['user_info'].get('email')
        create_google_user(email)
        init_login_session(email)
        st.rerun()
    
    # Captcha Component
    captcha_control()

    if 'server_code' not in st.session_state:
        st.session_state.server_code = ""

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button("Sign Up", use_container_width=True):
            if not is_valid_email(new_email):
                st.error("🚫 Invalid email format")
            elif not is_valid_password(new_password):
                st.error("🚫 Password must be at least 8 characters long, contain a letter, a number, and a special character")
            elif new_password != confirm_password:
                st.error("🚫 Passwords do not match")
            else:
                ret = create_user(new_email, new_password)
                if ret != "error":
                    st.success("✅ User created successfully. Please check your email for the verification link.")
                else:
                    st.error("🚫 Error creating user. Please try again.")

        if st.button("Go to Sign In", use_container_width=True):
            st.session_state['page'] = "login"
            st.rerun()

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
