from threading import Thread
from typing import Any
from django.core.mail import send_mail
from django.conf import settings
from devteamtask.projects.models import Project


class SendEmailByThread(Thread):

    def __init__(self, thread_name: str, instance: Project | Any, email: str, link):
        Thread.__init__(self)
        self.thread_name = thread_name
        self._instance = instance

        # Falta atribuir o atributo email no recipient_list in send_email func
        self.email = email
        self.link = link
        self.has_errors = False

    def get_errors(self):
        return self.has_errors

    def save_invite_and_send_email(self):
        print("Email sending - Thread " + self.thread_name)

        send_mail(
            subject="Title",
            message="Link" + str(self.link),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["talismar788.una@gmail.com"]
        )

    def run(self):
        self.save_invite_and_send_email()
