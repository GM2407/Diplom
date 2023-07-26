from vk_api.bot_longpoll import VkBotEventType
import Classes
from Classes import longpoll, vk

SQL = Classes.SQL()
Keyboard = Classes.Keyboards()
Main = Classes.MainFuncs()

SQL.init_database()

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:

        answer = vk.users.get(my_ids=event.obj.message['from_id'])

        my_id = event.obj.message['peer_id']

        msg = event.obj.message['text']

        if SQL.check_my_profile(my_id):
            if msg == "Обновить профиль":
                try:
                    Data = Main.profile(my_id)
                    SQL.update_my_profile(Data[0], Data[1], Data[2], Data[3], Data[4])
                    Main.send(my_id, "Параметры твоего профиля сохранены и обновлены.\
                    \nЕсли параметры не актуальные, то обнови свой профиль ВКонтакте.", Keyboard.menu(), [])
                except:
                    Main.send(my_id, "Не удалось обновить твой профиль.\nПопробуй чуть позже", Keyboard.menu(), [])

            elif msg == "Поиск" or msg == "Продолжить":
                Main.search(my_id)

            elif msg == "👍":
                CurrentID = SQL.get_current_id(my_id)[0]
                Main.send(my_id, f"Ссылка на профиль: https://vk.com/id{CurrentID}\nИщем дальше?", Keyboard.search_next(), [])
                SQL.insert_match(CurrentID, 1)

            elif msg == "👎":
                SQL.insert_match(CurrentID, 0)
                Main.search(my_id)

            elif msg == "Меню":
                Main.send(my_id, "Ты вернулся в меню", Keyboard.menu(), [])

            else:
                Main.send(my_id, "Неизвестная команда", Keyboard.menu(), [])

        else:

            if msg == "Создать профиль":
                try:
                    Data = Main.profile(my_id)
                    SQL.insert_my_profile(Data[0], Data[1], Data[2], Data[3], Data[4])
                    Main.send(my_id, "Параметры твоего профиля сохранены", Keyboard.menu(), [])
                except:
                    Main.send(my_id, "Не удалось сохранить твой профиль.\nПопробуй чуть позже", Keyboard.create(), [])


            else:
                Main.send(my_id, "Мне нужно получить твои данные, чтобы начать подбирать подходящие пары", Keyboard.create(), [])