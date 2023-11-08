import logging
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class WebDriver:
    adresses = []

    def __init__(self):
        self.PATH = "/Users/mjdaoudi/Development/MapsScrapper/chromedriver"
        self.options = Options()
        #self.options.add_argument("--headless")
        self.service = Service(executable_path=self.PATH)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def scroll_the_page(self, pause_time=1, max_iter=20000):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role = 'feed']"))
            )  # Waits for the page to load.

            x = 0
            while x < max_iter:
                try:
                    # Check if the button element is present on the screen
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//*[contains(text(), "You\'ve reached the end of the list.")]',
                            )
                        )
                        and EC.visibility_of_element_located(
                            (
                                By.XPATH,
                                '//*[contains(text(), "You\'ve reached the end of the list.")]',
                            )
                        )
                    )
                    # If the button is found, break out of the loop
                    break
                except:
                    pass

                scrollable_div = self.driver.find_element(
                    By.XPATH, "//div[@role = 'feed']"
                )  # It gets the section of the scroll bar.
                try:
                    self.driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight",
                        scrollable_div,
                    )  # Scroll it to the bottom.
                except:
                    pass
                time.sleep(pause_time)  # wait for more reviews to load.
                x = x + 1

        except NoSuchElementException:
            logging.error("No Such Element Exception")
            self.driver.quit()

        return None

    def refuse_cookies(self):
        time.sleep(2)
        self.driver.find_element(
            "xpath",
            '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[1]/div/div/button',
        ).click()
        return None

    def search(self, word_search):
        time.sleep(1)
        input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="searchboxinput"]'))
        )
        input.clear()
        input.send_keys(word_search)
        time.sleep(1)
        searchButton = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="searchbox-searchbutton"]')
            )
        )
        searchButton.click()
        time.sleep(1)
        return None

    def get_restaurant_data(self):
        time.sleep(2)
        res_data = {}

        try:
            name = self.driver.find_element(
                By.XPATH,
                '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1',
            )
            res_data["name"] = name.text
        except:
            pass

        try:
            avg_rating = self.driver.find_element(
                By.XPATH,
                '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]',
            )
            res_data["avg_rating"] = avg_rating.text
        except:
            pass

        try:
            total_reviews = self.driver.find_element(
                By.XPATH,
                '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span',
            )
            res_data["total_reviews"] = total_reviews.text[1:-1]
        except:
            pass

        try:
            address = self.driver.find_element(
                By.CSS_SELECTOR, "[data-item-id='address']"
            )
            res_data["address"] = address.text
        except:
            pass

        try:
            phone_number = self.driver.find_element(
                By.CSS_SELECTOR, "[data-tooltip='Copy phone number']"
            )
            res_data["phone_number"] = phone_number.text
        except:
            pass

        try:
            website = self.driver.find_element(
                By.CSS_SELECTOR, "[data-item-id='authority']"
            )
            res_data["website"] = website.text
        except:
            pass

        return res_data

    def parse_restaurants(self):
        logging.info("Parsing Containers ")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role = 'feed']"))
        )
        container = self.driver.find_element(By.XPATH, "//div[@role = 'feed']")
        restaurants = container.find_elements(By.XPATH, "./div")

        logging.info(f"Found approx. {len(restaurants)/2} restaurants.")
        actions = ActionChains(self.driver)

        for restaurant in restaurants:
            # Scroll to the restaurant item
            logging.info("Scrolling to item")
            try:
                actions.move_to_element(restaurant).click(restaurant).perform()
                restaurant_data = self.get_restaurant_data()
                if restaurant_data != {}:
                    self.adresses.append(restaurant_data)
            except:
                pass
        return None

    def scrape(self, url, search):  # Passed the URL as a variable
        try:
            self.driver.get(url)

        except Exception:
            self.driver.quit()
            return

        logging.info("Refusing Cookies")
        self.refuse_cookies()

        logging.info(f"Searching for {search}")
        self.search(word_search=search)

        logging.info("Loading results")
        self.scroll_the_page()

        logging.info("Scrolled all the results.")
        self.parse_restaurants()

        logging.info("Closing Instance")
        self.driver.quit()  # Closing the driver instance.

        return self.adresses
