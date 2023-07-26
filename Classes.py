import psycopg2

from datetime import datetime

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.keyboard import VkKeyboard



bot_token = "vk1.a.NQ2S9IO3Lt5p7zdGLo0UiO67Ek5hKS-0P22AGUsjJPsefEfnZoPQQ2SSv-wKivRbQz7VaCw8fHZ56SkbNIM1-9MtO5iVRBMoVJki381L-vxK6Q2WdrhotEuOq3Jk6ibUXUQn_Lxd-JJSp6U8FdeoG4jkGAG5RQu7Gig238xGRsvP9Nb1As0kndXL2VPn21AQJ9CaHQgpWQeD7--WBxCeAg"
bot_id = "221168754"
longpoll = VkBotLongPoll(vk_api.VkApi(token=bot_token), bot_id)
vk = vk_api.VkApi(token=bot_token).get_api()

user_token = "vk1.a.moyaZRvoKnv9v4ORBwCZ4GHIv_pOl-7yXd1dfRmjx8GWi8LF_Q_exEfsGgwykbftp6QSCOy5os4HjVaFYdK7eQdG0wWO0PWaxwzK0RuG0zlZd6ODpX2uI0rqOUELDY9C-FYtzQdd1sCLPw6G0XKARkDu-2uYfaQM1mgBiqlaXcHNOvS1bagQ708LRM5CW2oAzk7zlr9XJbzDbuqlzcNcHw"
user_vk = vk_api.VkApi(token=user_token).get_api()



class Keyboards:

    __instance = None
    
    def __new__(cls, *args, **kwargs):
        
        if not Keyboards.__instance:
            Keyboards.__instance = super(Keyboards, cls).__new__(cls, *args, **kwargs)
        return Keyboards.__instance


    def menu(self):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Поиск')
        keyboard.add_line()  
        keyboard.add_button('Обновить профиль')
        return keyboard


    def create(self):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Создать профиль')
        return keyboard


    def search(self):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('👍')
        keyboard.add_button('👎')
        keyboard.add_line()
        keyboard.add_button('Меню')
        return keyboard


    def search_next(self):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Продолжить')
        keyboard.add_line()
        keyboard.add_button('Меню')
        return keyboard



class SQL:

    __instance = None
    
    def __new__(cls, *args, **kwargs):
        
        if not SQL.__instance:
            try:
                
                self.connection = psycopg2.connect(
                    host="localhost",
                    port="4532",
                    database="postgres",
                    user="postgres",
                    password="123456"
                )
                print("База данных подключена")
            except (Exception, psycopg2.Error) as e:
                print("База данных не подключена:", e)
            SQL.__instance = super(SQL, cls).__new__(cls, *args, **kwargs)
        return SQL.__instance


    # Создание таблиц в базе данных

    def init_database(self): 
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS MyProfile (MyID INTEGER, MyCity TEXT,\
                            MyAge INTEGER, MySex INTEGER, MyRelation INTEGER, MyOffset INTEGER, CurrentID INTEGER);")

            cursor.execute("CREATE TABLE IF NOT EXISTS Match (VK_ID INTEGER, Result BOOLEAN);")
                                    
            cursor.execute("CREATE TABLE IF NOT EXISTS Users (VK_ID INTEGER, Name TEXT, Relation INTEGER);")


    # Взаимодействие с таблицей MyProfile

    def insert_my_profile(self, ID, City, Age, Sex, Relation): 
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT OR IGNORE INTO MyProfile (MyID, MyCity, MyAge, MySex, MyRelation,\
                            MyOffset, CurrentID) VALUES ('{ID}', '{City}', '{Age}', '{Sex}', '{Relation}', '0', '');")
            
    def update_my_profile(self, ID, City, Age, Sex, Relation): 
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE MyProfile SET MyID = '{ID}', MyCity = '{City}', MyAge = '{Age}',\
                            MySex = '{Sex}', MyRelation = '{Relation}' WHERE MyID = '{ID}';")

    def check_my_profile(self, ID): 
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT EXISTS (SELECT 1 FROM MyProfile WHERE MyID = {ID})")
            answer = cursor.fetchone()[0]
            return bool(answer)

    def get_my_profile(self, ID):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM MyProfile WHERE MyID = {ID}")
            answer = cursor.fetchone()
            return answer

    def set_my_offset(self, ID, offset): 
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE MyProfile SET MyOffset = {offset} WHERE MyID = {ID}")

    def add_my_offset(self, ID, Count): 
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE MyProfile SET MyOffset = MyOffset + {Count} WHERE MyID = {ID}")

    def set_current_id(self, ID, CurrentID): 
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE MyProfile SET CurrentID = {CurrentID} WHERE MyID = {ID}")

    def get_current_id(self, ID): 
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT CurrentID FROM MyProfile WHERE MyID = {ID}")
            answer = cursor.fetchone()
            return answer

    # Взаимодействие с таблицей Match

    def insert_match(self, ID, Result): 
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT INTO Match (VK_ID, Result) VALUES ('{ID}', '{Result}');")
            
    def check_match(self, ID):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM Match WHERE VK_ID = {ID}")
            answer = cursor.fetchone()[0]
            return answer == 0

    def delete_match(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM Match")


    # Взаимодействие с таблицей Users

    def insert_users(self, ID, Name, Relation): 
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT INTO Users (VK_ID, Name, Relation) VALUES ('{ID}', '{Name}', '{Relation}');")

    def get_user(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM Users LIMIT 1")
            answer = cursor.fetchone()
            return answer

    def delete_users(self, ID):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM Users WHERE VK_ID = {ID};")

    def count_users(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM Users")
            answer = cursor.fetchone()[0]
            return int(answer) != 0 



class MainFuncs():

    database = SQL()
    keyboard = Keyboards()
    Offset = 30

    relations = {
        1: 'Не женат/Не замужем',
        2: 'Есть друг/Подруга',
        3: 'Помолвлен/Помолвлена',
        4: 'Женат/Замужем',
        5: 'Всё сложно',
        6: 'В активном поиске',
        7: 'Влюблён/Влюблена',
        8: 'В гражданском браке'
        }


    def send(self, user_id, message, keyboard, images):
        adds = ""
        for i in images:
            adds += f"photo{i['owner_id']}_{i['id']},"
        vk.messages.send(user_id = user_id, message = message, attachment = adds,
                         keyboard = keyboard.get_keyboard(), random_id = vk_api.utils.get_random_id())
    

    def age(self, date):
        if not date:
            return "Не указан"

        date_split = date.split('.')
        if len(date_split) == 3:
            return datetime.now().year - int(date_split[2])
        else:
            return "Не указан"

    
    def profile(self, user_id):
        user_info = user_vk.users.get(user_ids = user_id, fields = "bdate, sex, city, relation")[0]
        age = self.age(user_info['bdate'])
        sex = "Женский" if user_info['sex'] == 1 else "Мужской" if user_info['sex'] == 2 else "Не указан"
        city = user_info.get('city', {})
        relation = self.relations.get(user_info.get('relation'), "Не указано")
        self.send(user_id, f"Информация о тебе:\nВозраст: {age}\nПол: {sex}\n\
                            Город: {city.get('title', 0)}\nСП: {relation}", self.keyboard.menu(), [])
        return [user_id, city.get('id', 0), age, user_info['sex'], user_info.get('relation')]


    def search(self, user_id):
        if self.database.count_users():
            
            user = self.database.get_user()
            self.database.set_current_id(user_id, user[0])

            parameters = {
                'owner_id': user[0],
                'album_id': 'profile',
                'extended': 1
            }

            images = sorted(user_vk.photos.get(**parameters)['items'], key=lambda x: x['likes']['count'], reverse=True)[:3]
            
            self.send(user_id, f"{user[1]} ({self.relations.get(user[2], 'СП не указано')})", self.keyboard.search(), images)
            self.database.delete_users(user[0])


        else: # Если не осталось профилей для оценки

            profile = self.database.get_my_profile(user_id)

            parameters = {
                'offset': int(profile[5]),
                'count': 30,
                'fields': 'sex, city, relation',
                'age_from': int(profile[2]) - 5,
                'age_to': int(profile[2]) + 5,
                'sex': 1 if int(profile[3]) == 2 else 1,
                'city': profile[1],
                'has_photo': 1
            }
            all_users = user_vk.users.search(**parameters)

            if int(all_users['count']) > int(profile[5]):

                for i in all_users['items']:
                    if not i['is_closed']:
                        if self.database.check_match(i['id']):
                            if 'relation' in i:
                                self.database.insert_users(i['id'], i['first_name'] + " " + i['last_name'], i['relation'])
                            else:
                                self.database.insert_users(i['id'], i['first_name'] + " " + i['last_name'], -1)
                    
                self.database.add_my_offset(user_id, self.Offset)

            else:
                self.database.set_my_offset(user_id, 0) 
                self.database.delete_match()

            self.search(user_id)