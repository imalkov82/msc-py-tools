__author__ = 'imalkov'

# from PECUBE_RUN import *
# import os
# execdir = '{0}/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02'.format(os.environ['HOME'])
# for bpath in [os.path.join(execdir, el) for el in os.listdir(execdir)]:
#     print bpath
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket

def send_mail():
    hostname = socket.gethostname()
    mailing_list = ['igor.malkov82@gmail.com']

    msg = MIMEMultipart()
    msg['Subject'] = "Pecube Status"
    msg['From'] = 'generate-sample@' + hostname
    msg['To'] = ",".join(mailing_list)
    body = 'Success ' + "<br>"
    part = MIMEText(body,'html')
    msg.attach(part)
    smtp_host = 'localhost'

    try:
        s = smtplib.SMTP(smtp_host)
        s.sendmail('malkov@post.bgu.ac.il', mailing_list, msg.as_string())
    except Exception, e:
        raise e
    finally:
        s.quit()

def runcmd(cmd):
    import sys, os
    sys.stdout.flush()
    proc = os.popen(cmd)
    s = ""
    while True:
        line = proc.readline()
        if line != '':
            print line.strip()
            s += line
            sys.stdout.flush()
        else:
            break
    return s