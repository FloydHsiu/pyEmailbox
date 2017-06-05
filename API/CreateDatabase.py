import sqlite3

def InitializeDatabase():
    conn = sqlite3.connect('Emailbox.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS CLIENTS
                    (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        FLOOR INTEGER NOT NULL,
                        FIRST_NAME NVARCHAR(60) NOT NULL,
                        LAST_NAME NVARCHAR(60) NOT NULL,
                        EMAIL_ADDRESS VARCHAR(200) NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS MAILBOXES
                    (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        INUSED BOOLEAN NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS MAILBOX_BINDING
                    (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        PWD VARCHAR(200) NOT NULL,
                        MAILBOX_IDS VARCHAR(100) NOT NULL,
                        CLIENT_ID INTEGER NOT NULL, --FOREIGN KEY CLIENT(ID)
                        LAST_REMIND_TIME DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FINISH BOOLEAN NOT NULL --CHECK IF THIS PACKAGE IS BEEN TAKE OFF
                    )''')

    conn.commit()
    conn.close()

def AddSystemData():
    conn = sqlite3.connect('Emailbox.db')
    cursor = conn.cursor()

    #Mailbox Data
    cursor.execute("INSERT INTO MAILBOXES VALUES(NULL, 0)")
    cursor.execute("INSERT INTO MAILBOXES VALUES(NULL, 0)")

    #Add Your Own Data
    cursor.execute("INSERT INTO CLIENTS VALUES(NULL, '4F','Test', 'Test', 'test@test.com')")

    conn.commit()
    conn.close()