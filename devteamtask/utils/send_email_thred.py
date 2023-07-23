from threading import Thread
from config.settings.base import env
from django.core.mail import send_mail
from django.conf import settings
from devteamtask.projects.models import Project


class SendEmailByThread(Thread):
    def __init__(self, thread_name: str, instance: Project, email: str, token):
        Thread.__init__(self)
        self.thread_name = thread_name
        self.project = instance

        self.email = email
        self.token = token
        self.has_errors = False

    def get_errors(self):
        return self.has_errors

    def save_invite_and_send_email(self):
        print("Email sending - Thread " + self.thread_name)

        subject = f"Joining the {self.project.name} project"
        token = f"<a href='{env('BACK_URL')}/api/invite/{self.token}/'>Joinig now!</a>"
        message = "Link to joining: " + token

        send_mail(
            subject=subject,
            message="",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.email],
            html_message=message,
        )

    def run(self):
        self.save_invite_and_send_email()
