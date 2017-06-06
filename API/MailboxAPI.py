import sqlite3
import json
import random
import string
import hashlib
import binascii
import MailSender
import Config

class Mailbox:
    def __init__(self, id, inused):
        self.id = id
        self.inused = inused

class MailboxRepository:

    def __init__(self):
        pass

    @staticmethod
    def GetAll():
        conn = sqlite3.connect('Emailbox.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM MAILBOXES")
        mailboxList = list()
        for data in cursor.fetchall():
            mailboxList.append(Mailbox(data[0], data[1]))
        conn.close()
        return mailboxList

    @staticmethod
    def Assign(want):
        emptyCount = 0
        mailboxList = MailboxRepository.GetAll()
        for mailbox in mailboxList:
            if mailbox.inused == 0:
                emptyCount = emptyCount + 1
        if want > emptyCount:
            return False
        else:
            if want == 1:
                for mailbox in mailboxList:
                    if mailbox.inused == 0:
                        return [mailbox]
            else:
                return mailboxList

    @staticmethod
    def PwdHashing(pwd):
        dk = hashlib.pbkdf2_hmac(Config.HASHING_ALGORITHM, pwd, Config.HASHING_SALT, Config.HASHING_TIMES)
        hashPwd = binascii.hexlify(dk)
        return hashPwd

    @staticmethod
    def ConfirmAssign(mailboxList, client):
        conn = sqlite3.connect('Emailbox.db')
        cursor = conn.cursor()
        idList = list()
        #set mailbox inused
        for mailbox in mailboxList:
            idList.append(mailbox.id)
            cursor.execute("UPDATE MAILBOXES SET INUSED=1 WHERE ID=?", (mailbox.id,))
        #random password
        pwd = ''.join(random.choice(string.digits) for _ in range(8))
        #get pwd hash
        hashPwd = MailboxRepository.PwdHashing(pwd)
        insertData = (hashPwd, json.dumps(idList), client.id, )
        #bind the mailbox inused, and client id, password
        cursor.execute("INSERT INTO MAILBOX_BINDING VALUES(NULL,?,?,?,CURRENT_TIMESTAMP,0)", insertData)
        sendEmailThread = MailSender.SendPasswordMailThread(client.email_address, pwd)
        sendEmailThread.start()
        conn.commit()
        conn.close()

    @staticmethod
    def ResendPassword():
        conn = sqlite3.connect('Emailbox.db')
        cursor = conn.cursor()
        #get all unfinish mailbox_binding
        cursor.execute('''SELECT CLIENT_ID, (strftime('%s','now') - strftime('%s', LAST_REMIND_TIME))
                        FROM MAILBOX_BINDING 
                        WHERE FINISH=0
                        ''')
        orders = cursor.fetchall()
        if orders is not None:
            for order in orders:
                client_id = order[0]
                last_remind = order[1]
                if last_remind > 3600*20:
                    #change password
                    pwd = ''.join(random.choice(string.digits) for _ in range(8))
                    pwdHashing = MailboxRepository.PwdHashing(pwd)
                    cursor.execute("UPDATE MAILBOX_BINDING SET PWD=?, LAST_REMIND_TIME=CURRENT_TIMESTAMP", (pwdHashing,))
                    #send password to client
                    cursor.execute("SELECT EMAIL_ADDRESS FROM CLIENTS WHERE ID=?", (client_id,))
                    client_email_address = cursor.fetchone()
                    sendMailThread = MailSender.SendPasswordMailThread(client_email_address[0], pwd)
                    sendMailThread.start()
                    sendMailThread.join()

        conn.commit()
        conn.close()

    @staticmethod
    def GetPackage(password):
        conn = sqlite3.connect('Emailbox.db')
        cursor = conn.cursor()
        hashPwd = MailboxRepository.PwdHashing(password)
        cursor.execute("SELECT * FROM MAILBOX_BINDING WHERE PWD=? AND FINISH=0", (hashPwd,))
        order = cursor.fetchone()
        returnValue = None
        if order is not None:
            #get box id for open
            cursor.execute("UPDATE MAILBOX_BINDING SET FINISH=1 WHERE ID=?", (order[0],))
            idList = json.loads(order[2])
            for id in idList:
                cursor.execute("UPDATE MAILBOXES SET INUSED=0 WHERE ID=?", (id,))
            returnValue = idList
        else:
            returnValue = False
        conn.commit()
        conn.close()
        return returnValue
