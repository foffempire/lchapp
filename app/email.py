import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


MAIL_USERNAME = 'mo6014245571@gmail.com'
MAIL_PASSWORD = 'lnuu meou kcvs nhyk'
MAIL_FROM = "mo6014245571@gmail.com"
MAIL_PORT = 587
MAIL_SERVER = 'smtp.gmail.com'
MAIL_FROM_NAME = "Labour Connect Hub"




async def send_mail(to: str, subject: str, body: str):
    message = MIMEMultipart("alternative")
    message["From"] = MAIL_USERNAME
    message["To"] = to
    message["Subject"] = subject

    part = MIMEText(body, "html")
    message.attach(part)
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_USERNAME, to, message.as_string())
    except Exception as e:
        return {"status": 500, "errors": e}