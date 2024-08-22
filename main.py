import pyautogui
import keyboard
import time
import openpyxl

from pos_const import *





IS_CLICKING = False

MAIN_POS_CLICK = None

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

keyboard.add_hotkey('Alt + z', set_clicker)
keyboard.add_hotkey('Alt + x', get_pos)




def catch_mis(ability, ability_menu_pos):
    time.sleep(1)
    if pyautogui.pixel(TYPR_MIS_POS[0], TYPR_MIS_POS[1]) != TYPE_MIS_COL['common']:
        for _ in range(ability_menu_pos):         
            pyautogui.click(CHANGE_ABILITY_BUTTON_LEFT_POS)
            time.sleep(0.5)
        while  pyautogui.pixel(CHECK_HP_MIS['pos'][0], CHECK_HP_MIS['pos'][1]) != CHECK_HP_MIS['col']:
            pyautogui.click(ability)
            time.sleep(5)
        time.sleep(4)
        pyautogui.click(CATCH_BUTTON_POS)
        time.sleep(10)
        print('Проверяю поймал ли')
        if pyautogui.pixel(SKIP_BUTTON['pos'][0], SKIP_BUTTON['pos'][1]) == SKIP_BUTTON['col']:
            print('Поймал!')
            pyautogui.click(SKIP_BUTTON['pos'])
            time.sleep(6)
            # if or while
            while pyautogui.pixel(SKIP_MENU['pos'][0], SKIP_MENU['pos'][1]) == SKIP_MENU['col']:
                pyautogui.click(SKIP_BUTTON_POS)
            return True
    print('не поймал')
    return False

def click_ability(ability):
    flag = True
    while flag:
        if pyautogui.pixel(ABILITY_MENU['pos'][0], ABILITY_MENU['pos'][1]) == ABILITY_MENU['col']:
            while pyautogui.pixel(ABILITY_MENU['pos'][0], ABILITY_MENU['pos'][1]) == ABILITY_MENU['col']:
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
    while flag:
        if pyautogui.pixel(CLOSE_MENU['pos'][0], CLOSE_MENU['pos'][1]) == CLOSE_MENU['col']:
            time.sleep(0.1)
            pyautogui.click(CLOSE_FIGHT_BUTTON)
            flag = False
    while pyautogui.pixel(CLOSE_MENU['pos'][0], CLOSE_MENU['pos'][1]) == CLOSE_MENU['col']:
        time.sleep(0.1)

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
    if flag == 25:
        print('я не вижу боя')
        time.sleep(7)
        return
    # конец

    flag = catch_mis(ability_2, ability_menu_pos)
    print(flag)
    if not flag:
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
    do_lvl_up(sleep_time=0)


def exel_stats():
    global start_time
    workbook = openpyxl.load_workbook('stats.xlsx')
    worksheet = workbook.active
    worksheet['B1'] = int(worksheet['B1'].value) + 1
    worksheet['B2'] = int(worksheet['B2'].value) + 1
    worksheet['L2'] = float(worksheet['L2'].value) + (int(time.time()) - start_time)
    start_time = int(time.time())

    workbook.save('stats.xlsx')
    


while True:
    if IS_CLICKING:
        # mama
        # pyautogui.click(1054, 529)
        # time.sleep(15)
        # fight_action((845, 443), ABILITY_1, ABILITY_2)


        # pyautogui.moveTo(937, 441)
        # time.sleep(0.7)

        # земля окола дома коллекционера, пока не ловится
        # fight_action((961, 511), ABILITY_1, ABILITY_2)
        # time.sleep(13)
        pyautogui.moveTo(MAIN_POS_CLICK)
        time.sleep(0.3)
        fight_action(MAIN_POS_CLICK, ABILITY_1, ABILITY_4, 1)

        # когда как
        # time.sleep(5)
        time.sleep(10)

        # (845, 443)
        # fight_action(LOC_13_1, ABILITY_1, ABILITY_2)
        # fight_action(LOC_13_2, ABILITY_1, ABILITY_2)



