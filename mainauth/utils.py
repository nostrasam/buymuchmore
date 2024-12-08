from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
import os

def send_email(subject, to_email, template_name, context, logo_path, image1_path, image2_path):
    html_content = render_to_string(template_name, context)
    text_context = strip_tags(html_content)

    # create the email
    email = EmailMultiAlternatives(subject, text_context, 'mail@hube.com.ng', [to_email])
    email.attach_alternative(html_content, 'text/html')
    
    # Attach logo image
    with open(logo_path, 'rb') as img:
        mime_image = MIMEImage(img.read())
        mime_image.add_header('Content-ID', '<logo>')
        email.attach(mime_image)

    # Attach first image
    with open(image1_path, 'rb') as img:
        mime_image = MIMEImage(img.read())
        mime_image.add_header('Content-ID', '<image1>')
        email.attach(mime_image)

    # Attach second image
    with open(image2_path, 'rb') as img:
        mime_image = MIMEImage(img.read())
        mime_image.add_header('Content-ID', '<image2>')
        email.attach(mime_image)

    email.send()

    