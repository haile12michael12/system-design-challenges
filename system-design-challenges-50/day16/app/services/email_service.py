import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..core.config import settings

class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.email_user = settings.EMAIL_USER
        self.email_password = settings.EMAIL_PASSWORD

    def send_password_reset_email(self, to_email: str, reset_token: str) -> None:
        """Send password reset email."""
        subject = "Password Reset Request"
        body = f"""
        You have requested to reset your password.
        Please use the following token to reset your password: {reset_token}
        
        If you did not request this, please ignore this email.
        """
        
        self._send_email(to_email, subject, body)

    def send_verification_email(self, to_email: str, verification_token: str) -> None:
        """Send email verification email."""
        subject = "Email Verification"
        body = f"""
        Please verify your email address using the following token: {verification_token}
        """
        
        self._send_email(to_email, subject, body)

    def _send_email(self, to_email: str, subject: str, body: str) -> None:
        """Send an email."""
        # In a real implementation, we would send the email
        # For now, we'll just print to console
        print(f"Sending email to {to_email}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        
        # Uncomment the following code to actually send emails
        # msg = MIMEMultipart()
        # msg['From'] = self.email_user
        # msg['To'] = to_email
        # msg['Subject'] = subject
        # 
        # msg.attach(MIMEText(body, 'plain'))
        # 
        # server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        # server.starttls()
        # server.login(self.email_user, self.email_password)
        # text = msg.as_string()
        # server.sendmail(self.email_user, to_email, text)
        # server.quit()