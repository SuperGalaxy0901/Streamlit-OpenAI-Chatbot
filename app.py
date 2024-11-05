import streamlit as st
st.set_page_config(layout="wide")

import asyncio
from views import main_view, login_view, signup_view
from database.user_manager import create_users_table
from database.chat_manager import create_chat_table
from database.cost_manager import create_cost_table
from database.session_manager import create_session_table

# st.set_page_config(
#     page_title="Chatbot",
#     page_icon="🤖"
# )
async def main():
    """Main function to execute the Streamlit app."""
    if 'connected' not in st.session_state:
        st.session_state['connected'] = False

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state['page'] = 'login'

    if "user_id" in st.session_state and st.session_state["user_id"]:
        st.session_state["logged_in"] = True

    if 'user_info' not in st.session_state:
        st.session_state['user_info'] = {}

    if st.session_state['logged_in']:
        await main_view.main_content()
    else:
        if st.session_state['page'] == 'login':
            login_view.login_page()
        else:
            signup_view.signup_page()

if __name__ == "__main__":
    # Call the function to create the table
    create_users_table()
    create_chat_table()
    create_cost_table()
    create_session_table()
    # Run the main function
    asyncio.run(main())