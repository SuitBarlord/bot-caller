from getpass import getpass
from mysql.connector import connect, Error
import mysql.connector
from mysql.connector import Error
import time
import re

connected = False

class MySQL():      
    def __init__(self, host, db, user, password):
        self.host = host
        self.db = db
        self.user = user
        self.password = password

    def connect(self):
        while not connected:
            try:
                connect = mysql.connector.connect(host = self.host, user = self.user, password = self.password, database = self.db)
                print("Подключение к базе данных прошло успешно.")
                return connect
            except Error as e:          
                print(e)
                time.sleep(5)
    



    def get_by_id_orders(self, guid):
        connect = self.connect()
        sql = f"SELECT * FROM status_statement WHERE guid='{guid}'"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            # for row in result:
                # print(row)
            return result
        except Error as e:
            print(e)


    def get_by_appeal_id_orders(self, appeal_id):
        connect = self.connect()
        sql = f"SELECT * FROM status_statement WHERE appeal_id='{appeal_id}'"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            # for row in result:
                # print(row)
            return result
        except Error as e:
            print(e)




    def get_by_tel_orders(self, appeal_id, person_mobile):
        connect = self.connect()
        sql = f"SELECT * FROM status_statement WHERE appeal_id='{appeal_id}' AND person_mobile='{person_mobile}'"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            # for row in result:
                # print(row)
            return result
        except Error as e:
            print(e)


    
    def set_new_order(self, guid, appeal_id, order_number, short_order_number, person_fio, person_mobile, subservice, date_creation, executor_order, user_creater_order, user_last_modification_order, several_in_day, repeated_day, united):
        connect = self.connect()
        sql = f"INSERT INTO status_statement(guid, appeal_id, order_number, short_order_number, person_fio, person_mobile, subservice, date_creation, first_call_moment, call_status, count_calls, last_call_moment, call_status_now, executor_order, user_creater_order, user_last_modification_order, several_in_day, repeated_day, united) VALUES ('{guid}', '{appeal_id}', '{order_number}', '{short_order_number}', '{person_fio}', '{person_mobile}', '{subservice}', '{date_creation}', NULL, NULL, 0, NULL, 0, '{executor_order}', '{user_creater_order}', '{user_last_modification_order}', '{several_in_day}', '{repeated_day}', '{united}')"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            connect.commit()
            connect.close()
        except Error as e:
            print(e)



    
    def update_first_call_by_id(self, guid, date):
        connect = self.connect()
        sql = f"UPDATE status_statement SET first_call_moment = '{date}', count_calls = 1 WHERE guid = '{guid}';"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            connect.commit()
            connect.close()
        except Error as e:
            print(e)




    def update_call_status_by_id(self, guid, status):
        connect = self.connect()
        sql = f"UPDATE status_statement SET call_status = '{status}' WHERE guid = '{guid}';"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            connect.commit()
            connect.close()
        except Error as e:
            print(e)
    



    def get_last_call_by_id(self, appeal_id):
        connect = self.connect()
        sql = f"SELECT last_call_moment FROM status_statement WHERE appeal_id='{appeal_id}';"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            connect.commit()
            connect.close()
        except Error as e:
            print(e)
    


    def update_last_call_by_id(self, guid, last_call_moment):
        connect = self.connect()
        sql = f"UPDATE status_statement SET last_call_moment = '{last_call_moment}', count_calls = count_calls + 1 WHERE guid = '{guid}';"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            connect.commit()
            connect.close()
        except Error as e:
            print(e)



    def update_notified_call_by_id(self, guid, notified):
        connect = self.connect()
        sql = f"UPDATE status_statement SET notified = '{notified}' WHERE guid = '{guid}';"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            connect.commit()
            connect.close()
        except Error as e:
            print(e)


    

    def get_all_orders_interval_3(self):
        connect = self.connect()
        sql = f"SELECT * FROM status_statement WHERE first_call_moment >= NOW() - INTERVAL 3 DAY AND (notified IS null or notified = 0);"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            # for row in result:
                # print(row)
            
            return result
        except Error as e:
            print(e)


    def get_orders_tel_today(self, tel, date, subservice):
        connect = self.connect()
        sql = f"SELECT * FROM status_statement WHERE DATE(last_call_moment) = CURDATE() AND person_mobile='{tel}' AND DATE(date_creation) = DATE('{date}') AND subservice='{subservice}';"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            # for row in result:
                # print(row)
            
            return result
        except Error as e:
            print(e)



    def update_several_in_day(self, guid, several_in_day):
        connect = self.connect()

        sql = f"UPDATE status_statement SET several_in_day = CONCAT(several_in_day, ' {several_in_day}') WHERE guid = '{guid}';"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            connect.commit()
            connect.close()
        except Error as e:
            print(e)


    def get_orders_number_tel_today(self, tel, appeal_id):
        connect = self.connect()
        sql = f"SELECT * FROM status_statement where appeal_id='{appeal_id}' AND person_mobile='{tel}' AND DATE(last_call_moment) = CURDATE();"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            # for row in result:
                # print(row)
            
            return result
        except Error as e:
            print(e)





    def update_repeated_this_day(self, guid, repeated_this_day):
        connect = self.connect()
        sql = f"UPDATE status_statement SET repeated_day = CONCAT(repeated_day, ' {repeated_this_day}') WHERE guid = '{guid}';"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            connect.commit()
            connect.close()
        except Error as e:
            print(e)
        


    

    def get_orders_tel_dubly(self, tel, date, appeal_id):
        connect = self.connect()
        sql = f"SELECT * FROM status_statement WHERE appeal_id='{appeal_id}' AND person_mobile='{tel}' AND DATE(date_creation) = DATE('{date}');"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            # for row in result:
                # print(row)
            
            return result
        except Error as e:
            print(e)







    def get_orders_tel_subservice_one_day(self, tel, date, subservice):
        connect = self.connect()
        sql = f"SELECT * FROM status_statement WHERE subservice='{subservice}' AND person_mobile='{tel}' AND DATE(date_creation) = DATE('{date}');"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            # for row in result:
                # print(row)
            
            return result
        except Error as e:
            print(e)

    
        






    def update_several_in_day_orders(self, guid, united):
        connect = self.connect()

        sql = f"UPDATE status_statement SET united = CONCAT(united, ' {united}') WHERE guid = '{guid}';"
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            connect.commit()
            connect.close()
        except Error as e:
            print(e)




sql_init = MySQL("192.168.4.4", "r", ", "") 
