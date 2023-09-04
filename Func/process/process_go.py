import vk_api
import random

def process_go(event, token_bot, poll_id):
    vk_session = vk_api.VkApi(token=token_bot)
    vk = vk_session.get_api()
    poll_id = vk.polls.getById(poll_id=poll_id)
    for i in poll_id['answers']:
        if "+" in i["text"]:
            users = vk.polls.getVoters(poll_id=poll_id, answer_ids=i["id"])[0]["users"]["items"]
    vk.messages.send(chat_id = event.chat_id,
                                    message=f"{str[j]}:\n\nТемпература: {round(rs['main']['temp'] - 273.15)} ℃\nОщущается как: {round(rs['main']['feels_like'] - 273.15)} ℃\nСкорость ветра: {round(rs['wind']['speed'],1)} м/c",
                                    random_id=get_random_id())