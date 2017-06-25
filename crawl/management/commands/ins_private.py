# -*- coding: utf-8 -*


import random
import time

from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def login():
    try:
        opts = Options()
        opts.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36")
        opts.add_argument("window-size=1500,800")
        driver = webdriver.Chrome(chrome_options=opts)

        # Login
        driver.get("https://www.instagram.com/")
        time.sleep(random.uniform(6, 10))
        driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[2]/p/a").click()
        time.sleep(random.uniform(5, 9))

        # Username
        driver.find_element_by_xpath("//INPUT[@name='username']").click()
        username = driver.find_element_by_xpath("//INPUT[@name='username']")
        for i in 'ranaoyang@outlook.com':
            username.send_keys(i)
            time.sleep(random.uniform(0.1, 0.7))
        # Password
        driver.find_element_by_xpath("//INPUT[@name='password']").click()
        time.sleep(random.uniform(1, 3))
        password = driver.find_element_by_xpath("//INPUT[@name='password']")
        for i in '1991627yar':
            password.send_keys(i)
            time.sleep(random.uniform(0.1, 0.7))
        time.sleep(random.uniform(1, 3))
        driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/span/button").click()
        time.sleep(random.uniform(7, 9))
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/button").click()
            time.sleep(random.uniform(1, 3))
        except:
            pass

        return driver
    except Exception as e:
        return None


def search_keyword(search_input=None, driver=None):
    time.sleep(random.uniform(2, 4))
    driver.find_element_by_xpath("//*[@id='react-root']/section/nav/div/div/div/div[2]/div/div/span[2]").click()
    input_box = driver.find_element_by_xpath("//*[@id='react-root']/section/nav/div/div/div/div[2]/input")
    for i in search_input:
        time.sleep(random.uniform(0.4, 0.7))
        input_box.send_keys(i)
        time.sleep(random.uniform(0.1, 0.7))
    input_box.send_keys(Keys.ENTER)
    time.sleep(random.uniform(3, 6))


def loop_and_like(driver=None, max_like=100):

    # Click initial picture
    time.sleep(random.uniform(2.5, 4.5))
    driver.find_elements_by_xpath("//a[contains(@href,'/p/')]")[0].click()
    like_counter = 0
    time.sleep(random.uniform(2.5, 4.5))

    # While loop
    while driver.find_element_by_xpath("//a[contains(@class,'coreSpriteRightPaginationArrow')]"):
        time.sleep(random.uniform(2.5, 4.5))
        driver.find_element_by_xpath("//span[contains(@class,'coreSpriteLikeHeartOpen')]").click()
        like_counter += 1
        time.sleep(random.uniform(2.5, 4.5))
        driver.find_element_by_xpath("//a[contains(@class,'coreSpriteRightPaginationArrow')]").click()
        time.sleep(random.uniform(2.5, 4.5))
        if like_counter % 10 == 0:
            print(like_counter)
        if like_counter > max_like:
            break


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):

        # Login
        driver = login()

        # Search Keyword
        search_keyword(search_input="#food", driver=driver)

        # Loop pic and like them
        loop_and_like(driver=driver, max_like=120)

        driver.close()



