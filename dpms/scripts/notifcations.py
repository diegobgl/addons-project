# -*- coding:utf-8 -*-
import xmlrpclib
import json
import re
from ast import literal_eval
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

db = 'MyCompany'
url = 'http://127.0.0.1:8079'
username = 'admin'
password = 'mypassword'


def send_email(recipient, name, project_title):
    sender_email = "pmt@mycompany.dz"
    receiver_email = recipient
    password = ''  # input("Type your password and press enter:")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Project Update Notification"
    message["From"] = 'dpms@mycompany.dz'
    message["To"] = recipient

    # Create the plain-text and HTML version of your message
    text = """\
         Dear {name}, 

         Please update your project {project} status (Current Status, Planned Actions, Risks and Issues)
         Thanks."""

    html = """\
    <html>
      <body>
        <p>Dear {name},<br>
        </p>
        <p>
           Please update your project {project} status. (Current Status, Planned Actions, Risks and Issues).
        </p>
        <p>
        Merci.
        </p>
      </body>
    </html>
    """

    text = text.replace('{name}', name)
    text = text.replace('{project}', project_title)

    html = html.replace('{name}', name)
    html = html.replace('{project}', project_title)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    # server = smtplib.SMTP_SSL("smtp.gmail.com", port=465)
    server = smtplib.SMTP("mail.mycompany.dz", port=25)
    # server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())


common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

projects = models.execute_kw(db, uid, password, 'dpms.project', 'search_read',
                             [[['status', '!=', 'suspended'], ['status', '!=', 'closed']]])

for project in projects:
    print project['title']
    title = project['title']
    emp = models.execute_kw(db, uid, password, 'dpms.employee', 'search_read',
                            [[['id', '=', str(project['projectmanager_id'][0])]]])
    user = models.execute_kw(db, uid, password, 'res.users', 'search_read', [[['id', '=', str(emp[0]['user_id'][0])]]])
    name = user[0]['name']
    email_address = user[0]['email']
    # send_email(email_address,name, title)
    print 'sending :' + name + ' - ' + email_address