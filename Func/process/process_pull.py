import random
import vk_api

def process_pull(conn, token_bot):
    vk_session = vk_api.VkApi(token=token_bot)
    vk = vk_session.get_api()
    parent_pull = conn.recv()
    while True:
        if (conn.poll()):
            parent_pull = conn.recv()
        for gaid in parent_pull:
            if (parent_pull[gaid].poll()):
                usid=parent_pull[gaid].recv()
                vk.messages.send(user_id=usid,
                                        message="Ваш ход!",
                                        random_id=random.randint(0, 2 ** 64))