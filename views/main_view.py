import streamlit as st
from embeddings.vector_store import generate_questions, generate_vector_store, get_conversational_chain, clear_cache, get_file_content
from database.session_manager import update_end_session
from functools import partial
from streamlit_url_fragment import get_fragment
import fitz
import time
import re

from utils.string_util import find_positions_multiple

file_citations = []

def clear_chat_history():
    st.session_state.answered_questions = []
    st.session_state.messages = [
        {"role": "assistant", "content": "Upload some PDFs and ask me a question"}]

async def user_input(user_question, thread_id, assistant_id, file_name, session_id):
    response = get_conversational_chain(user_question, thread_id, assistant_id, file_name, session_id)
    for chunk in response:
        yield chunk

def display_question(thread_id, assistant_id, file_name, session_id):
    questions = generate_questions(thread_id, assistant_id, file_name, session_id)
    return [q.strip() for q in questions.split('\n') if q.strip()]

def process_file():
    progress_bar = st.progress(0)
    for i in range(10):
        time.sleep(0.2)
        progress_bar.progress((i + 1) * 10)

def start_new_job():
    st.session_state.questions = []
    st.session_state.uploaded_files = []
    st.session_state.file_uploader_key += 1
    st.session_state.clicked_file_id = None
    st.session_state.citation_index = None
    st.session_state.initial_state = True
    clear_chat_history()
    clear_cache(st.session_state["user_id"])
    st.rerun()

def set_file_id(file_id, index):
    if st.session_state.clicked_file_id != file_id or st.session_state.citation_index != index:
        if st.session_state.clicked_file_id is not None:
            st.session_state.initial_state = False
        st.session_state.clicked_file_id = file_id
        st.session_state.citation_index = index
        st.rerun()

async def display_chat_room():
    global file_citations

    st.title("Chat with document files 🤖")
    st.write("Welcome to the chat!")
    st.write("Upload any file types or several types(pdf, docx, csv, pptx, xlsx, txt)")

    st.sidebar.button('Clear Chat History', on_click=clear_chat_history, use_container_width=True)
    st.sidebar.button('SignOut', on_click=logout)

    current_file_id = get_fragment()
    if current_file_id is not None:
        conf = current_file_id.split("#")
        if len(conf) > 2:
            set_file_id(conf[1], conf[2])
        else:
            set_file_id(None, None)
    # Chat input
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Upload some PDFs and ask me a question"}]
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            # st.code(message["content"], language="markdown", wrap_lines=True)
            st.markdown(f"""{message["content"]}""", unsafe_allow_html=True)

    button_pressed = ''
    if 'questions' in st.session_state and st.session_state.questions:
        for question in st.session_state.questions:
            if st.button(question, disabled=question in st.session_state.answered_questions):
                button_pressed = question[3:]
                if question not in st.session_state.answered_questions:
                    st.session_state.answered_questions.append(question)

    if prompt := ((st.chat_input()) or button_pressed):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.code(prompt, language="markdown", wrap_lines=True)
    
    st.markdown("""
                 <style>
                .file-citation {
                    display: none;
                }
                </style>
                """, unsafe_allow_html=True)

    if st.session_state.messages[-1]["role"] != "assistant" and 'thread_id' in st.session_state:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ""
                placeholder = st.empty()
                async for chunk in user_input(prompt, st.session_state.thread_id, st.session_state.assistant_id, st.session_state['file_name'], st.session_state.session_id):
                    if isinstance(chunk, str):
                        response = response + chunk
                    else:
                        positions = find_positions_multiple(response, "【", "】")

                        if len(positions) > 0:
                            placeholder.markdown("")

                            end_pos = 0
                            result = ""
                            for index, (start, end) in enumerate(positions):
                                result += response[end_pos:start]
                                end_pos = end

                                html_link = f"<a href='#{chunk[index].file_citation.file_id}#{chunk[index].start_index}' id='{chunk[index].file_citation.file_id}'>{response[start:end]}</a>"
                                result += html_link

                                pattern = r'<div class="file-citation">\s*(.*?)\s*</div>'
                                matches = re.findall(pattern, response[end:], re.DOTALL)  

                                if len(matches) > 0:
                                    file_citations.append({
                                        "index": chunk[index].start_index,
                                        "markdown": matches[0]
                                    })

                            result += response[end_pos:]
                            response = result

                    placeholder.markdown(response, unsafe_allow_html=True)

        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
        
    if len(st.session_state.answered_questions) is 3:
        st.session_state.btn_disabed = False
        st.text("Would you like to continue?")
        if st.button("Yes", disabled=st.session_state.btn_disabled):
            st.session_state.answered_questions = []
            st.session_state.questions = display_question(st.session_state['thread_id'], st.session_state['assistant_id'], st.session_state['file_name'], st.session_state.session_id)
            st.rerun()
        if st.button("No", disabled=st.session_state.btn_disabled):
            st.session_state.btn_disabled = True
            st.rerun()

async def main_content():
    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0
    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []
    if 'clicked_file_id' not in st.session_state:  
        st.session_state.clicked_file_id = None
    if 'citation_index' not in st.session_state:  
        st.session_state.citation_index = None
    if 'initial_state' not in st.session_state:  
        st.session_state.initial_state = False
    if 'answered_questions' not in st.session_state:
        st.session_state.answered_questions = []
    if 'btn_disabled' not in st.session_state:
        st.session_state.btn_disabled = False
    # Sidebar for uploading PDF files
    with st.sidebar:
        st.title("Menu:")
        if st.button("Start a New Job", use_container_width=True):
            start_new_job()
        uploaded_files = st.file_uploader(
            "Upload your Files and Click on the Submit & Process Button", accept_multiple_files=True, key=st.session_state["file_uploader_key"])
        if uploaded_files:
            st.session_state["uploaded_files"] = uploaded_files    
        if uploaded_files != []:
            if st.button("Submit & Process", use_container_width=True):
                with st.spinner("Processing..."):
                    start_time = time.time()
                    thread_id, assistant_id, file_name = generate_vector_store(uploaded_files, user_id=st.session_state.user_id)
                    st.session_state['thread_id'] = thread_id
                    st.session_state['assistant_id'] = assistant_id
                    st.session_state['file_name'] = file_name
                    st.session_state.questions = display_question(thread_id, assistant_id, st.session_state['file_name'], st.session_state.session_id)
                    process_file()
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    st.success(f"Done in {elapsed_time:.2f} seconds")

    if st.session_state.clicked_file_id and not st.session_state.initial_state:
        col1, col2 = st.columns(2)
        with col1:
            for citation in file_citations:
                if citation["index"] == int(st.session_state.citation_index):
                    st.markdown(citation["markdown"], unsafe_allow_html=True)
        with col2:
            await display_chat_room()
    else:
        await display_chat_room()

def logout():
    update_end_session(st.session_state["session_id"])
    clear_cache(st.session_state["user_id"])
    st.session_state.clear()
    st.session_state['logout'] = True
    st.session_state['name'] = None
    st.session_state['username'] = None
    st.session_state['connected'] = False