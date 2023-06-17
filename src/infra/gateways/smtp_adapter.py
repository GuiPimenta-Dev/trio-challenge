import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.application.ports.gateways.mailer import Mailer


class SmtpAdapter(Mailer):
    def __init__(self, smtp_username: str, smtp_password: str):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    def send(self, to: str, subject: str, body: str) -> None:
        message_obj = MIMEMultipart()
        message_obj["From"] = self.smtp_username
        message_obj["To"] = to
        message_obj["Subject"] = subject

        message_obj.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(message_obj)
