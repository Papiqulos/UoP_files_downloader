import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

url_eclass = "https://eclass.upatras.gr/"  # url του eclass


# General function for interacting with scraped elements
# (can be expanded for other types, currently uses XPATH, NAME and LINK_TEXT)
# Not very efficient(if statements)
def scraped_element_action(driver, TYPE, value_var, action, send_keys_value="", time_to_wait=0.5):
    global scraped_element

    if TYPE == "xpath":
        scraped_element = driver.find_element(by=By.XPATH, value=value_var)
    elif TYPE == "link_text":
        scraped_element = driver.find_element(by=By.LINK_TEXT, value=value_var)
    elif TYPE == "name":
        scraped_element = driver.find_element(by=By.NAME, value=value_var)

    if action == "click":
        scraped_element.click()
    elif action == "sendkeys":
        scraped_element.send_keys(send_keys_value)
    driver.implicitly_wait(time_to_wait)


# Downloads all files from a subject if you have reached the 'Ολα τα μαθήματα page while webscraping
def subject_downloader(driver, subject, time_to_download):
    # Clicking Subject
    scraped_element_action(driver, "link_text", subject, "click")
    driver.implicitly_wait(50)
    print('--Clicked Subject--')

    # Clicking Έγγραφα

    # Μερικές φορές δεν βρίσκει τα Έγγραφα μόνο από το όνομα
    # γι΄αυτο χειρίζομαι το error και μετα βλέπω αν
    # υπάρχει το πεδίο Ασκήσεις για να επιλεχτεί το κατάλληλο xpath
    try:
        # print("try1")
        scraped_element_action(driver, "link_text", "Έγγραφα", "click")
    except NoSuchElementException:
        # print("except1")
        if determine_askhseis(driver) is True:
            scraped_element_action(driver, "xpath", '//*[@id="collapse0"]/a[3]/span[2]', "click")
        else:
            scraped_element_action(driver, "xpath", '//*[@id="collapse0"]/a[2]/span[2]', "click")
    print('--Clicked Έγγραφα--')

    # Clicking Λήψη Όλου του Καταλόγου
    scraped_element_action(driver, "xpath", '//*[@id="main-content"]/div/div/div[3]/div/div/div/div/a[2]/span', "click")
    print('--Clicked Λήψη Όλου του Κατάλογου--')
    print('Downloading. Check Downloads Folder')
    time.sleep(time_to_download)


# Web Scraping(sort of)
def download_all_files_eclass(username, password, time_to_download=5):
    # Making the Browser headless(no open window)
    options = Options()
    options.add_argument("--headless=new")

    # Opening a Chrome tab
    driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()), options=options)
    driver.maximize_window()

    # Going to a specific url
    driver.get(url_eclass)
    driver.implicitly_wait(50)  # Waiting for things to load before scraping them

    # Clicking Είσοδος
    scraped_element_action(driver, "xpath", '//*[@id="main-content"]/div/div/div[2]/div/div/div/div/div/div['
                                            '1]/div[1]/a', "click")
    driver.implicitly_wait(50)
    print('--Clicked Είσοδος--')

    # Typing username
    scraped_element_action(driver, "name", "j_username", "sendkeys", username)
    driver.implicitly_wait(50)
    print('--Typed username--')

    # Typing password
    scraped_element_action(driver, "name", "j_password", "sendkeys", password)
    driver.implicitly_wait(50)
    print('--Typed password--')

    # Clicking Σύνδεση
    scraped_element_action(driver, "xpath", '//*[@id="loginButton"]', "click")
    driver.implicitly_wait(50)
    print('--Clicked Σύνδεση--')

    # Clicking Όλα τα μαθήματα
    scraped_element_action(driver, "xpath", '//*[@id="portfolio_lessons_wrapper"]/div[1]/a', "click")
    driver.implicitly_wait(50)
    print('--Clicked Σύνδεση--')

    # Selecting the Subject
    print('Loading Subjects...')
    subjects = get_list_of_classes(driver)
    print(*(f'{i + 1}.{subjects[i]}' for i in range(len(subjects))), sep='\n')
    subject_number = input('Choose Subject(Number): ')
    if subject_number.lower() == 'x' or subject_number.lower() == 'χ':
        quit()
    print(subjects[int(subject_number) - 1])
    subject_downloader(driver, subjects[int(subject_number) - 1].strip(), time_to_download)

    driver.quit()


# Gets the specific classes of the student
def get_list_of_classes(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    subjects = []
    mathimata_class = soup.find_all('strong')
    print(f'Σύνολο Μαθημάτων: {len(mathimata_class)}')
    for subject in mathimata_class:
        # print(subject.get_text())
        subjects.append(subject.get_text())
    return subjects


# True αν υπάρχει το πεδίο Ασκήσεις , Else όταν δεν υπάρχει
def determine_askhseis(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')  # σούπα
    karteles = soup.find_all('a', {"class": "list-group-item"})
    askhseis_me_skoupidia = re.sub(r"[\n\t\s]*", "", karteles[1].get_text())  # βγάζει όλα τα tabs, whitespaces,
    # newlines
    askhseis_xwris_skoupidia = re.sub(r'[0-9]+', '', askhseis_me_skoupidia)  # βγάζει όλους τους αριθμούς
    if askhseis_xwris_skoupidia == 'Ασκήσεις':
        return True
    else:
        return False


if __name__ == '__main__':
    try:
        print('Eclass File Downloader(Press X or x in any field to exit)')
        username = input('username: ')
        if username.lower() == 'x' or username.lower() == 'χ':
            quit()
        password = input('password: ')
        if password.lower() == 'x' or password.lower() == 'χ':
            quit()
        # username = "upXXXXXX"
        # password = "xxxxxxx"
        download_all_files_eclass(username, password)
        print("Done!")
    except KeyboardInterrupt:
        quit()
