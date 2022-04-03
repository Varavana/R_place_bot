from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyshadow.main import Shadow
from PIL import Image
from multiprocessing import Process
import time

# defining variables for the session
img = 'ab2btarget.png'
live_writting = True

PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
starting_pos = [0, 644]


def login_to_reddit(driver, user, user_pass):

    username = driver.find_element_by_id('loginUsername')
    username.send_keys(user)

    password = driver.find_element_by_id('loginPassword')
    password.send_keys(user_pass)
    password.submit()


def find_and_click(driver, shadow, submit, color):

    try:
        driver.find_element_by_class_name("moeaZEzC0AbAvmDwN22Ma").click()

    except:
        print('Got an error, reloading page')
        return 'error'
    driver.implicitly_wait(3)

    try:
        driver.switch_to.frame(
            driver.find_element_by_class_name("Q-OBKuePQXXm3LGhGfv3k"))

    except:
        print('Got an error, reloading page')
        return 'error'
    time.sleep(1)

    try:
        shadow.find_element("mona-lisa-status-pill").click()

    except:
        print('Got an error, reloading page')
        return 'error'
    time.sleep(1)

    try:
        shadow.find_element(f".color-container:nth-child({color})").click()

    except:
        print('Got an error, reloading page')
        return 'error'

    time.sleep(1)
    if submit:
        shadow.find_element(".confirm").click()


def make_color_coords(image_path):
    img = Image.open(image_path)
    width, height = img.size
    rgb_img = img.convert('RGB')
    colors_coords = {}

    for h in range(height):
        for w in range(width):

            rgb = rgb_img.getpixel((w, h))

            if rgb == (255, 214, 53):
                colors_coords[(w, h)] = '4'

            elif rgb == (0, 0, 0):
                colors_coords[(w, h)] = '21'

    return colors_coords


def get_screenshot_color(img_path):
    img = Image.open(img_path)
    width, height = img.size
    rgb_img = img.convert('RGB')

    rgb = rgb_img.getpixel(((width/2), (height/2+80)))

    if rgb == (255, 214, 53):
        return '4'

    elif rgb == (0, 0, 0):
        return '21'


def bot(user, user_pass):

    # setting new_chrome_tab
    driver = webdriver.Chrome(PATH)
    driver.get(
        'https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2Fr%2Fplace%2F')
    shadow = Shadow(driver)

    login_to_reddit(driver, user, user_pass)

    WebDriverWait(driver, 10).until(EC.title_contains("place"))

    colors = make_color_coords('a2b2target.png')

    driver.get('https://www.reddit.com/r/place/?cx=0&cy=0&px=10')

    log = open('log.txt', 'a')

    while True:
        for x, y in colors:
            pos_x = starting_pos[0] + int(x)
            pos_y = starting_pos[1] + int(y)
            url = f'https://www.reddit.com/r/place/?cx={pos_x}&cy={pos_y}&px=10'

            driver.get(url)
            WebDriverWait(driver, 10).until(EC.title_contains("place"))
            time.sleep(8)
            driver.save_screenshot(f'screenshot{user}.png')

            correct_color = colors[(x, y)]
            current_color = get_screenshot_color(f'screenshot{user}.png')

            if current_color != correct_color:
                print(
                    f'{user}: I found {current_color} at ({pos_x},{pos_y}), expected {correct_color}. Correcting...', flush=True)
                log.write(
                    f'{user}: I found {current_color} at ({pos_x},{pos_y}), expected {correct_color}. Correcting...\n')
                log.flush()

                response = find_and_click(
                    driver, shadow, live_writting, correct_color)

                if response == 'error':
                    continue

                time.sleep(300)

            elif current_color == correct_color:
                print(
                    f'{user}: I found {current_color} at ({pos_x},{pos_y}), expected {correct_color}', flush=True)
                log.write(
                    f'{user}: I found {current_color} at ({pos_x},{pos_y}), expected {correct_color}\n')
                log.flush()

    log.close()


if __name__ == '__main__':

    delay = 30

    user_1 = Process(target=bot, args=[
                     list(users.keys())[0], users[list(users.keys())[0]]])
    user_1.start()
    time.sleep(delay)
    user_2 = Process(target=bot, args=[
                     list(users.keys())[1], users[list(users.keys())[1]]])
    user_2.start()
    time.sleep(delay)
    user_3 = Process(target=bot, args=[
                     list(users.keys())[2], users[list(users.keys())[2]]])
    user_3.start()
    time.sleep(delay)
    user_4 = Process(target=bot, args=[
                     list(users.keys())[3], users[list(users.keys())[3]]])
    user_4.start()
    time.sleep(delay)

    user_1.join()
    user_2.join()
    user_3.join()
    user_4.join()
