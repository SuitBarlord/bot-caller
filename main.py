from pymongo import MongoClient 
import pymongo
import datetime
import os
import schedule
import time
import paramiko
import sql_request
import sql_asterisk
from datetime import date, timedelta







def create_conf_aster_file(data_file):

    
            
            # Маска для файлов
            mask = "Avaya4_"
            save_path = "./output/"
            os.makedirs(save_path, exist_ok=True)
            # Генерация файлов

            # Генерация имени файла
            file_name = f"{mask}{data_file[0][1]}"
                # Полный путь к файлу
            file_path = os.path.join(save_path, file_name)
            tel = str(data_file[0][6]).replace("(", "").replace(")", "").replace("+", "").replace(" ", "")
            tel = "8" + tel[1:]
            tel = tel.strip()

                



                # Заполнение файла содержимым
            with open(file_path, 'w') as file:
                file.write(f'Channel: Local/{tel}@from-internal\n')
                file.write('Callerid: 9000\n')
                file.write('MaxRetries: 0\n')
                file.write('RetryTime: 1\n')
                file.write('WaitTime: 20\n')
                file.write('Account: 9000\n')
                file.write('Context: AutoInformerAvaya4\n')
                file.write('Extension: 9000\n')
                file.write('Priority: 1\n')

            print(f"Файл {file_name} успешно создан.")



# def check_aster_file():
#     folder_path = './aster_file/'  # указать путь к папке, в которой нужно провести проверку
#     prefix = 'Avaya4_'  # префикс имени файла

#     file_exists = False

#     for file_name in os.listdir(folder_path):
#         if file_name.startswith(prefix):
#             file_exists = True
#             break

#     if file_exists:
#         print("Файл с префиксом 'Avaya4 python' найден в папке")
#     else:
#         print("Файл с префиксом 'Avaya4 python' не найден в папке")

#     return file_exists





def check_aster_file():
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect("192.168.134.250", username="root", password="porcupine3") 
                command = "ls /var/spool/asterisk/outgoing/"

                # Выполнение команды на удаленном сервере
                stdin, stdout, stderr = ssh.exec_command(command)

                # Получение результатов выполнения команды
                output = stdout.readlines()
                output = [s.strip() for s in output]
                # print(output)
                ssh.close()
                file_exist = False
                avaya4_files = [file for file in output if "Avaya4" in file]
                # print(avaya4_files)
                if avaya4_files != []:
                     file_exist = True

                return file_exist






# def move_aster_file(file):
#     import shutil

#     file_path = f'./output/{file}'  # указать путь к исходному файлу
#     destination_folder = './aster_file/'  # указать путь к папке Python, в которую нужно переместить файл

#     shutil.move(file_path, destination_folder)




def move_aster_file(file):
    import shutil

    source_file = f"C:\mong_th_2\output\{file}"  # Путь к исходному файлу на Windows
    destination_dir = f"/var/opt/call_avaya4/{file}"  # Путь к целевой директории на Linux

    # source_audio = f"C:\mong_th_2\{audio}"
    # destination_dir_audio = f"/var/opt/call_avaya_audio/{audio}"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.134.250", username="root", password="porcupine3")  # Подключение к серверу Linux
    
    sftp = ssh.open_sftp()
    print("Соединение")
    sftp.put(source_file, destination_dir)  # Копирование файла с Windows на Linux
    sftp.close()


    # if audio == 'Государственная услуга по государственному кадастровому учету недвижимого имущества и (или) государственной регистрации прав на недвижимое имущество и сделок с ним':

    #     command_audio_2 = f"chown asterisk:asterisk /var/opt/call_avaya_audio/ros/4/msg4.wav"
    #     ssh.exec_command(command_audio_2)
    #     command_audio_4 = f"mv /var/opt/call_avaya_audio/ros/4/msg4.wav /var/lib/asterisk/sounds/ru/custom && chmod 664 /var/lib/asterisk/sounds/ru/custom/msg4.wav"
    #     ssh.exec_command(command_audio_4)
    # else:
    #     command_audio_2 = f"chown asterisk:asterisk /var/opt/call_avaya_audio/vse/4/msg4.wav"
    #     ssh.exec_command(command_audio_2)
    #     command_audio_4 = f"mv /var/opt/call_avaya_audio/vse/4/msg4.wav /var/lib/asterisk/sounds/ru/custom && chmod 664 /var/lib/asterisk/sounds/ru/custom/msg4.wav"
    #     ssh.exec_command(command_audio_4)


    # time.sleep(2)

    command = f"chmod -R 777 /var/opt/call_avaya4"
    ssh.exec_command(command)
    command_4 = f"chown asterisk:asterisk /var/opt/call_avaya4/{file}"
    ssh.exec_command(command_4)
    command_2 = f"mv /var/opt/call_avaya4/{file} /var/spool/asterisk/outgoing && chmod 777 /var/spool/asterisk/outgoing/{file}"
    ssh.exec_command(command_2)
    
    
    
    ssh.close()
    # os.remove(source_file)



# def send_file_sftp(file):
#     source_file = f"D:\mong\output\{file}"  # Путь к исходному файлу на Windows
#     destination_dir = f"/var/spool/asterisk/outgoing/{file}"  # Путь к целевой директории на Linux

#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect("192.168.134.250", username="root", password="porcupine3")  # Подключение к серверу Linux
    
#     sftp = ssh.open_sftp()
#     print("Соединение")
#     sftp.put(source_file, destination_dir)  # Копирование файла с Windows на Linux
    
#     sftp.close()
#     ssh.close()
    

def update_log(line):
     # Открываем файл для записи
    file = open("log.txt", "a", encoding="utf-8")


    # Записываем строки в файл построчно
    
    file.write(line + "\n")

    # Закрываем файл
    file.close()




# Пока не используется
def create_audio_file(subservice):
    import pyttsx3



    engine = pyttsx3.init()

    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)

    engine.say(f"Вас приветствует центр Мои Документы. Результат оказания услуги готов к выдаче {subservice}")
    engine.runAndWait()




    


def start():
    target_date = datetime.datetime.strptime('2023-11-24','%Y-%m-%d')
    current_time = datetime.datetime.now().time()
    start_time = datetime.time(hour=8)
    end_time = datetime.time(hour=20)
    if start_time <= current_time <= end_time:
            
        update_log(f"{datetime.datetime.now()} - Текущее время находится в интервале между 8 утра и 9 вечера. Запускаем скрипт обзвона...")
        print("Текущее время находится в интервале между 8 утра и 9 вечера.")

        # Подключение к базе 
        connect = MongoClient('mongodb://sier:9bpVRRN8moyH@192.168.223.203:27017,192.168.223.204:27017,192.168.223.213:27017/?replicaSet=sierrs&readPreference=primary&serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=sier&authMechanism=SCRAM-SHA-256') 
        # connect = MongoClient('mongodb://localhost:27017/')
        # Создание экземпляра базы sier
        db = connect.sier
        # Получение экземпляра коллекции appealMessages
        coll = db.appealMessages
        coll_appeals = db.appeals


        con = 0
        update_log(f"{datetime.datetime.now()} - Соединяемся с базой sier и получаем коллекцию appealMessages...")


        data_arr = []


        data_ob = {}

        now = datetime.datetime.now()

        # # Вычисляем вчерашнюю дату
        yesterday = now - datetime.timedelta(days=1)

        # # Устанавливаем время на 9 часов вечера
        # yesterday_9pm = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 12, 0, 0)



        i = 0 
        # desired_date = datetime(2023, 10, 24, 0, 5, 58, 762)
        # Получаем только готовые к выдачи, статус - звонок, дата с 9 вечера вчера и по сейчас 
        
        for value in coll.find({'message': 'Результат оказания услуги готов к выдаче', 'type.code': 'call',  'dateCreation': { '$gt' : target_date },      "$and": [ { "appeal.subservice": { "$ne": "Регистрация, подтверждение, восстановление и удаление УЗ в ЕСИА (универсальная)" } }, { "appeal.subservice": { "$ne": "Информирование физических лиц о налоговой задолженности и выдача платежных документов" } }, { "appeal.subservice": { "$ne": "Получение в МФЦ результата оказания услуги от ЕПГУ" } }, { "appeal.subservice": { "$ne": "Информирование застрахованных лиц о состоянии их индивидуальных лицевых счетов в системе обязательного пенсионного страхования согласно федеральным законам «Об индивидуальном (персонифицированном) учете в системе обязательного пенсионного страхования» и «Об инвестировании средств для финансирования накопительной пенсии в Российской Федерации»" }},
        { "appeal.subservice": { "$ne": "Предоставление сведений о трудовой деятельности зарегистрированного лица, содержащихся в его индивидуальном лицевом счете" } }, { "appeal.subservice": { "$ne": "Информирование граждан об отнесении к категории граждан предпенсионного возраста"} }, { "appeal.subservice": { "$ne": "Предоставление информации по находящимся на исполнении исполнительным производствам в отношении физического и юридического лица"} }, { "appeal.subservice": { "$ne": "Прием заявлений для размещения сведений о транспортном средстве, управляемом инвалидом, или транспортном средстве, перевозящем инвалида и (или) ребенка-инвалида, в федеральной государственной информационной системе \"Федеральный реестр инвалидов\""} },  { "appeal.subservice": { "$ne": "Предоставление физическим лицом отказа от сбора и размещения биометрических персональных данных в целях проведения идентификации и (или) аутентификации, отзыва такого отказа"} } ] }):
            if start_time <= current_time <= end_time:
                
            
                update_log(f"{datetime.datetime.now()} - Получаем из базы sier готовые к выдачи заявления...")
                # print(value)
                # Разница с кол-во записями в базе 25
                i = i + 1
                # Получаем запись по appeal guid
                try:
                    result = sql_request.sql_init.get_by_id_orders(value['guid'])
                    update_log(f"{datetime.datetime.now()} - Проверка на сушествование записи дела - {value['guid']} в таблице status_statement...")
                except ValueError as e:
                    update_log(f"{datetime.datetime.now()} - Ошибка - {e} ")
                # Проверяем есть ли такая запись в базе
                try:
                    if result == []:
                        from bson.objectid import ObjectId
                        order = coll_appeals.find_one({'_id': ObjectId(f"{value['appeal']['_id']}")})
                        if order['status']['name'] == 'Выдано':
                            pass
                        else:
                            appeal_id = sql_request.sql_init.get_by_appeal_id_orders(value['appeal']['_id'])
                            if appeal_id == []:
                                date_string = str(value['dateCreation'])
                                date_creation_t = date_string.split("T")[0]
                                orders_tel_today = sql_request.sql_init.get_orders_tel_today(value['person']['mobile'], date_creation_t, value['appeal']['subservice'])
                                if orders_tel_today != []:
                                    several_in_day_array = str(orders_tel_today[0][18]).split()
                                    if str(value['guid']) in several_in_day_array:
                                        pass
                                    else:
                                        sql_request.sql_init.update_several_in_day(orders_tel_today[0][1], value['guid'])
                                        united_in_day_array = str(orders_tel_today[0][20]).split()
                                        if str(value['guid']) in united_in_day_array:
                                            sql_request.sql_init.update_several_in_day_orders(orders_tel_today[0][1], value['appeal']['number'])
                                            pass
                                        else:
                                            pass

                                else:
                                    
                                    # tel_appeal = sql_request.sql_init.get_by_tel_orders(value['person']['mobile'])
                                    # if tel_appeal != []:
                                    #     pass
                                    # orders_tel_today_array = orders_tel_today
                                    # for el in orders_tel_today_array:
                                    #     el 
                                    date_string_t_several = str(value['dateCreation'])
                                    date_creation_t_several = date_string_t_several.split("T")[0]
                                    get_orders_tel_subservice_one_day = sql_request.sql_init.get_orders_tel_subservice_one_day(value['person']['mobile'], date_creation_t_several, value['appeal']['subservice'])
                                    if get_orders_tel_subservice_one_day != []:
                                        get_orders_tel_subservice_one_day_array = str(get_orders_tel_subservice_one_day[0][18]).split()
                                        if str(value['guid']) in get_orders_tel_subservice_one_day_array:
                                            update_log(f"{datetime.datetime.now()} - {value['guid']} пропущен по причине объединения дел в один звонок.")
                                            pass
                                    else:



                                        update_log(f"{datetime.datetime.now()} - Такой записи нет, записываем в status_statement.")

                                        from bson.objectid import ObjectId
                                        executor_order = coll_appeals.find_one({'_id': ObjectId(f"{value['appeal']['_id']}")})
                                        print(executor_order)
                                        executor_order_last = ''
                                        if executor_order['userLastModification'] == None:
                                            executor_order_last = executor_order['userCreation']['name']
                                        else:
                                            executor_order_last = executor_order['userLastModification']['name']
                                        several_in_day = ' '
                                        repeated_day = ' '
                                        united = ' '
                                        try:
                                        # Если нет такой записи в базе то добавляем ее
                                            sql_request.sql_init.set_new_order(value['guid'], value['appeal']['_id'], value['appeal']['number'], value['appeal']['shortNumber'], value['person']['fio'], value['person']['mobile'], value['appeal']['subservice'], value['dateCreation'], executor_order['status']['user']['name'], executor_order['userCreation']['name'], executor_order_last, several_in_day, repeated_day, united) 
                                        except TypeError as e:
                                            update_log(f"{datetime.datetime.now()} - Ошибка - {e} ")
                                            continue

                                        # Запрашиваем только что добавленную запись
                                        result = sql_request.sql_init.get_by_id_orders(value['guid'])
                                        # create_time = datetime.datetime.strptime(result[0][8],'%Y-%m-%d')
                                        # target_date_2 = datetime.datetime.strptime('2023-12-18','%Y-%m-%d')
                                        # Проверяем есть ли вызов по этому ордеру в данный момент
                                        if result[0][13] == 1:
                                            pass
                                        elif result[0][6] == '+7(914) 492 30 49':
                                            pass
                                        # elif result[0][7] == 'Выдача гражданам справок о размере пенсий (иных выплат)' and create_time < target_date_2:
                                        #      pass
                                        else:
                                            # Если нет текущего вызова, проверяем был ли вообще звонок, если нет то создаем файл конф. для asteriska
                                            if result[0][9] == None and result[0][10] == None:
                                                update_log(f"{datetime.datetime.now()} - Создаем callfile для asteriska...")
                                                create_conf_aster_file(result)
                                                time.sleep(4)
                                                # Пока есть файл в папке astera, ждем
                                                if check_aster_file() == True:
                                                    while check_aster_file() == True:
                                                        time.sleep(8)
                                                        print("Жду...")
                                                # Если файла нет, то отправляем файл в папку astera
                                                update_log(f"{datetime.datetime.now()} - Отправляем файл Avaya4_{result[0][1]} в папку astera...")
                                                print("Отправляем файл в папку astera...")
                                                move_aster_file(f'Avaya4_{result[0][1]}')
                                                time.sleep(4)
                                                # Получаем номер телефона заявителя и приводим его в формат для запроса в базу asterisk
                                                tel = str(result[0][6]).replace("(", "").replace(")", "").replace("+", "").replace(" ", "")
                                                tel = "8" + tel[1:]
                                                tel = tel.strip()
                                                print(tel)
                                                # print(sql_asterisk.sql_init.get_call_by_mobile(tel))
                                                update_log(f"{datetime.datetime.now()} - Спим 15 сек... на текущем исполнении дело с id - {result[0][2]}")
                                                print("Спим 15 сек...")
                                                time.sleep(15)
                                                # Проверяем, был ли звонок по этому номеру в базе самого asteriska
                                                if sql_asterisk.sql_init.get_call_by_mobile(tel) == []:
                                                    # Если, нет то спим 10 сек
                                                    while sql_asterisk.sql_init.get_call_by_mobile(tel) == []:
                                                        print("Спим 10 сек...")
                                                        time.sleep(10)
                                                # Если есть или появился, то смотрим дату и меняем данные о звонке исходя из статуса в базе asteriska 
                                                if sql_asterisk.sql_init.get_call_by_mobile(tel) != []:
                                                    # ////
                                                    # Получаем дату первого звонока по номеру телефона 
                                                    try:
                                                        first_call_moment = sql_asterisk.sql_init.get_first_moment_call_by_mobile(tel)[0][0]
                                                        print(first_call_moment)
                                                    except:
                                                        time.sleep(4)
                                                        first_call_moment = sql_asterisk.sql_init.get_first_moment_call_by_mobile(tel)[0][0]
                                                    # Ставим дату первого звонка в базу 
                                                    sql_request.sql_init.update_first_call_by_id(result[0][1], first_call_moment)
                                                    # Ставим сразу дату крайнего звонка в базу, при первом обзвоне первый и будет крайним
                                                    sql_request.sql_init.update_last_call_by_id(result[0][1], first_call_moment)
                                                    # Если есть запись в базе asterisk того, что звонок прошел
                                                    if sql_asterisk.sql_init.get_first_moment_call_by_mobile(tel) != []:
                                                        update_log(f"{datetime.datetime.now()} - Ждем статуса звонка... по номеру - {tel}.")
                                                        print("Ждем статуса звонка...")
                                                        time.sleep(5)
                                                        # Проверяем какой статус звонка
                                                        # print(sql_asterisk.sql_init.get_first_call_status_by_mobile(tel)[0][11])
                                                        print(sql_asterisk.sql_init.get_last_call_status_by_mobile(tel))
                                                        if sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][11] == 'ANSWERED':
                                                            sql_request.sql_init.update_call_status_by_id(result[0][1], 2)
                                                            # Если статус звонка  - 2, отвечен, то проверяем породолжительность соединения
                                                            if int(sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][10]) > 7:
                                                                # Если продолжительность соединения больше 7 сек, то ставим статус в обращении - 1, оповещен
                                                                sql_request.sql_init.update_notified_call_by_id(result[0][1], 1)
                                                            else:
                                                                # Если менее 7 сек, то ставим - 0, неоповещен 
                                                                sql_request.sql_init.update_notified_call_by_id(result[0][1], 0)
                                                        elif sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][11] == 'BUSY':
                                                            sql_request.sql_init.update_call_status_by_id(result[0][1], 1)
                                                        elif sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][11] == 'NO ANSWER':
                                                            if sql_asterisk.sql_init.get_last_call_status_by_mobile_if_notanw(tel) != []:
                                                                sql_request.sql_init.update_call_status_by_id(result[0][1], 2)
                                                                sql_request.sql_init.update_notified_call_by_id(result[0][1], 1)
                                                            else:
                                                                sql_request.sql_init.update_call_status_by_id(result[0][1], 0)
                                                    update_log(f"{datetime.datetime.now()} - Статус получен. {result[0][1]}")
                            
                            elif appeal_id != []:
                                tel_appeal = sql_request.sql_init.get_by_tel_orders(value['appeal']['_id'], value['person']['mobile'])
                                if tel_appeal == []:
                                    # update_log(f"{datetime.datetime.now()} - Такой записи нет, записываем в status_statement.")

                                    from bson.objectid import ObjectId
                                    executor_order = coll_appeals.find_one({'_id': ObjectId(f"{value['appeal']['_id']}")})
                                    print(executor_order)
                                    executor_order_last = ''
                                    if executor_order['userLastModification'] == None:
                                        executor_order_last = executor_order['userCreation']['name']
                                    else:
                                        executor_order_last = executor_order['userLastModification']['name']

                                    several_in_day = ' '
                                    repeated_day = ' '
                                    united = ' '
                                    try:
                                    # Если нет такой записи в базе то добавляем ее
                                        sql_request.sql_init.set_new_order(value['guid'], value['appeal']['_id'], value['appeal']['number'], value['appeal']['shortNumber'], value['person']['fio'], value['person']['mobile'], value['appeal']['subservice'], value['dateCreation'], executor_order['status']['user']['name'], executor_order['userCreation']['name'], executor_order_last, several_in_day, repeated_day, united) 
                                    except TypeError as e:
                                        update_log(f"{datetime.datetime.now()} - Ошибка - {e} ")
                                        continue

                                    # Запрашиваем только что добавленную запись
                                    result = sql_request.sql_init.get_by_id_orders(value['guid'])
                                    # create_time = datetime.datetime.strptime(result[0][8],'%Y-%m-%d')
                                    # target_date_2 = datetime.datetime.strptime('2023-12-18','%Y-%m-%d')
                                    # Проверяем есть ли вызов по этому ордеру в данный момент
                                    if result[0][13] == 1:
                                        pass
                                    elif result[0][6] == '+7(914) 492 30 49':
                                        pass
                                    # elif result[0][7] == 'Выдача гражданам справок о размере пенсий (иных выплат)' and create_time < target_date_2:
                                    #      pass
                                    else:
                                        # Если нет текущего вызова, проверяем был ли вообще звонок, если нет то создаем файл конф. для asteriska
                                        if result[0][9] == None and result[0][10] == None:
                                            update_log(f"{datetime.datetime.now()} - Создаем callfile для asteriska...")
                                            create_conf_aster_file(result)
                                            time.sleep(4)
                                            # Пока есть файл в папке astera, ждем
                                            if check_aster_file() == True:
                                                while check_aster_file() == True:
                                                    time.sleep(8)
                                                    print("Жду...")
                                            # Если файла нет, то отправляем файл в папку astera
                                            update_log(f"{datetime.datetime.now()} - Отправляем файл Avaya4_{result[0][1]} в папку astera...")
                                            print("Отправляем файл в папку astera...")
                                            move_aster_file(f'Avaya4_{result[0][1]}')
                                            time.sleep(4)
                                            # Получаем номер телефона заявителя и приводим его в формат для запроса в базу asterisk
                                            tel = str(result[0][6]).replace("(", "").replace(")", "").replace("+", "").replace(" ", "")
                                            tel = "8" + tel[1:]
                                            tel = tel.strip()
                                            print(tel)
                                            # print(sql_asterisk.sql_init.get_call_by_mobile(tel))
                                            update_log(f"{datetime.datetime.now()} - Спим 15 сек... на текущем исполнении дело с id - {result[0][2]}")
                                            print("Спим 15 сек...")
                                            time.sleep(15)
                                            # Проверяем, был ли звонок по этому номеру в базе самого asteriska
                                            if sql_asterisk.sql_init.get_call_by_mobile(tel) == []:
                                                # Если, нет то спим 10 сек
                                                while sql_asterisk.sql_init.get_call_by_mobile(tel) == []:
                                                    print("Спим 10 сек...")
                                                    time.sleep(10)
                                            # Если есть или появился, то смотрим дату и меняем данные о звонке исходя из статуса в базе asteriska 
                                            if sql_asterisk.sql_init.get_call_by_mobile(tel) != []:
                                                # ////
                                                # Получаем дату первого звонока по номеру телефона 
                                                try:
                                                    first_call_moment = sql_asterisk.sql_init.get_first_moment_call_by_mobile(tel)[0][0]
                                                    print(first_call_moment)
                                                except:
                                                    time.sleep(4)
                                                    first_call_moment = sql_asterisk.sql_init.get_first_moment_call_by_mobile(tel)[0][0]
                                                # Ставим дату первого звонка в базу 
                                                sql_request.sql_init.update_first_call_by_id(result[0][1], first_call_moment)
                                                # Ставим сразу дату крайнего звонка в базу, при первом обзвоне первый и будет крайним
                                                sql_request.sql_init.update_last_call_by_id(result[0][1], first_call_moment)
                                                # Если есть запись в базе asterisk того, что звонок прошел
                                                if sql_asterisk.sql_init.get_first_moment_call_by_mobile(tel) != []:
                                                    update_log(f"{datetime.datetime.now()} - Ждем статуса звонка... по номеру - {tel}.")
                                                    print("Ждем статуса звонка...")
                                                    time.sleep(5)
                                                    # Проверяем какой статус звонка
                                                    # print(sql_asterisk.sql_init.get_first_call_status_by_mobile(tel)[0][11])
                                                    print(sql_asterisk.sql_init.get_last_call_status_by_mobile(tel))
                                                    if sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][11] == 'ANSWERED':
                                                        sql_request.sql_init.update_call_status_by_id(result[0][1], 2)
                                                        # Если статус звонка  - 2, отвечен, то проверяем породолжительность соединения
                                                        if int(sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][10]) > 7:
                                                            # Если продолжительность соединения больше 7 сек, то ставим статус в обращении - 1, оповещен
                                                            sql_request.sql_init.update_notified_call_by_id(result[0][1], 1)
                                                        else:
                                                            # Если менее 7 сек, то ставим - 0, неоповещен 
                                                            sql_request.sql_init.update_notified_call_by_id(result[0][1], 0)
                                                    elif sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][11] == 'BUSY':
                                                        sql_request.sql_init.update_call_status_by_id(result[0][1], 1)
                                                    elif sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][11] == 'NO ANSWER':
                                                        if sql_asterisk.sql_init.get_last_call_status_by_mobile_if_notanw(tel) != []:
                                                            sql_request.sql_init.update_call_status_by_id(result[0][1], 2)
                                                            sql_request.sql_init.update_notified_call_by_id(result[0][1], 1)
                                                        else:
                                                            sql_request.sql_init.update_call_status_by_id(result[0][1], 0)
                                                update_log(f"{datetime.datetime.now()} - Статус получен. {result[0][1]}")
                                
                                elif tel_appeal != []:
                                    date_string_2 = str(value['dateCreation'])
                                    date_creation_t_dybli = date_string_2.split("T")[0]
                                    orders_tel_dubly = sql_request.sql_init.get_orders_tel_dubly(value['person']['mobile'], date_creation_t_dybli, value['appeal']['_id'])
                                    if orders_tel_dubly == []:
                                        call_update_today = sql_request.sql_init.get_orders_number_tel_today(value['person']['mobile'], value['appeal']['_id'])
                                        if call_update_today == []:
                                            from bson.objectid import ObjectId
                                            executor_order = coll_appeals.find_one({'_id': ObjectId(f"{value['appeal']['_id']}")})
                                            print(executor_order)
                                            executor_order_last = ''
                                            if executor_order['userLastModification'] == None:
                                                executor_order_last = executor_order['userCreation']['name']
                                            else:
                                                executor_order_last = executor_order['userLastModification']['name']

                                            several_in_day = ' '
                                            repeated_day = ' '
                                            united = ' '
                                            try:
                                            # Если нет такой записи в базе то добавляем ее
                                                sql_request.sql_init.set_new_order(value['guid'], value['appeal']['_id'], value['appeal']['number'], value['appeal']['shortNumber'], value['person']['fio'], value['person']['mobile'], value['appeal']['subservice'], value['dateCreation'], executor_order['status']['user']['name'], executor_order['userCreation']['name'], executor_order_last, several_in_day, repeated_day, united) 
                                            except TypeError as e:
                                                update_log(f"{datetime.datetime.now()} - Ошибка - {e} ")
                                                continue

                                            # Запрашиваем только что добавленную запись
                                            result = sql_request.sql_init.get_by_id_orders(value['guid'])
                                            # create_time = datetime.datetime.strptime(result[0][8],'%Y-%m-%d')
                                            # target_date_2 = datetime.datetime.strptime('2023-12-18','%Y-%m-%d')
                                            # Проверяем есть ли вызов по этому ордеру в данный момент
                                            if result[0][13] == 1:
                                                pass
                                            elif result[0][6] == '+7(914) 492 30 49':
                                                pass
                                            # elif result[0][7] == 'Выдача гражданам справок о размере пенсий (иных выплат)' and create_time < target_date_2:
                                            #      pass
                                            else:
                                                # Если нет текущего вызова, проверяем был ли вообще звонок, если нет то создаем файл конф. для asteriska
                                                if result[0][9] == None and result[0][10] == None:
                                                    update_log(f"{datetime.datetime.now()} - Создаем callfile для asteriska...")
                                                    create_conf_aster_file(result)
                                                    time.sleep(4)
                                                    # Пока есть файл в папке astera, ждем
                                                    if check_aster_file() == True:
                                                        while check_aster_file() == True:
                                                            time.sleep(8)
                                                            print("Жду...")
                                                    # Если файла нет, то отправляем файл в папку astera
                                                    update_log(f"{datetime.datetime.now()} - Отправляем файл Avaya4_{result[0][1]} в папку astera...")
                                                    print("Отправляем файл в папку astera...")
                                                    move_aster_file(f'Avaya4_{result[0][1]}')
                                                    time.sleep(4)
                                                    # Получаем номер телефона заявителя и приводим его в формат для запроса в базу asterisk
                                                    tel = str(result[0][6]).replace("(", "").replace(")", "").replace("+", "").replace(" ", "")
                                                    tel = "8" + tel[1:]
                                                    tel = tel.strip()
                                                    print(tel)
                                                    # print(sql_asterisk.sql_init.get_call_by_mobile(tel))
                                                    update_log(f"{datetime.datetime.now()} - Спим 15 сек... на текущем исполнении дело с id - {result[0][2]}")
                                                    print("Спим 15 сек...")
                                                    time.sleep(15)
                                                    # Проверяем, был ли звонок по этому номеру в базе самого asteriska
                                                    if sql_asterisk.sql_init.get_call_by_mobile(tel) == []:
                                                        # Если, нет то спим 10 сек
                                                        while sql_asterisk.sql_init.get_call_by_mobile(tel) == []:
                                                            print("Спим 10 сек...")
                                                            time.sleep(10)
                                                    # Если есть или появился, то смотрим дату и меняем данные о звонке исходя из статуса в базе asteriska 
                                                    if sql_asterisk.sql_init.get_call_by_mobile(tel) != []:
                                                        # ////
                                                        # Получаем дату первого звонока по номеру телефона 
                                                        try:
                                                            first_call_moment = sql_asterisk.sql_init.get_first_moment_call_by_mobile(tel)[0][0]
                                                            print(first_call_moment)
                                                        except:
                                                            time.sleep(4)
                                                            first_call_moment = sql_asterisk.sql_init.get_first_moment_call_by_mobile(tel)[0][0]
                                                        # Ставим дату первого звонка в базу 
                                                        sql_request.sql_init.update_first_call_by_id(result[0][1], first_call_moment)
                                                        # Ставим сразу дату крайнего звонка в базу, при первом обзвоне первый и будет крайним
                                                        sql_request.sql_init.update_last_call_by_id(result[0][1], first_call_moment)
                                                        # Если есть запись в базе asterisk того, что звонок прошел
                                                        if sql_asterisk.sql_init.get_first_moment_call_by_mobile(tel) != []:
                                                            update_log(f"{datetime.datetime.now()} - Ждем статуса звонка... по номеру - {tel}.")
                                                            print("Ждем статуса звонка...")
                                                            time.sleep(5)
                                                            # Проверяем какой статус звонка
                                                            # print(sql_asterisk.sql_init.get_first_call_status_by_mobile(tel)[0][11])
                                                            print(sql_asterisk.sql_init.get_last_call_status_by_mobile(tel))
                                                            if sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][11] == 'ANSWERED':
                                                                sql_request.sql_init.update_call_status_by_id(result[0][1], 2)
                                                                # Если статус звонка  - 2, отвечен, то проверяем породолжительность соединения
                                                                if int(sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][10]) > 7:
                                                                    # Если продолжительность соединения больше 7 сек, то ставим статус в обращении - 1, оповещен
                                                                    sql_request.sql_init.update_notified_call_by_id(result[0][1], 1)
                                                                else:
                                                                    # Если менее 7 сек, то ставим - 0, неоповещен 
                                                                    sql_request.sql_init.update_notified_call_by_id(result[0][1], 0)
                                                            elif sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][11] == 'BUSY':
                                                                sql_request.sql_init.update_call_status_by_id(result[0][1], 1)
                                                            elif sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][11] == 'NO ANSWER':
                                                                if sql_asterisk.sql_init.get_last_call_status_by_mobile_if_notanw(tel) != []:
                                                                    sql_request.sql_init.update_call_status_by_id(result[0][1], 2)
                                                                    sql_request.sql_init.update_notified_call_by_id(result[0][1], 1)
                                                                else:
                                                                    sql_request.sql_init.update_call_status_by_id(result[0][1], 0)
                                                        update_log(f"{datetime.datetime.now()} - Статус получен. {result[0][1]}")

                                        elif call_update_today != []:
                                            # sql_request.sql_init.update_repeated_this_day(call_update_today[0][1], value['guid'])
                                            pass

                                    elif orders_tel_dubly != []:
                                        orders_tel_dubly_array = str(orders_tel_dubly[0][19]).split()
                                        if str(value['guid']) in orders_tel_dubly_array:
                                            pass
                                        else:
                                            sql_request.sql_init.update_repeated_this_day(orders_tel_dubly[0][1], value['guid'])
                                            pass
                    # Если есть запись по заялению, то проверяем статус звонка
                    # elif result != []:
                    #     update_log(f"{datetime.datetime.now()} - Есть запись о деле id - {result[0][2]}")
                    #     print("Есть запись")
                    #     if result[0][14] == 1:
                    #         update_log(f"{datetime.datetime.now()} - Пропуск т.к. оповещен - {result[0][2]}")
                    #         pass
                    #     elif result[0][6] == '+7(914) 492 30 49':
                    #         pass
                    #     else:
                    #         # Если статус звонка - 2, дозвонился, то пропускаем
                    #         if result[0][14] == 1:
                    #             pass
                    #         # Если статус - 1, занят, то проверяем когда звонил крайний раз
                    #         elif result[0][10] == '1' or result[0][10] == '0' or result[0][14] == 0:
                    #             now_t = datetime.datetime.now()
                    #             # start_time = datetime.datetime(2022, 1, 1)
                    #             # Разница во времени между текущей датой и заданным временем
                    #             start_time_t = datetime.datetime.strptime(result[0][9], "%Y-%m-%d %H:%M:%S")
                    #             time_difference_t = now_t - start_time_t
                    #             if time_difference_t.total_seconds() > 172800:
                    #                 print("Прошло более 2 дней")
                    #                 sql_request.sql_init.update_notified_call_by_id(result[0][2], 1)
                    #                 update_log(f"{datetime.datetime.now()} - Пропуск т.к. Прошло более 3 дней, ставим статус оповещен - {result[0][2]}")
                    #                 # pass
                    #             else:
                    #             # if result[0][14] == '0':
                    #             #     update_log(f"{datetime.datetime.now()} - Статус - 0 - {result[0][2]}")
                    #             # update_log(f"{datetime.datetime.now()} - Проверяем прошлый звонок... - {result[0][2]}")
                    #                 time_now = datetime.datetime.now()
                    #                 # Вычисляем разницу между текущей и заданной датой
                    #                 date_object = datetime.datetime.strptime(result[0][12], "%Y-%m-%d %H:%M:%S")
                    #                 difference = time_now - date_object
                    #                 # Проверяем разницу с текущей датой
                    #                 print(difference.total_seconds())
                    #                 if difference.total_seconds() > 84600:
                    #                     update_log(f"{datetime.datetime.now()} - Прошло больше суток с момента крайнего звонка, звоним... - {result[0][2]}")
                    #                     print("Прошло более суток ...")
                    #                     if check_aster_file() == True:
                    #                         while check_aster_file() == True:
                    #                             time.sleep(20)
                    #                     # Передаем файл в папку asteriska
                    #                     move_aster_file(f'Avaya4_{result[0][1]}')
                    #                     # Спим 20 сек
                    #                     time.sleep(55)
                    #                     # end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    #                     time_now_s = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    #                     # Получение времени втечении 2 мин
                    #                     # start_time = end_time - timedelta(minutes=2)
                    #                     # Преобразуем телефон для запроса в базу asteriska 
                    #                     tel = str(result[0][6]).replace("(", "").replace(")", "").replace("+", "").replace(" ", "")
                    #                     tel = "8" + tel[1:]
                    #                     tel = tel.strip()
                    #                     # Если за крайние 2 минуты, нет статуса по номеру телефона текущего дела, то пока нет статуса спать 4 секунды
                    #                     if sql_asterisk.sql_init.get_call_by_mobile(tel) == []:
                    #                         while sql_asterisk.sql_init.get_call_by_mobile(tel) == []:
                    #                             update_log(f"{datetime.datetime.now()} - Ждем статуса звонка... Аварийно! - {result[0][2]}")
                    #                             time.sleep(4)
                    #                     else:
                    #                         # Проверяем был ли звонок втечении крайних 2 мин по номеру телефона
                    #                         if sql_asterisk.sql_init.get_call_by_mobile(tel) != []:
                    #                             sql_request.sql_init.update_last_call_by_id(result[0][2], time_now_s)
                    #                             # Если есть, то проверяем статус крайнего статуса по этому номеру телефона
                    #                             update_log(f"{datetime.datetime.now()} - Ставим статус звонка. - {result[0][2]}")
                    #                             if sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][11] == 'ANSWERED':
                    #                                 sql_request.sql_init.update_call_status_by_id(result[0][2], 2)
                    #                                 if int(sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][10]) > 7:
                    #                                     sql_request.sql_init.update_notified_call_by_id(result[0][2], 1)
                    #                                 else:
                    #                                     sql_request.sql_init.update_notified_call_by_id(result[0][2], 0)
                    #                             elif sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][11] == 'BUSY':
                    #                                     sql_request.sql_init.update_call_status_by_id(result[0][2], 1)
                    #                             elif sql_asterisk.sql_init.get_last_call_status_by_mobile(tel)[0][11] == 'NO ANSWER':
                    #                                 if sql_asterisk.sql_init.get_last_call_status_by_mobile_if_notanw(tel) != []:
                    #                                     sql_request.sql_init.update_call_status_by_id(result[0][2], 2)
                    #                                     sql_request.sql_init.update_notified_call_by_id(result[0][2], 1)
                    #                                 else:
                    #                                     sql_request.sql_init.update_call_status_by_id(result[0][2], 0)
                    #                         update_log(f"{datetime.datetime.now()} - Статус получен. {result[0][2]}")
                    #                         time.sleep(40)
                                        
                    #                 elif difference.total_seconds() < 84600:
                    #                     update_log(f"{datetime.datetime.now()} - Не прошло суток с момента крайнего звонка по делу - {result[0][2]}")
                    #                     pass
                                
                except ValueError as e:
                    update_log(f"{datetime.datetime.now()} - Аварийный пропуск заявления, ошибка - {e}")
                    pass

            
            else:
                print("Прерывание, нерабочее время.")
                break
        print(i)
            
    else:
         print("Нерабочее время")
        #     if value['message'] == "Результат оказания услуги готов к выдаче":






schedule.every(20).seconds.do(start)


while True:
    schedule.run_pending()
    time.sleep(1)