from subprocess import Popen, PIPE
from email.mime.text import MIMEText


def sendmail(recipients, subject, message, sender=None):
    msg = MIMEText(message)
    if sender:
        msg["From"] = sender
    msg["To"] = ",".join(recipients)
    msg["Subject"] = subject
    p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
    p.communicate(msg.as_string())
