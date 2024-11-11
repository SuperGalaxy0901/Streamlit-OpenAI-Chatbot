# RAG System with OpenAI and Streamlit 🤖📄

Welcome to the **RAG System** (Retrieve and Generate) — an innovative AI-powered chatbot that leverages the OpenAI Assistant API and Streamlit to provide real-time, context-aware answers based on user-uploaded documents.

## Features ✨

- **Multiformat Document Support**: Upload and process various file types including PDFs, DOCX, PPTX, TXT, and script files. 📂
- **Real-time Responses**: Enjoy seamless and interactive responses fetched via WebSocket connections. 🔄
- **Context Aware**: Provides answers based on the content of the uploaded documents, making the interactions more meaningful and personalized. 🔍

## Installation ⚙️

To get started with the RAG system, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SuperGalaxy0901/Streamlit-OpenAI-Chatbot.git
   cd rag-system
   ```

2. **Set up a Virtual Environment** (recommended):
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install the Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file to safely store your API keys and configuration settings.
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage 🚀

1. **Run the Streamlit App**:
   ```bash
   streamlit run app.py
   ```

2. **Interact with the Chatbot**:
   - Upload documents via the application interface. 📤
   - Engage with the chatbot as it generates insightful responses based on your document contents. 💬

## Architecture Overview 🏗️

- **Streamlit**: Provides the front-end interface where users can upload documents and interact with the chatbot. 🌐
- **OpenAI Assistant API**: Powers the natural language comprehension and generation. 🧠
- **WebSockets**: Enables real-time, efficient communication between the front-end and back-end services. 📡

## Acknowledgements 🙏

- [OpenAI](https://openai.com) for their incredible API.
- [Streamlit](https://streamlit.io) for the easy-to-use app framework.
