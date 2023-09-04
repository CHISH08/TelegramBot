import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from multiprocessing import Process, Pipe
import time

token_us = 'secret'

vk_session = vk_api.VkApi(token=token_us)
vk = vk_session.get_api()

poll_id = vk.polls.getById(poll_id="830954760")
for i in poll_id['answers']:
    if "+" in i["text"]:
        print(vk.polls.getVoters(poll_id="830954760", answer_ids=i["id"])[0]["users"]["items"])