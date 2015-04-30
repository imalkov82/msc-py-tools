__author__ = 'imalkov'

# from PECUBE_RUN import *
# import os
# execdir = '{0}/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02'.format(os.environ['HOME'])
# for bpath in [os.path.join(execdir, el) for el in os.listdir(execdir)]:
#     print bpath
import smtplib

def send_mail(body):
    sender = "malkov@bgu.ac.il"
    receivers = ["igor.malkov82@gmail.com"]
    yourname = "Igor Malkov"
    recvname = "Igor Malkov"
    sub = "Testing email"
    message = "From: " + yourname + "\n"
    message = message + "To: " + recvname + "\n"
    message = message + "Subject: " + sub + "\n"
    message = message + body
    try:
        print "Sending email to " + recvname + "...",
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        username = 'igor.malkov82@gmail.com'
        password = 'itgooRr2'
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(sender, receivers, message)
        server.quit()
        print "successfully sent!"
    except  Exception:
        print "Error: unable to send email"

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


# send_mail()
import logging
import os

fname = '{0}/Dropbox/M.s/Research/DATA/SESSION_TREE/log.dat'.format(os.environ['HOME'])
logging.basicConfig(filename=fname,level=logging.DEBUG)
logging.info('start logger')

logging.error()
# exec_dir = '{0}/Dropbox/M.s/Research/DATA/SESSION_TREE/NODE02'.format(os.environ['HOME'])
#
# for bpath in [os.path.join(exec_dir, d) for d in ['Session1D', 'Session1E', 'Session1F', 'Session2A', 'Session2B', 'Session2C']]:
#     print bpath