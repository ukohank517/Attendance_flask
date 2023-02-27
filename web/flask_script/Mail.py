import os
from os.path import join, dirname
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib


class Mail:

    def create_message(self, from_addr, to_addr, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Date'] = formatdate()
        return msg


    def send_mail(self, HOST, USER, PASS, from_addr, to_addr, body_msg):
        smtpobj = smtplib.SMTP(HOST, 587)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        smtpobj.login(USER, PASS)
        smtpobj.sendmail(from_addr, to_addr, body_msg)
        smtpobj.close()