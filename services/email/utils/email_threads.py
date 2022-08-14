import threading

from django.core.mail import EmailMessage


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient):
        self.subject = subject
        self.recipient_list = recipient
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(
            self.subject,
            body=self.html_content,
            to=[self.recipient_list],
            from_email="te734793@gmail.com",
        )
        msg.content_subtype = "html"
        msg.send()
