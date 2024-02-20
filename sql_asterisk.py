from getpass import getpass
from mysql.connector import connect, Error
import mysql.connector
from mysql.connector import Error
import time
import re



class MySQL():      
    def __init__(self, host, db, user, password):
        self.host = host
        self.db = db
        self.user = user
        self.password = password

    def connect(self):
        try:
            connect = mysql.connector.connect(host = self.host, user = self.user, password = self.password, database = self.db)
            print("Подключение к базе данных прошло успешно.")
            return connect
        except Error as e:          
            print(e)
    



    def get_call_by_mobile(self, mobile):
        connect = self.connect()
        # sql = f"SELECT * FROM cdr WHERE dst='{mobile}'"
        sql = f"SELECT * FROM cdr WHERE calldate >= NOW() - INTERVAL 2 MINUTE AND dst = '{mobile}'"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            # for row in result:
                # print(row)
            return result
        except Error as e:
            print(e)

            

    # ////
    def get_first_moment_call_by_mobile(self, mobile):
        connect = self.connect()
        sql = f"SELECT * FROM cdr WHERE calldate >= NOW() - INTERVAL 2 MINUTE AND dst = '{mobile}' ORDER BY calldate DESC LIMIT 1;"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            # for row in result:
                # print(row)
            return result
        except Error as e:
            print(e)



    def get_last_call_status_by_mobile(self, mobile):
        connect = self.connect()
        # sql = f"SELECT * FROM cdr WHERE dst = '{mobile}' ORDER BY calldate ASC LIMIT 1;"
        sql = f"SELECT * FROM cdr WHERE calldate >= NOW() - INTERVAL 2 MINUTE AND dst = '{mobile}' ORDER BY calldate ASC LIMIT 1;"
        
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            # for row in result:
                # print(row)
            return result
        except Error as e:
            print(e)



    def get_last_call_status_by_mobile_if_notanw(self, mobile):
        connect = self.connect()
        # sql = f"SELECT * FROM cdr WHERE dst = '{mobile}' ORDER BY calldate ASC LIMIT 1;"
        sql = f"select * from cdr where dst='{mobile}' and ROUND(time_to_sec((TIMEDIFF(NOW(), calldate))) / 60)< 10  and disposition='ANSWERED' and billsec>7;"
        
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            # for row in result:
                # print(row)
            return result
        except Error as e:
            print(e)

    

    
    


sql_init = MySQL("192.168.4.4", "", "", "") 
