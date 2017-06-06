import smtplib
import threading
import time
import Config
import MailboxAPI

def SendEmail(user, pwd, recipient, subject, body):

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        # SMTP_SSL Example
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(gmail_user, gmail_pwd)
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
        server_ssl.sendmail(FROM, TO, message)
        #server_ssl.quit()
        server_ssl.close()
        return True
    except:
        return False

class SendPasswordMailThread(threading.Thread):
    def __init__(self, recipient, pwd):
        threading.Thread.__init__(self)
        self.user = Config.GMAIL_ACCOUNT
        self.pwd = Config.GMAIL_PASSWORD
        self.recipient = recipient
        self.subject = 'Mailbox Password'
        self.body = 'Password:' + pwd

    def run(self):
        SendEmail(self.user, self.pwd, self.recipient, self.subject, self.body)

class ResendPasswordMailThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.end = False

    def run(self):
        while True:
            MailboxAPI.MailboxRepository.ResendPassword()
            time.sleep(10)
            self.lock.acquire()
            if self.end:
                self.lock.release()
                break
            self.lock.release()

    def stop(self):
        self.lock.acquire()
        self.end = True
        self.lock.release()
