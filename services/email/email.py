# app imports
from .utils.email_threads import EmailThread

__all__ = ["send_student_notification_email"]


def send_mail(subject, email_body, to):
    EmailThread(subject=subject, recipient=to, html_content=email_body).start()


def send_student_notification_email(student, teacher, student_class):
    """
    Sends Nnotification email to the new add student

    Arguments:
        student (Student): Student model object for which we send email
        teacher (str): Teacher Name whose added the student
        student_class (str): Class name which student was added to

    Return:
        bool: pass

    """

    email_body = (
        "Hi "
        + student.full_name
        + ", You have been add to the "
        + student_class
        + " class by the teacher"
        + teacher
    )

    send_mail(
        subject="School Nnotification", to=student.email, email_body=email_body
    )

    return True
