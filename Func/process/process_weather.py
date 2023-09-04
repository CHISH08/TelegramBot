from ..func import *
import vk_api
from ..api_req import *
from transliterate import translit
from vk_api.utils import get_random_id

def process_weather(event, str, flag, token_bot):
    vk_session = vk_api.VkApi(token=token_bot)
    vk = vk_session.get_api()
    city_counter = len(str)
    if (city_counter > 1):
        for j in range(1, city_counter):
            city2 = translit(str[j], language_code='ru', reversed=True)
            if (flag == "chat"):
                try:
                    rs = apiWeather_find(city2)[0]
                    vk.messages.send(chat_id = event.chat_id,
                                    message=f"{str[j]}:\n\nТемпература: {round(rs['main']['temp'] - 273.15)} ℃\nОщущается как: {round(rs['main']['feels_like'] - 273.15)} ℃\nСкорость ветра: {round(rs['wind']['speed'],1)} м/c",
                                    random_id=get_random_id())
                except:
                    vk.messages.send(
                        message=f"{str[j]}:\n\nТакого города не существует!",
                        random_id = get_random_id(),
                        chat_id = event.chat_id)
            else:
                try:
                    rs = apiWeather_find(city2)[0]
                    vk.messages.send(user_id = event.obj.message['from_id'],
                                    message=f"{str[j]}:\n\nТемпература: {round(rs['main']['temp'] - 273.15)} ℃\nОщущается как: {round(rs['main']['feels_like'] - 273.15)} ℃\nСкорость ветра: {round(rs['wind']['speed'],1)} м/c",
                                    random_id=get_random_id())
                except:
                    vk.messages.send(
                        message=f"{str[j]}:\n\nТакого города не существует!",
                        random_id = get_random_id(),
                        user_id = event.obj.message['from_id'])