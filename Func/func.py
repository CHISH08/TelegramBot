import json
import vk_api

token_us = 'secret'

def checkNatNum(n):
    if str(n).isdigit() and float(n) == int(n) and int(n) > 0:
        return True
    else:
        return False


def get_poll_mes(str, is_admin, poll_id):
    poll_id1 = poll_id
    mes = ""
    if ("-a" in str and is_admin):
        mes = "@all"
    if ("-u" in str):
        token = token_us
        vk_session1 = vk_api.VkApi(token=token)
        vk1 = vk_session1.get_api()
        mas_answer = []
        poll_ques = ""
        flag = 0
        index = 2
        while(index < len(str)):
            if (str[index][0] == "-"):
                index += 1
                continue
            flag = 1
            poll_ques = poll_ques + str[index] + " в " + str[index + 1] + " | "
            mas_answer.append(str[index] + " +")
            mas_answer.append(str[index] + " +-")
            mas_answer.append(str[index] + " -")
            index += 2
        if (flag == 0):
            poll_ques = 'Гулять в 21 | Настолки в 21 | '
            mas_answer = ['Гулять +', 'Гулять +-', 'Гулять -', 'Настолки +', 'Настолки +-', 'Настолки -']
        poll_ques = poll_ques[:-3]
        poll_id1 = vk1.polls.create(is_multiple=1, question=poll_ques,
                                    add_answers=json.dumps(mas_answer))['id']
    pid = f'{poll_id1}'
    poll_send = 'poll218313726_' + pid
    return poll_send, mes, poll_id1

def str_to_id(str):
    id = str.removeprefix('https://vk.com/')
    mas = id.split("|@")
    mas = mas[-1].split("]")
    id = mas[0]
    return id