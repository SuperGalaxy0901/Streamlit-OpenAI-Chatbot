from mailersend import emails
from config import settings

api_key = settings.MAILERSEND_API_KEY
signup_template = settings.EMAIL_TEMPLATE_SIGNUP
backend_url = settings.BACKEND_URL

mailer = emails.NewEmail(api_key)

def signup_mailer(customer_email, verify_token):
    signup_link = f"{backend_url}/verify-email?token={verify_token}"
    print(signup_link)
    print(api_key)
    print(signup_template)
    print(backend_url)
    mail_body = {"signup_link": signup_link}
    mail_from = {
        "name": "GTRAG",
        "email": "info@gtrag.com",
    }
    recipients = [
        {
            "email": customer_email,
        }
    ]
    personalization = [
        {
            "email": customer_email,
            "data": {
                "verify_id": signup_link
            }
        }
    ]
    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject("Please verify your email", mail_body)
    mailer.set_template(signup_template, mail_body)
    mailer.set_personalization(personalization, mail_body)
    response = mailer.send(mail_body)
    print(response)
