import sqlite3
class Client:
    def __init__(self, id, floor, first_name, last_name, email_address):
        self.id = id
        self.floor = floor
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
    
    def __repr__(self):
        return '(' + str(self.id) + '. ' + self.first_name + ', ' + self.last_name + ')'

class ClientRepository:
    @staticmethod
    def GetAll():
        conn = sqlite3.connect('Emailbox.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM CLIENTS')
        clientList = list()
        for data in cursor.fetchall():
            clientList.append(Client(data[0], data[1], data[2], data[3], data[4]))
        conn.close()
        return clientList
