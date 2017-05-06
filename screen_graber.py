import time
import openpyxl

from selenium import webdriver

from selenium.webdriver.common.keys import Keys


def get_screen(url, login, password, i=None):
    driver = webdriver.Chrome()
    driver.get(url)
    login_field = driver.find_element_by_id("user_login")
    login_field.send_keys(login)
    pass_field = driver.find_element_by_id("user_pass")
    pass_field.send_keys(password)
    login_button = driver.find_element_by_name("wp-submit")
    login_button.click()
    url = driver.current_url
    edit = 'edit.php' if url[-1] == '/' else '/edit.php'
    edit_url = driver.current_url + edit
    driver.get(edit_url)
    time.sleep(5)
    driver.save_screenshot(f'{i}.png')
    driver.close()


def get_logins(book_path):
    book = openpyxl.load_workbook(book_path)['1']
    cells = book["A:C"]
    creds = [
        {
            "url": cells[0][j].value,
            "login": cells[1][j].value,
            "password": cells[2][j].value
         }
        for j in range(1, len(cells[0]))
    ]
    print(creds)
    i = 2
    for cred in creds:
        try:
            get_screen(cred["url"], cred["login"], cred["password"], i)
        except:
            open(f"{i}.txt", "w+").write("Error here")
        i += 1


get_logins("input.xlsx")
