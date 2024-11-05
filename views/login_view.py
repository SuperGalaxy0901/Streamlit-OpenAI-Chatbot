import streamlit as st
from database.user_manager import authenticate_user, get_user_id, update_user_country, create_google_user
from database.session_manager import insert_start_session
from views.capcha_plugin import captcha_control
from utils.ip_tools import get_remote_country
from embeddings.vector_store import clear_cache
from streamlit_google_auth import Authenticate
from utils.google_authenticate import authenticator


def init_login_session(email):
    user_id = get_user_id(email)
    session_id = insert_start_session(user_id)
    st.session_state["logged_in"] = True
    st.session_state["email"] = email
    st.session_state["user_id"] = user_id
    st.session_state["session_id"] = session_id
    clear_cache(user_id)

def login_page():
    st.title("Sign In")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    authenticator.check_authentification()
    authorization_url = authenticator.get_authorization_url()

    print(st.session_state["connected"])
    # SignIn By Google
    if st.session_state["connected"] == False:
        st.link_button('Sign In With Google', authorization_url, use_container_width=True)
    elif st.session_state["connected"] == True:
        email = st.session_state['user_info'].get('email')
        create_google_user(email)
        init_login_session(email)
        st.rerun()

    # Captcha Component
    captcha_control()

    # Signin By Email and Password
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button("Sign In", use_container_width=True):
            res = authenticate_user(email, password)
            if res == "Success":
                update_user_country(email, get_remote_country())
                init_login_session(email)
                st.rerun()
            else:
                # st.error(res)
                print(res)
  
        if st.button("Go to Sign Up", use_container_width=True):
            st.session_state['page'] = 'signup'
            st.rerun()

