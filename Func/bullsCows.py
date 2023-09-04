import random
import datetime

def norm_Num(Num):
    if (Num[0] in range(10) and Num[1] in range(10) and Num[2] in range(10) and Num[3] in range(10)):
        return True
    else:
        return False

def gen_Number():
    digits = random.sample("0123456789",4)
    return "".join(digits)

def BullsAndCows(number, gen_number):
    bulls = 0
    cows = 0
    usage = []
    for i in range(4):
        if number[i] == gen_number[i]:
            bulls += 1
    if (bulls == 4):
        return "4 быка и 0 коров!"
    else:
        for i in range(3):
            for j in range(i+1, 4):
                if (number[i] == gen_number[j] and number[i] not in usage):
                    usage.append(number[i])
                    cows += 1
        return f"{bulls} быка и {cows} коров!"

def game_BK_proc(conn_push, conn_pull, conn2_push, players):
    number = gen_Number()
    timeS = datetime.datetime.now()
    N_players = 1
    que_game = 0
    begin_game = False
    while True:
        timeE = datetime.datetime.now()
        if ((timeE - timeS).total_seconds() > 7 and begin_game and N_players > 1):
            que_game = (que_game + 1) % N_players
            timeS = timeE
            conn2_push.send(players[que_game])
        elif (conn_pull.poll()):
            players_mes = conn_pull.recv()
            if (len(players_mes) >= 2 and players_mes[1] == "/remove"):
                break
            elif (len(players_mes) >= 2 and players_mes[1] == "/выйти"):
                if (players_mes[0] == players[que_game]):
                    que_game = (que_game + 1) % N_players
                N_players -= 1
                players.remove(players_mes[0])
                if (N_players == 0):
                    break
            elif (players_mes[0] not in players):
                N_players += 1
                players.append(players_mes[0])
            else:
                if (begin_game == False):
                    timeS = datetime.datetime.now()
                    begin_game = True
                if (players_mes[0] == players[que_game]):
                    if (len(players_mes) >= 2 and len(players_mes[1]) == 4):
                        mes = BullsAndCows(players_mes[1], number)
                        que_game = (que_game + 1) % N_players
                        conn_push.send([mes, players[que_game]])
                        if (mes == "4 быка и 0 коров!"):
                            break
                    else:
                        conn_push.send(["Число введено неккоректно!", players[que_game]])
                else:
                    conn_push.send(["Сейчас ходите не вы!", players[que_game]])
    conn2_push.close()
    conn_push.close()
    conn_pull.close()