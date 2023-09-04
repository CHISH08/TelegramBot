import vk_api
import random

def process_warn(game_users_BK, mes, token_bot, flag):
    vk_session = vk_api.VkApi(token=token_bot)
    vk = vk_session.get_api()
    for user_game_i in game_users_BK:
        vk.messages.send(user_id=user_game_i,
            message=mes,
            random_id=random.randint(0, 2 ** 64))
    if (flag):
        vk.messages.send(user_id=game_users_BK[0],
                            message="Ваш ход!",
                            random_id=random.randint(0, 2 ** 64))

def process_warn_s(game_users_BK, game_BK, token_bot, flag):
    vk_session = vk_api.VkApi(token=token_bot)
    vk = vk_session.get_api()
    for user_game_i in game_users_BK:
        vk.messages.send(user_id=user_game_i,
            message=f"В игре пока {game_BK[0]} из {game_BK[1]} игроков! Ожидайте или введите команду /выйти, чтобы выйти из комнаты ожидания",
            random_id=random.randint(0, 2 ** 64))

def process_warn_win(game_users_BK, winer, token_bot):
    vk_session = vk_api.VkApi(token=token_bot)
    vk = vk_session.get_api()
    for play_i in game_users_BK:
        if (winer == play_i):
            vk.messages.send(user_id=play_i,
                            message="Игра завершена... Вы победитель!)",
                            random_id=random.randint(0, 2 ** 64))
        else:
            vk.messages.send(user_id=play_i,
                message="Игра завершена!",
                random_id=random.randint(0, 2 ** 64))

def process_warn_r(users, mes, token_bot):
    vk_session = vk_api.VkApi(token=token_bot)
    vk = vk_session.get_api()
    for us in users:
        vk.messages.send(user_id=us["id"],
            message=us["last_name"] + " " + us["first_name"] + ", " + mes,
            random_id=random.randint(0, 2 ** 64))