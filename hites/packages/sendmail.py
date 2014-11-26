from subprocess import Popen, PIPE
from email.mime.text import MIMEText


def sendmail(sender, recipients, subject, message):
    msg = MIMEText(message)
    msg["From"] = sender
    msg["To"] = ",".join(recipients)
    msg["Subject"] = subject
    p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
    p.communicate(msg.as_string())
