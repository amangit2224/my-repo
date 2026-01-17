from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def send_reset_email(to_email, reset_link):
    message = Mail(
        from_email=os.getenv("SENDER_EMAIL"),
        to_emails=to_email,
        subject="Reset Your Password",
        html_content=f"""
        <h3>Password Reset</h3>
        <p>You requested to reset your password.</p>
        <p>Click the link below to proceed:</p>
        <p>
            <a href="{reset_link}" target="_blank">
                Reset Password
            </a>
        </p>
        <p>This link is valid for 1 hour.</p>
        <p>If you did not request this, ignore this email.</p>
        """
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)
        print("Reset email sent successfully")
        return True
    except Exception as e:
        print("SendGrid error:", e)
        return False
