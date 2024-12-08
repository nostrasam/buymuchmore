from celery import shared_task
from .utils import send_email

@shared_task
def user_register_send_email_task(to_email,verification_url):
    subject = 'INNOVATION STARTS NOW'
    logo_path = 'static/images/logo.png'
    image1_path = 'static/images/emailimage-1.jpeg'
    image2_path = 'static/images/emailimage-2.png'

    context = {
        'subject': subject,
        'verification_url':verification_url
    }
    send_email(subject,to_email,'starter-email.html',context, logo_path, image1_path, image2_path)



@shared_task
def user_reset_password_send_email_task(to_email,verification_url):
    subject = 'INNOVATION STARTS NOW'
    logo_path = 'static/images/logo.png'
    image1_path = 'static/images/emailimage-1.jpeg'
    image2_path = 'static/images/emailimage-2.png'

    context = {
        'subject': subject,
        'verification_url':verification_url
    }
    send_email(subject,to_email,'starter-email.html',context, logo_path, image1_path, image2_path)