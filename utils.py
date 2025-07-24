import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD

def send_phishing_email(to_email, subject, html_content):
    try:
        # Set up the SMTP connection
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Upgrade connection to secure
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        # Build email
        msg = MIMEMultipart('alternative')
        msg['From'] = SMTP_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(html_content, 'html'))

        # Send email
        server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        server.quit()

        print(f"[+] Email sent to {to_email}")

    except Exception as e:
        print(f"[!] Failed to send email to {to_email}: {e}")
