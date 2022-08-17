from threading import Thread

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


class EmailThread(Thread):

    def __init__(self, email):
        self.email = email
        Thread.__init__(self)

    def run(self):
        self.email.send()


class Utils:
    token_generator = default_token_generator

    @staticmethod
    def send_email(data):
        """Отправка почты без threading"""

        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']])
        email.send()

    @staticmethod
    def send_email_thread(data):
        """Отправка почты с threading"""

        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']])
        EmailThread(email).start()
