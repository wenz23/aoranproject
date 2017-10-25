import random
import time

from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def search_page(city_name=None, category_name=None):
    mobile_emulation = {"deviceName": "iPhone 6 Plus"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver = webdriver.Chrome('/Users/aoran/aoranproject/aws/chromedriver',
                              desired_capabilities=chrome_options.to_capabilities())
    driver.set_window_size(450, 900)
    driver.get('http://www.google.com/xhtml')
    time.sleep(random.uniform(4, 6))
    input_box = driver.find_element_by_xpath('//*[@id="lst-ib"]')
    input_box.click()
    time.sleep(random.uniform(4, 6))
    input_box.clear()
    search_item = str(category_name) + " in " + str(city_name)
    for i in search_item:
        input_box.send_keys(i)
        time.sleep(random.uniform(0.2, 0.6))

    input_box.send_keys(Keys.RETURN)

    time.sleep(random.uniform(4, 6))
    return driver


def nav_to_result_page(driver=None, max_page=10, high_rating=True):
    time.sleep(random.randint(4, 6))
    scroll = 0
    times = 0
    driver.execute_script("window.scrollTo(0, " + str(random.randint(290, 300)) + ");")
    time.sleep(random.randint(4, 6))
    more_places = driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[2]/div[1]/div[3]/div/g-immersive-footer/g-fab/span')
    more_places.click()
    time.sleep(random.randint(4, 6))

    while times < 10:
        results = [am for am in driver.find_elements_by_xpath('//div[contains(@jsaction, "hero_carousel_call_to_action_card_shown")]') if am.is_displayed()]

        for result in results:
            try:
                result.click()
                time.sleep(random.randint(3, 5))
                # Parse Here
                driver.find_elements_by_xpath('//span[contains(@class,"kp-header-icon")]')[0].click()
                time.sleep(random.randint(3, 5))
            except Exception as e:
                print(str(e))
                pass

        time.sleep(random.uniform(2, 4))
        times += 1
        scroll += 550
        driver.execute_script("window.scrollTo(0, " + str(scroll) + ");")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        driver = search_page(city_name='San Francisco', category_name='Boutique Shop')
        nav_to_result_page(driver=driver)
