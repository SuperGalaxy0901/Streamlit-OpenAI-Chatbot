import os
from dotenv import load_dotenv

load_dotenv()

# LLM Model Information
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# MySQL Database information
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Mailersend Information
MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY")
EMAIL_TEMPLATE_SIGNUP = os.getenv("EMAIL_TEMPLATE_SIGNUP")

# URL Information
BACKEND_URL = os.getenv("BACKEND_URL")
PRODUCT_URL = os.getenv("PRODUCT_URL")

# reCAPTCHA Information
RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

# langfuse Information
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")