import pyautogui
import keyboard
import time
import openpyxl
import asyncio

from pos_const import *

from datetime import datetime
import pytz


import telegram

# Замените TOKEN на ваш собственный токен бота
TOKEN = '7521024299:AAGChr0npXJP1t6OR6VnqLy2g6Pdjf9KF10'

# Создаем объект бота
bot = telegram.Bot(token=TOKEN)


async def telegram_message():
    # Идентификатор чата (chat_id) получателя
    RECIPIENT_CHAT_ID = '@D2Isaac'
    message_text = 'Нужно поймать редкого мискрита!!!'
    bot.send_message(chat_id=RECIPIENT_CHAT_ID, text=message_text)
    time.sleep(15)


FIGHT_COUNTER = 0 


IS_CLICKING = False

MAIN_POS_CLICK = (956, 510)

start_time = int(time.time())

# count_fight = 0

LVL_UP_CHECK = [False, False, False, False]

def set_clicker():
    global IS_CLICKING
    IS_CLICKING = not IS_CLICKING
    if IS_CLICKING:
        print(f'\033[92mКликер включен')
        global start_time
        start_time = int(time.time())
        return
    print(f'\033[91mКликер выключен')


def get_pos():
    global MAIN_POS_CLICK
    MAIN_POS_CLICK = tuple(pyautogui.position()) 
    print('Изменил позицию на', MAIN_POS_CLICK)

def get_pos_col():
    pos = tuple(pyautogui.position())
    print(pos, '-', pyautogui.pixel(pos[0], pos[1]))

keyboard.add_hotkey('Alt + z', set_clicker)
keyboard.add_hotkey('Alt + x', get_pos)
keyboard.add_hotkey('Alt + a', get_pos_col)



def catch_mis(ability, ability_menu_pos):
    time.sleep(1)
    if pyautogui.pixel(TYPR_MIS_POS[0], TYPR_MIS_POS[1]) == TYPE_MIS_COL['common']:
        asyncio.run(telegram_message())
        for _ in range(ability_menu_pos):         
            pyautogui.click(CHANGE_ABILITY_BUTTON_LEFT_POS)
            time.sleep(0.5)
        flag = 0
        while pyautogui.pixel(CHECK_HP_MIS['pos'][0], CHECK_HP_MIS['pos'][1]) != CHECK_HP_MIS['col']:
            pyautogui.click(ability)
            time.sleep(5)
            flag += 1
            if flag == 25:
                pyautogui.click(1886, 12)
                time.sleep(1)
                pyautogui.doubleClick(1853, 33)
                return
        time.sleep(4)
        pyautogui.click(CATCH_BUTTON_POS)
        time.sleep(10)
        print('Проверяю поймал ли')
        time.sleep(3)
        if pyautogui.pixel(SKIP_BUTTON['pos'][0], SKIP_BUTTON['pos'][1]) == SKIP_BUTTON['col']:
            print('Поймал!')
            pyautogui.click(SKIP_BUTTON['pos'])
            time.sleep(6)
            # if or while
            flag_1 = 0
            while pyautogui.pixel(SKIP_MENU['pos'][0], SKIP_MENU['pos'][1]) == SKIP_MENU['col']:
                pyautogui.click(SKIP_BUTTON_POS)
                if flag_1 == 30:
                    pyautogui.click(1886, 12)
                    time.sleep(1)
                    pyautogui.doubleClick(1853, 33)
                    return
            return True
    print('не поймал')
    return False

def click_ability(ability):
    count = 0
    flag = True
    while flag:
        if pyautogui.pixel(ABILITY_MENU['pos'][0], ABILITY_MENU['pos'][1]) == ABILITY_MENU['col']:
            while pyautogui.pixel(ABILITY_MENU['pos'][0], ABILITY_MENU['pos'][1]) == ABILITY_MENU['col']:
                if count == 55:
                    return
                count += 1
                print('делаю атаку', datetime.now(pytz.timezone('Europe/Moscow')).strftime('%H:%M:%S'))
                pyautogui.click(ability)
                time.sleep(1)
            flag = False
    exel_stats()
    # вот тут не совсем помню зачем
    # time.sleep(1)
    # time.sleep(3)


def check_lvl_up():
    LVL_UP_CHECK[0] = pyautogui.pixel(LVL_UP_MIS_1[0], LVL_UP_MIS_1[1]) == LVL_COLOR_1
    LVL_UP_CHECK[1] = pyautogui.pixel(LVL_UP_MIS_2[0], LVL_UP_MIS_2[1]) == LVL_COLOR_2
    LVL_UP_CHECK[2] = pyautogui.pixel(LVL_UP_MIS_3[0], LVL_UP_MIS_3[1]) == LVL_COLOR_3
    LVL_UP_CHECK[3] = pyautogui.pixel(LVL_UP_MIS_4[0], LVL_UP_MIS_4[1]) == LVL_COLOR_4
    # print('проверяю лвл')
    # print(LVL_UP_CHECK)
    # time.sleep(1.5)   

def close_fight_menu():
    # вот тут надо увеличить, чтобы он сразу делал лвл ап
    # но можно сделать так, чтобы лв происходил после второго боя
    time.sleep(1)
    flag = True
    flag_1 = 0
    while flag:
        flag_1 += 1
        if flag_1 == 250:
            return
        if pyautogui.pixel(CLOSE_MENU['pos'][0], CLOSE_MENU['pos'][1]) == CLOSE_MENU['col']:
            time.sleep(0.1)
            pyautogui.click(CLOSE_FIGHT_BUTTON)
            flag = False
    time.sleep(4)

def do_lvl_up(sleep_time = 3):
    # print('запустил функцию проверку лвла')
    time.sleep(2)
    # print(LVL_UP_CHECK)

    if sum(LVL_UP_CHECK) != 0:
        # print('делаю лвл ап')
        pyautogui.click(LVL_UP_MENU_BUTTON)
        time.sleep(1)
        for i in range(4):
            if LVL_UP_CHECK[i]:
                pyautogui.click(LVL_UP_MENU_MIS[i])
                time.sleep(0.5)
                pyautogui.click(LVL_UP_BUTTON_1)
                time.sleep(1.5)
                pyautogui.click(LVL_UP_BUTTON_2)
                time.sleep(1)
                pyautogui.click(ABILITY_LVL_MENU_CLOSE_BUTTON)
                time.sleep(1)
                pyautogui.click(ABILITY_LVL_MENU_CLOSE_BUTTON_2)
                time.sleep(1)
                pyautogui.click(ABILITY_LVL_MENU_CLOSE_BUTTON_3)
                LVL_UP_CHECK[i] = False
                time.sleep(1)
        pyautogui.click(CLOSE_LVL_UP_BUTTON)
        time.sleep(1)
        return 
    time.sleep(sleep_time)


def fight_action(pos, ability_1, ability_2, ability_menu_pos = 4):
    # do_heal()
    print('иду на позицию', pos)


    pyautogui.click(pos)

    # одну можно убрать если расстояние небольшое
    # time.sleep(5)
    
    # вот тут если мало ставить, то может не найти бой
    # time.sleep(2.5)

    # вот эту часть надо еще протестить
    flag = 0
    while flag < 25:
        if pyautogui.pixel(ABILITY_MENU['pos'][0], ABILITY_MENU['pos'][1]) != ABILITY_MENU['col']:
            time.sleep(0.2)
            flag += 1
            # time.sleep(15)
        else:
            break
    global FIGHT_COUNTER
    if flag == 25:
        print('я не вижу боя')
        FIGHT_COUNTER += 1
        time.sleep(15)
        return
    FIGHT_COUNTER = 0
    # конец

    flag = catch_mis(ability_2, ability_menu_pos)

    if not flag:
        print('начинаю бой')
        click_ability(ability_1)
    else:
        print('не поймал, буду добивать')
    time.sleep(2)
    check_lvl_up()
    close_fight_menu()

    # закрытие окна поимки
    if flag:
        time.sleep(2)
        pyautogui.click(KEEP_BUTTON)
        time.sleep(1)
    do_heal()
    do_lvl_up(sleep_time=0)


def exel_stats():
    global start_time
    workbook = openpyxl.load_workbook('state_25_08.xlsx')
    worksheet = workbook.active
    worksheet['B1'] = int(worksheet['B1'].value) + 1
    worksheet['B2'] = int(worksheet['B2'].value) + 1
    worksheet['L2'] = float(worksheet['L2'].value) + (int(time.time()) - start_time)
    worksheet['L6'] = str(datetime.now(pytz.timezone('Europe/Moscow')))
    start_time = int(time.time())

    workbook.save('state_25_08.xlsx')
    

def do_heal():
    pyautogui.moveTo(121, 73)
    time.sleep(0.2)
    pyautogui.moveTo(121, 72)
    time.sleep(0.5)
    pyautogui.moveTo(121, 72)
    time.sleep(2)
    if pyautogui.pixel(HEAL_CHECK['pos'][0], HEAL_CHECK['pos'][1]) == HEAL_CHECK['col']:
        pyautogui.click(HEAL_BUTTON_POS)
        print('хилюсь')
        time.sleep(1)

def log():
    print('пытаюсь залогинется')
    if pyautogui.pixel(CHECK_LOG_MENU['pos'][0], CHECK_LOG_MENU['col'][1]) == CHECK_LOG_MENU['col']:
        pyautogui.click(OPEN_LOG_MENU_BUTTOM)
        time.sleep(0.7)
    if pyautogui.pixel(LOG_MENU_CHECK['pos'][0], LOG_MENU_CHECK['pos'][1]) == LOG_MENU_CHECK['col']:
        pyautogui.click(EXIT_GAME_POS)
        pyautogui.click(EXIT_GAME_POS)
        time.sleep(3)
        pyautogui.doubleClick(ICON_GAME)
        time.sleep(20)
        while pyautogui.pixel(LOG_MENU_CHECK['pos'][0], LOG_MENU_CHECK['pos'][1]) == LOG_MENU_CHECK['col']:
            pyautogui.click(LOG_MENU_BUTTON)
            time.sleep(0.5)
        time.sleep(20)
        return True
    return False

def go_pos(location):
    global MAIN_POS_CLICK
    if location == 'гора':
        MAIN_POS_CLICK = (956, 510)
        pyautogui.click(283, 123)
        time.sleep(5)
        pyautogui.click(1352, 120)
        time.sleep(5)
        pyautogui.click(332, 134)
        time.sleep(5)
        pyautogui.click(110, 128)
        time.sleep(5)
        pyautogui.click(136, 380)
        time.sleep(5)
        pyautogui.click(115, 164)
        time.sleep(5)
        pyautogui.click(1689, 134)
        time.sleep(5)
        pyautogui.click(1817, 205)
        time.sleep(5)
        pyautogui.click(1865, 617)
        time.sleep(5)
        pyautogui.click(1360, 65)
        time.sleep(5)
        pyautogui.click(1127, 69)
        time.sleep(10)
        # кристал с легендаркой
        # pyautogui.click(511, 155)
        pyautogui.click(479, 245)
        time.sleep(5)
        pyautogui.click(769, 365)
        time.sleep(14)
        # pyautogui.click(734, 498)
    if location == 'дом':
        MAIN_POS_CLICK = (936, 441)
        pyautogui.click(1600, 847)
        time.sleep(14)
    if location == 'пляж':
        MAIN_POS_CLICK = (961, 509)
        pyautogui.click(227, 1000)
        time.sleep(5)
        pyautogui.click(79, 880)
        time.sleep(5)
        pyautogui.click(302, 986)
        time.sleep(5)
        pyautogui.click(147, 792)
        time.sleep(5)
        pyautogui.click(863, 982)
        time.sleep(5)
        pyautogui.click(1831, 797)
        time.sleep(5)
        pyautogui.click(1758, 931)
        time.sleep(5)
        pyautogui.click(1876, 903)
        time.sleep(5)
        pyautogui.click(1823, 968)
        time.sleep(5)
        pyautogui.click(1716, 625)
        time.sleep(5)
        pyautogui.click(1701, 262)
        time.sleep(5)
        pyautogui.click(1264, 590)
        time.sleep(7)
    

while True:
    if IS_CLICKING:
        if log():
            if pyautogui.pixel(DAILY_SPIN_CHECK['pos'][0], DAILY_SPIN_CHECK['pos'][1]) == DAILY_SPIN_CHECK['col']:
                pyautogui.click(DAILY_SPIN_BUTTON)
                time.sleep(10)
                pyautogui.click(IM_DONE)
                time.sleep(5)
                pyautogui.click(DAILY_SPIN_EXIT)
            go_pos('пляж')
        pyautogui.moveTo(MAIN_POS_CLICK)
        time.sleep(1)
        fight_action(MAIN_POS_CLICK, ABILITY_1, ABILITY_4, 1)
        if FIGHT_COUNTER == 5:
            pyautogui.click(EXIT_GAME_POS)
            time.sleep(3)
            pyautogui.doubleClick(ICON_GAME)
            FIGHT_COUNTER = 0
            
        # рубрика ээээксперименты
        # time.sleep(7)

        time.sleep(1.5)
        datetime.now(pytz.timezone('Europe/Moscow')).strftime('%H:%M:%S')


