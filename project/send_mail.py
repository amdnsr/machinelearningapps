import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename
import email
import email.mime.application
import email_body
from email.headerregistry import Address
import sys
import config
import os
# from helpers import createFolder
import datetime
import pytz
import details


def send_mail(name="John", mail_id=os.environ["EMAIL_ADDRESS"], token_link="https://www.google.com", msg_type="new_user"):
    msg = MIMEMultipart('alternative')

    if msg_type == "new_user":
        html = email_body.html_msg_new_user.format(
            name, token_link, token_link)
        msg['Subject'] = details.subject_new_user
    elif msg_type == "forgot":
        html = email_body.html_msg_forgot_pwd.format(
            name, token_link, token_link)
        msg['Subject'] = details.subject_forgot

    msg['From'] = config.EMAIL_ADDRESS
    msg['To'] = mail_id

    # The MIME types for text/html
    HTML_Contents = MIMEText(html, 'html')
    # Text_Contents = MIMEText(textmsg, 'text')
    # Adding pptx file attachment

    msg.attach(HTML_Contents)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(config.EMAIL_ADDRESS, config.PASSWORD)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(config.EMAIL_ADDRESS, mail_id, msg.as_string())

    # terminating the session
    s.quit()

# send_mail(token_link="https://www.google.com")
