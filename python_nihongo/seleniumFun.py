# C:/Program Files (x86)/chromedriver.exe
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# what our program should do:
# go to kanshudo/favorites
# while favorites > 0:
#   save the kanji, hiragana, first english meaning []
#   unclick the star and move down the list
# go to google sheets
# for kanji, hiragana, english in []:
#   if row not already populated:
#       populate first, second, third column with kanji, hiragana, meaning

class vocab_word:
    def __init__(self, kanji, hiragana, meaning):
        self.kanji = kanji
        self.hiragana = hiragana
        self.meaning = meaning
    
    def get_kanji(self):
        return self.kanji
    
    def get_hiragana(self):
        return self.hiragana
    
    def get_meaning(self):
        return self.meaning

class kanshudo_scraper:
    def __init__ (self, PATH, driver):
        self.PATH = PATH
        self.driver = driver

    def log_into_website(self):
        if driver.find_element_by_link_text("LOG IN"):
            driver.find_element_by_link_text("LOG IN").click()

            time.sleep(1)

            email_form = driver.find_element_by_name("user[email]")
            password_form = driver.find_element_by_name("user[password]")
            login_button = driver.find_element_by_name("commit")

            # to make this program for other people just make a ui that inputs email and password and saves it
            email_form.send_keys("jason.bondarchuk@stonybrook.edu")
            password_form.send_keys("darthvader11")
            login_button.click()

        else:
            print("something happened")
            driver.quit()

        time.sleep(1)

    def remove_advertisement(self):
        # click the ad to allow for page access
        advertisement = driver.find_element_by_id("ms_subhead")
        if advertisement:
            driver.find_element_by_id("ms_hide").click()

    def scrape_vocabulary(self):
        vocabularyList = driver.find_elements_by_class_name("jr_inner")

        count = 0
        words_for_excel = [] # DATA TO BE INSERTED WITH THE SHEETS API CALL, RETURN REQUIRED
        for item in vocabularyList:
            count += 1
            kanji_and_hiragana = ''.join(item.find_element_by_tag_name('a').text.split('\n'))
            
            # grab kanji
            kanji = kanji_and_hiragana
            furigana_to_remove = item.find_elements_by_class_name('furigana')
            for furigana in furigana_to_remove:
                if furigana.text in kanji:
                    kanji = kanji.replace(furigana.text, '')
            
            # grab hiragana
            hiragana = kanji_and_hiragana
            kanji_to_remove = item.find_elements_by_class_name("f_kanji")
            for bad_kanji in kanji_to_remove:
                if bad_kanji.text in hiragana:
                    hiragana = hiragana.replace(bad_kanji.text, '')

            # grab meaning
            meaning = item.find_element_by_class_name("vm").text.split("\n")[1:]
            meaning = ''.join(meaning).replace('1.', '')
            
            # save kanji, hiragana, meaning into a list of vocab_word objects
            word_object = vocab_word(kanji, hiragana, meaning)
            words_for_excel.append(word_object)
            print(f"got vocab {count}")
            print(f"vocab {count}: {word_object.get_kanji()}, {word_object.get_hiragana()}, {word_object.get_meaning()}")
            time.sleep(0.3)
            favorite_button = item.find_element_by_class_name("fav").find_element_by_tag_name("div")
            favorite_button.click()

        time.sleep(0.5)
        return words_for_excel

    def close_driver(self):
        driver.quit()

# scrape kanshudo, global variables***
PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.kanshudo.com/favorites")

kanshudoScraper = kanshudo_scraper(PATH, driver)
kanshudoScraper.log_into_website()
kanshudoScraper.remove_advertisement()
words_for_excel = kanshudoScraper.scrape_vocabulary()
kanshudoScraper.close_driver()