import time
import customtkinter as ctk
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

url_eclass = "https://eclass.upatras.gr/"  # url του eclass

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


# Μπούρδα
def sleep():
    time.sleep(0.5)


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

    # Clicking Dropdown Menu
    scraped_element_action(driver, "xpath", '//*[@id="header"]/button/span[1]', "click")

    # Clicking Έγγραφα
    scraped_element_action(driver, "link_text", 'Έγγραφα', "click", time_to_wait=1)

    # Clicking Λήψη Όλου του Καταλόγου
    scraped_element_action(driver, "xpath", '//*[@id="main-content"]/div/div/div[3]/div/div/div/div/a[2]/span', "click")

    time.sleep(time_to_download)


# Main GUI
class EclassAllFileDownloader(ctk.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.iconbitmap("images\logo.ico")
        self.title("Upatras Eclass All File Downloader")
        self.geometry(f"{EclassAllFileDownloader.WIDTH}x{EclassAllFileDownloader.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.myFrame = ctk.CTkFrame(master=self, width=780, height=520)
        self.myFrame.grid(row=0, column=0, sticky="ew", padx=30, pady=100)

        self.subjectLabel = ctk.CTkLabel(master=self.myFrame, text='Subject')

        self.subjectInput = ctk.CTkEntry(master=self.myFrame, width=200)

        self.subjectNotice = ctk.CTkLabel(master=self.myFrame,
                                          text='!!Το μάθημα πρέπει να γράφτει έτσι όπως είναι στο eclass!!')

        self.usernameLabel = ctk.CTkLabel(master=self.myFrame, text='Username')

        self.usernameInput = ctk.CTkEntry(master=self.myFrame, text_font=('calibre', 10), width=200)

        self.passwordLabel = ctk.CTkLabel(master=self.myFrame, text='Password', )

        self.passwordInput = ctk.CTkEntry(master=self.myFrame, text_font=('calibre', 10), width=200, show='*')

        self.checkButton = ctk.CTkSwitch(master=self.myFrame, text="Show password", command=self.toggle)

        self.myButton = ctk.CTkButton(master=self.myFrame, text="Initialize Process",
                                      command=
                                      lambda: self.download_all_files_eclass(self.subjectInput.get().strip(),
                                                                             self.usernameInput.get().replace(" ", ""),
                                                                             self.passwordInput.get().replace(" ", "")))

        self.label_mode = ctk.CTkLabel(master=self.myFrame, text="Appearance Mode:")

        self.optionmenu_1 = ctk.CTkOptionMenu(master=self.myFrame,
                                              values=["Dark", "Light", "System"],
                                              command=self.change_appearance_mode)

        # Binding Enter to initialize process when focused on subject, username, password or the window
        # NOT FUNCTIONAL gia kapoio gamhmeno logo

        # self.subjectInput.bind("<Return>", lambda event,
        #                                           subject=self.subjectInput.get(), username=self.usernameInput.get(),
        #                                           password=self.passwordInput.get():
        # self.download_all_files_eclass(subject, username, password))
        #
        # self.usernameInput.bind("<Return>", lambda event,
        #                                            subject=self.subjectInput.get(), username=self.usernameInput.get(),
        #                                            password=self.passwordInput.get():
        # self.download_all_files_eclass(subject, username, password))
        #
        # self.passwordInput.bind("<Return>", lambda event,
        #                                            subject=self.subjectInput.get(), username=self.usernameInput.get(),
        #                                            password=self.passwordInput.get():
        # self.download_all_files_eclass(subject, username, password))
        #
        # self.bind("<Return>", lambda event,
        #                              subject=self.subjectInput.get(), username=self.usernameInput.get(),
        #                              password=self.passwordInput.get():
        #
        # self.download_all_files_eclass(subject, username, password))

        self.var = 0  # Βοηθητική παράμετρος για την toggle()

        # Putting stuff on window
        self.subjectLabel.grid(row=1, column=0)
        self.subjectInput.grid(row=1, column=1)
        self.subjectNotice.grid(row=1, column=2)

        self.usernameLabel.grid(row=3, column=0)
        self.usernameInput.grid(row=3, column=1)

        self.passwordLabel.grid(row=5, column=0)
        self.passwordInput.grid(row=5, column=1)

        self.checkButton.grid(row=5, column=2)

        self.myButton.grid(row=7, column=1)

        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1.grid(row=11, column=0, pady=10, padx=20, sticky="w")

    # Show password or hide password with autistic method
    def toggle(self):
        self.var += 1
        print(self.var)
        if self.var % 2:
            self.passwordInput.configure(show="")
        else:
            self.passwordInput.configure(show="*")

    # Change theme
    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    # Necessary function so that the program exits properly when pressing X
    def on_closing(self, event=0):
        self.destroy()

    # Web Scraping
    def download_all_files_eclass(self, subject, username, password, time_to_download=30):

        # Opening a Chrome tab
        driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))

        # Going to a specific url
        driver.get(url_eclass)
        driver.implicitly_wait(0.5)  # Waiting for things to load before scraping them

        # Clicking Είσοδος
        scraped_element_action(driver, "xpath", '//*[@id="main-content"]/div/div/div[2]/div/div/div/div/div/div['
                                                '1]/div[1]/a', "click")

        # Typing username
        scraped_element_action(driver, "name", "j_username", "sendkeys", username)

        # Typing password
        scraped_element_action(driver, "name", "j_password", "sendkeys", password)

        # Clicking Σύνδεση
        scraped_element_action(driver, "xpath", '//*[@id="loginButton"]', "click")

        # Clicking Όλα τα μαθήματα
        scraped_element_action(driver, "xpath", '//*[@id="portfolio_lessons_wrapper"]/div[1]/a', "click")

        # Handling the case where the student hasn't signed up for the class, UNSUCCESSFULLY for the time being

        try:
            subject_downloader(driver, subject, time_to_download)

        except selenium.common.exceptions.NoSuchElementException:       # Very common exception needs something else

            # Clicking Εγγραφη σε μάθημα
            scraped_element_action(driver, "link_text", "Εγγραφή σε μάθημα", "click")

            # Clicking Προπτυχιακό
            scraped_element_action(driver, "link_text", "Προπτυχιακό", "click")

            # Clicking checkbox για εγγραφή
            # Help

            # Clicking Επιστροφή
            scraped_element_action(driver, "link_text", "Επιστροφή", "click")

            # Clicking Όλα τα μαθήματα
            scraped_element_action(driver, "xpath", '//*[@id="portfolio_lessons_wrapper"]/div[1]/a', "click")

            # Downloading the files as usual
            subject_downloader(driver, subject, time_to_download)

        driver.quit()


if __name__ == '__main__':
    obj = EclassAllFileDownloader()
    obj.mainloop()
