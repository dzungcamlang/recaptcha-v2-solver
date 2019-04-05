from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from RecaptchaTest import *
from SeparateImage import *
from ImageLabeling import *

class ControlRecaptchaIframe:

    def __init__(self, web_driver):
        self.web_driver = web_driver
        self.recaptcha_iframe = None
        self.number_of_tiles = 0
        self.number_of_rows = 0
        self.number_of_columns = 0
        self.verify_button = None

    def find_recaptcha_iframe(self):
        # Wait until recaptcha iframe opens
        wait = WebDriverWait(self.web_driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='recaptcha challenge']")))
        # Find recpatcha iframe
        try:
            self.recaptcha_iframe = self.web_driver.find_element_by_css_selector("iframe[title='recaptcha challenge']")
            self.web_driver.switch_to.frame(self.recaptcha_iframe)
            return True
        except:
            return False

    # def find_skip_button(self):
    #     pass
    #
    # def find_next_button(self):
    #     pass

    def get_image_selection_tiles(self):
        self.number_of_tiles = (self.web_driver.find_elements_by_css_selector("td[class='rc-imageselect-tile']"))
        self.number_of_rows = len(self.web_driver.find_elements_by_css_selector("#rc-imageselect-target tr"))
        self.number_of_columns = int(len(self.web_driver.find_elements_by_css_selector("td[class='rc-imageselect-tile']")) / rows)

    def start(self):
        if not self.find_recaptcha_iframe():
            print("Could not find reCAPTCHA image selection menu after clicking 'I'm not a robot' button")
            return
        # self.find_skip_button()
        # self.find_next_button()
        self.get_image_selection_tiles()
        separate_image = SeparateImage()
        image_labeling = ImageLabeling()
        complete = False
        while not complete:
            new_test = RecaptchaTest(self.web_driver, self.number_of_tiles, self.number_of_rows, self.number_of_columns, separate_image, image_labeling)
            complete = new_test.start_test()
            self.verify_button.click()
        self.web_driver.switch_to.default_content()

