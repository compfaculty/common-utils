"""
Sends commands execution results to gmail
This is an attempt to make https://locationmagic.org/  before it was made ;-)
#TODO need to fix auth :-(
https://support.google.com/accounts/answer/6010255
https://support.google.com/accounts/answer/185833
"""
import argparse
import logging
import os
import re
import shlex
import smtplib
import subprocess
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from smtplib import SMTPHeloError, SMTPAuthenticationError, SMTPException

logging.basicConfig(format='%(asctime)-10s %(levelname)-5s:%(message)s', level=logging.DEBUG)
DEBUG = True

def _get_credentials(fn):
    # 1. trying to read from fn
    creds = Path(fn)
    user = ''
    passwd = ''
    if creds.exists() and creds.is_file():
        regex = re.compile(r"^\s*(?P<user>[\w+_@.!-]+)[\s:;,]+(?P<passwd>[\w_.@!]+)")
        found = regex.match(creds.read_text())
        if found:
            user, passwd = found.group('user'), found.group('passwd')
    else:  # check env
        import operator
        user, passwd = operator.itemgetter('USER_EMAIL', 'USER_PASS')(os.environ)
    if not (user and passwd):
        logging.error("Credentials are empty")
        sys.exit(1)
    return user, passwd


def create_mime_message(from_, to_, payload, subject_=None, preamble_='route log'):
    """Create the container (outer) email message."""
    try:
        info_ = " ".join(os.uname())
        subject_ = subject_ or "Route Info: {}".format(info_)
        msg = MIMEMultipart()
        msg['Subject'] = subject_
        msg['From'] = from_  # email address sending from
        msg['To'] = to_  # email address sending to
        msg.preamble = preamble_
        # attach user file to message
        loginfo = MIMEText(payload)
        msg.attach(loginfo)
    except Exception:
        if DEBUG:
            logging.error(sys.exc_info())
        else:
            pass
    else:
        return msg


def send_gmail(login, passwd, mime_message, smtp_server_port='smtp.gmail.com:587'):
    """sending mail  to gmail"""
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(login, passwd)
        server.sendmail(mime_message.get('From'), mime_message.get('To'), mime_message.as_string())

    except (SMTPHeloError, SMTPAuthenticationError, SMTPException,)  as e:
        if DEBUG:
            logging.error(f"Error code {e.smtp_code}, Error message {e.smtp_error}")
        return False
    else:
        if DEBUG:
            logging.info("Report is sent!")
        return True
    finally:
        server.quit()


def send_trace_to_owner(login: str, passwd: str, commands: list):
    with open("/tmp/payload", "w+") as fd:
        for cmd in commands:
            subprocess.run(shlex.split(cmd), stdout=fd)
        fd.seek(0)
        payload = fd.read()
        mime_msg = create_mime_message(
            from_=login,
            to_=login,
            payload= payload)
    res = False
    while not res:
        res = send_gmail(
            login=login,
            passwd=passwd,
            mime_message=mime_msg
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", type=str, help="user name")
    parser.add_argument("-p", "--passwd", type=str, help="user password")
    parser.add_argument("-f", "--file", type=str, help="name\pass file")
    parser.add_argument("-c", "--cmds", nargs='*', help="list of commands to run")
    args = parser.parse_args()
    if args.user and args.passwd:
        user, passwd = args.user, args.passwd
    else:
        user, passwd = _get_credentials(args.file)
    cmds = args.cmds
    if cmds:
        send_trace_to_owner(user, passwd, cmds)


if __name__ == "__main__":
    main()
