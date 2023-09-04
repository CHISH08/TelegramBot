import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from multiprocessing import Process, Pipe
import time
from transliterate import translit
from Func.api_req import *
from Func.func import *
from Func.bullsCows import *
from Func.process.process_pull import *
from Func.process.process_poll import *
from Func.process.process_weather import *
from Func.process.process_go import *
from Func.process.process_send import *
from Func.process.process_warn import *

token_bot = 'secret'
token_us = 'secret'
poll_id = 816217629

game_BK = {}
game_users_BK = {}
parent_conn_pull = {}
child_conn_push = {}
child_conn_pull = {}
parent_conn_push = {}
processP_pull = {}
processC_push = {}
games_proc = {}
procC_pull, procP_push = Pipe()
proc_pull = Process(target=process_pull, args=(procC_pull, token_bot, ))
proc_pull.start()

class MyVkLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try: 
                for event in self.check():
                    yield event
            except Exception as e:
                print('error', e)
                for k in game_BK:
                    processC_push[k].close()
                    processP_pull[k].close()
                    processC_push.pop(k)
                    processP_pull.pop(k)
                    procP_push.send(processP_pull)
                    parent_conn_push[k].close()
                    parent_conn_pull[k].close()
                    games_proc[k].kill()
                    game_BK.pop(k)
                    game_users_BK.pop(k)
                    parent_conn_pull.pop(k)
                    child_conn_push.pop(k)
                    child_conn_pull.pop(k)
                    parent_conn_push.pop(k)
                    games_proc.pop(k)
                    procP_push.close()
                    proc_pull.kill()
                time.sleep(1)
                procC_pull, procP_push = Pipe()
                proc_pull = Process(target=process_pull, args=(procC_pull, token_bot, ))
                proc_pull.start()
                continue

def proc_chat(event, vk, str):
    try:
        if str[0].lower() == "/опрос":
            process_poll(event,event.obj.message['peer_id'], poll_id, str, token_bot)
        elif str[0].lower() == "/погода":
            process_weather(event, str, "chat", token_bot)
        elif str[0].lower() == "/help":
            mes = "Команды бота в чате:\n\nСоздать опрос: /опрос *флаг* *куда1* *время1* *куда2* *время2* ...\n-u: сгенерировать опрос(по дефолту стоит типичный опрос, если написать куда и время, то генерируется опрос нужного вида)\n-a: добавить all к сообщению(для админов)\n-p: закрепить опрос(для админов, закрепляет сообщение и при запросе /опрос будет показываться именно этот опрос)\nПримеры:\n/опрос\n/опрос -u -p\n/опрос -u -a Каток 21 Настолки 13\nУзнать в городах погоду: /погода город1 город2 ...\nПример:\n/погода Москва Клинцы"
            vk.messages.send(
                            message=mes,
                            random_id = get_random_id(),
                            chat_id = event.chat_id)
    except:
        pass

def proc_user(event, vk, str):
    try:
        if str[0].lower() == "/отправить":
            process_send(event, str, token_bot)
        elif str[0].lower() == "/погода":
            process_weather(event, str, "ls", token_bot)
        elif (str[0].lower() == "/рассылка" and event.obj.message['from_id'] == 218313726):
            users = vk.groups.getMembers(group_id="218260616", fields="bdate")["items"]
            mes = " ".join(str[1:])
            process_warn_r(users, mes, token_bot)
        elif str[0].lower() == "/создать_бк":
            if (len(str) < 3 or not checkNatNum(str[2])):
                vk.messages.send(
                    message="Введите команду с названием игры и кол-вом участников:\n/создать_бк *название* *натуральное число*!",
                    random_id = get_random_id(),
                    user_id=event.obj.message['from_id'])
            else:
                if str[1] in game_BK:
                    vk.messages.send(
                        message="Игра с таким названием уже создана!",
                        random_id = get_random_id(),
                        user_id=event.obj.message['from_id'])
                else:
                    game_BK[str[1]] = [1, int(str[2]), False]
                    game_users_BK[str[1]] = [event.obj.message['from_id']]
                    parent_conn_pull[str[1]], child_conn_push[str[1]] = Pipe()
                    child_conn_pull[str[1]], parent_conn_push[str[1]] = Pipe()
                    processP_pull[str[1]], processC_push[str[1]] = Pipe()
                    procP_push.send(processP_pull)
                    games_proc[str[1]] = Process(target=game_BK_proc, args=(child_conn_push[str[1]], child_conn_pull[str[1]], processC_push[str[1]], [event.obj.message['from_id']], ))
                    games_proc[str[1]].start()
                    vk.messages.send(
                        message=f"Игра с названием {str[1]} успешно создана!",
                        random_id = get_random_id(),
                        user_id=event.obj.message['from_id'])
                    if (str[2] == "1"):
                        vk.messages.send(
                            message="Игра началась",
                            random_id = get_random_id(),
                            user_id=event.obj.message['from_id'])
                        vk.messages.send(
                            message="Ваш ход!",
                            random_id = get_random_id(),
                            user_id=event.obj.message['from_id'])
        elif str[0].lower() == "/поиск_бк":
            search_flag = 0
            name_game = ""
            if (len(str) >= 2):
                if ((str[1] in game_BK) and game_BK[str[1]][0] < game_BK[str[1]][1]):
                    search_flag = 1
                    name_game = str[1]
                    game_BK[str[1]][0] += 1
                    game_users_BK[str[1]].append(event.obj.message['from_id'])
                    parent_conn_push[str[1]].send([event.obj.message['from_id']])
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                            message="Игра с таким названием не создана, либо комната заполнена.\nНапишите /поиск_бк без слов справа, чтобы присоединиться к любой существующей игре или создайте новую игру с помощью команды: /создать_бк *название игры без пробелов*",
                            random_id=random.randint(0, 2 ** 64))
            else:
                for k in game_BK:
                    if (game_BK[k][0] < game_BK[k][1]):
                        game_BK[k][0] += 1
                        game_users_BK[k].append(event.obj.message['from_id'])
                        search_flag = 1
                        name_game = k
                        parent_conn_push[k].send([event.obj.message['from_id']])
                        break
                if (search_flag == 0):
                    vk.messages.send(user_id=event.obj.message['from_id'],
                            message="На даннный момент свободных игр нет, создайте новую игру с помощью команды: /создать_бк *название игры без пробелов*",
                            random_id=random.randint(0, 2 ** 64))
            if (search_flag == 1):
                vk.messages.send(user_id=event.obj.message['from_id'],
                            message=f"Вы успешно присоединились к игре с названием {name_game}!",
                            random_id=random.randint(0, 2 ** 64))
                if game_BK[k][0] == game_BK[k][1]:
                    proc_warn_cr = Process(target=process_warn, args=(game_users_BK[k], "Игра началась", token_bot, 1, ))
                    proc_warn_cr.start()
                else:
                    proc_warn_cr = Process(target=process_warn_s, args=(game_users_BK[k], game_BK[k], token_bot, ))
                    proc_warn_cr.start()
        elif (event.obj.message['text'] == "/выйти"):
            for k in game_users_BK:
                if event.obj.message['from_id'] in game_users_BK[k]:
                    parent_conn_push[k].send([event.obj.message['from_id'], event.obj.message['text']])
                    game_BK[k][0] -= 1
                    game_users_BK[k].remove(event.obj.message['from_id'])
                    if (game_BK[k][0] <= 0):
                        processC_push[k].close()
                        processP_pull[k].close()
                        processC_push.pop(k)
                        processP_pull.pop(k)
                        procP_push.send(processP_pull)
                        parent_conn_push[k].close()
                        parent_conn_pull[k].close()
                        games_proc[k].kill()
                        game_BK.pop(k)
                        game_users_BK.pop(k)
                        parent_conn_pull.pop(k)
                        child_conn_push.pop(k)
                        child_conn_pull.pop(k)
                        parent_conn_push.pop(k)
                        games_proc.pop(k)
                    vk.messages.send(user_id=event.obj.message['from_id'],
                        message="Вы вышли из комнаты ожидания!",
                        random_id=random.randint(0, 2 ** 64))
                    break
        elif str[0].lower() == "/help":
            mes = "Команды бота в лс:\n\nОтправить сообщение анонимно другому пользователю: /отправить *ссылка на пользователя*\nПримеры:\n/отправить https://vk.com/durov привет дуров\n/отправить @durov привет дуров\n/отправить durov привет дуров\nУзнать в городах погоду: /погода город1 город2 ...\nПример:\n/погода Москва Клинцы\n\nОписание игры Быки и коровы:\n/бк"
            vk.messages.send(user_id=event.obj.message['from_id'],
                            message=mes,
                            random_id=random.randint(0, 2 ** 64))
        elif str[0].lower() == "/бк":
            mes = "Создать игру:\n/создать_бк *название игры* *кол-во участников*\n\nПрисоединиться к игре(Необязательный параметр - название игры):\n/поиск_бк *название*\n\nВыйти из игры:\n/выйти\n\nПри входе в игру вам нужно писать четырехзначное число.\n\nСуть игры:\nВы вводите четырехзначное число, кол-во совпадений цифр по индексу - кол-во быков, кол-во коров - кол-во нахождений цифр в загаданном числе. Побеждает тот, кто отгадает загаданное число!"
            vk.messages.send(user_id=event.obj.message['from_id'],
                            message=mes,
                            random_id=random.randint(0, 2 ** 64))
        elif (str[0].lower() == "/end" and event.obj.message['from_id'] == 218313726):
            return 0
        else:
            gamer_flag = 0
            for k in game_users_BK:
                if event.obj.message['from_id'] in game_users_BK[k]:
                    gamer_flag = 1
                    if (game_BK[k][0] != game_BK[k][1] and not game_BK[k][2]):
                        vk.messages.send(user_id=event.obj.message['from_id'],
                            message=f"В игре пока {game_BK[k][0]} из {game_BK[k][1]} игроков! Ожидайте или введите команду /выйти, чтобы выйти из комнаты ожидания",
                            random_id=random.randint(0, 2 ** 64))
                    else:
                        game_BK[k][2] = True
                        parent_conn_push[k].send([event.obj.message['from_id'], event.obj.message['text']])
                        game_mes = parent_conn_pull[k].recv()
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                message=game_mes[0],
                                random_id=random.randint(0, 2 ** 64))
                        if (game_mes[0][2:6] == "быка"):
                            vk.messages.send(user_id=game_mes[1],
                                    message="Ваш ход!",
                                    random_id=random.randint(0, 2 ** 64))
                        if (game_mes[0] == "4 быка и 0 коров!"):
                            parent_conn_push[k].close()
                            parent_conn_pull[k].close()
                            games_proc[k].join()
                            game_BK.pop(k)
                            proc_warn_cr = Process(target=process_warn_win, args=(game_users_BK[k], event.obj.message['from_id'], token_bot, ))
                            proc_warn_cr.start()
                            processC_push[k].close()
                            processP_pull[k].close()
                            processC_push.pop(k)
                            processP_pull.pop(k)
                            procP_push.send(processP_pull)
                            game_users_BK.pop(k)
                            parent_conn_pull.pop(k)
                            child_conn_push.pop(k)
                            child_conn_pull.pop(k)
                            parent_conn_push.pop(k)
                            games_proc.pop(k)
                    break
            if (gamer_flag == 0):
                vk.messages.send(user_id=event.obj.message['from_id'],
                                message="Хорошо",
                                random_id=random.randint(0, 2 ** 64))
    except IndexError:
        vk.messages.send(user_id=event.obj.message['from_id'],
                                message="Пока я только умею читать...(",
                                random_id=random.randint(0, 2 ** 64))

def main():
    vk_session = vk_api.VkApi(token=token_bot)
    vk = vk_session.get_api()
    LongPoll = MyVkLongPoll(vk_session, '218260616')
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button("Начать", VkKeyboardColor.SECONDARY)
    for event in LongPoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            str = event.obj.message['text'].split()
            if event.from_chat:
                proc_chat_Poll = Process(target=proc_chat, args=(event, vk, str, ))
                proc_chat_Poll.start()
            elif event.from_user:
                proc_user_Poll = Process(target=proc_user(event, vk, str, ))
                proc_user_Poll.start()

if __name__ == '__main__':
    main()