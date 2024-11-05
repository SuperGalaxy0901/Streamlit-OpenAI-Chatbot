from streamlit_google_auth import Authenticate

authenticator = Authenticate(
    secret_credentials_path='./client_secret.json',
    cookie_name='rag-system-biscoito',
    cookie_key='senha_maluca_12345',
    redirect_uri='https://gtrag.bot/',
)