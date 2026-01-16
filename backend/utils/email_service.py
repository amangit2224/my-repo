from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

def send_test_email(to_email):
    message = Mail(
        from_email=os.getenv("SENDER_EMAIL"),
        to_emails=to_email,
        subject="Test Email from Medical Report Project",
        html_content="<p>If you got this, email works ✅</p>"
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print("Email sent:", response.status_code)
        return True
    except Exception as e:
        print("Email error:", e)
        return False
