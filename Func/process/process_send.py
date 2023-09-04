from ..func import *
import vk_api
from ..api_req import *
import random

def process_send(event, str, token_bot):
    vk_session = vk_api.VkApi(token=token_bot)
    vk = vk_session.get_api()
    try:
        id = str_to_id(str[1])
        user = vk.users.get(user_ids=id)
        vk.messages.send(user_id=user[0]["id"],
                        message="Анонимный пользователь отправил вам сообщение:\n" + " ".join(str[2:]),
                        random_id=random.randint(0, 2 ** 64))
        vk.messages.send(user_id=event.obj.message['from_id'],
                    message="Отправлено",
                    random_id=random.randint(0, 2 ** 64))
    except:
        vk.messages.send(user_id=event.obj.message['from_id'],
                        message="Такого пользователя нет в сообществе, либо он отключил сообщения для группы...(",
                        random_id=random.randint(0, 2 ** 64))