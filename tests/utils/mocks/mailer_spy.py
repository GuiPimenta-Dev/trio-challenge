from src.application.ports.gateways.mailer import Mailer


class MailerSpy(Mailer):
    def __init__(self):
        self.emails = []

    def send(self, to: str, subject: str, body: str) -> None:
        self.emails.append({"to": to, "subject": subject, "body": body})
