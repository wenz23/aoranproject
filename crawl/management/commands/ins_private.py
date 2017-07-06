# -*- coding: utf-8 -*


import time

import random
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from settings.production import ins_passwords, ins_tags, ins_comments


def ins_login(user_name=None):
    try:
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36")
        opts.add_argument("window-size=1500,800")
        driver = webdriver.Chrome(chrome_options=opts)

        # Login
        driver.get("https://www.instagram.com/")
        time.sleep(random.uniform(5, 7))
        driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[2]/p/a").click()
        time.sleep(random.uniform(3, 5))

        # Username
        driver.find_element_by_xpath("//INPUT[@name='username']").click()
        username = driver.find_element_by_xpath("//INPUT[@name='username']")
        for i in user_name:
            username.send_keys(i)
            time.sleep(random.uniform(0.2, 0.6))

        # Password
        driver.find_element_by_xpath("//INPUT[@name='password']").click()
        time.sleep(random.uniform(2, 3))
        password = driver.find_element_by_xpath("//INPUT[@name='password']")
        for i in ins_passwords[user_name]:
            password.send_keys(i)
            time.sleep(random.uniform(0.2, 0.6))
        time.sleep(random.uniform(2, 3))

        # Click Login
        driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/span/button").click()
        time.sleep(random.uniform(7, 9))

        try:
            driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/button").click()
            time.sleep(random.uniform(2, 3))
        except:
            pass

        return driver
    except Exception as e:
        print("Login Error", e)
        return None


def search_ins_tags(tag_input=None, driver=None):
    time.sleep(random.uniform(2, 4))
    driver.find_element_by_xpath("//*[@id='react-root']/section/nav/div/div/div/div[2]/div/div/span[2]").click()
    input_box = driver.find_element_by_xpath("//*[@id='react-root']/section/nav/div/div/div/div[2]/input")
    for i in tag_input:
        time.sleep(random.uniform(0.4, 0.7))
        input_box.send_keys(i)

    time.sleep(random.uniform(1, 2))
    input_box.send_keys(Keys.ENTER)
    time.sleep(random.uniform(3, 6))
    print('Search Tag:', tag_input)
    return driver


def loop_and_like(driver=None, max_like=50, comment_items=None):

    # Click initial picture
    time.sleep(random.uniform(2.5, 4.5))
    driver.find_elements_by_xpath("//a[contains(@href,'/p/')]")[0].click()
    like_counter = 0
    time.sleep(random.uniform(2.5, 4.5))

    # While loop
    while driver.find_element_by_xpath("//a[contains(@class,'coreSpriteRightPaginationArrow')]"):
        time.sleep(random.uniform(2.5, 4.5))
        try:
            driver.find_element_by_xpath("//span[contains(@class,'coreSpriteHeartOpen')]").click()
            like_counter += 1
            time.sleep(random.uniform(2.5, 4.5))
        except:
            pass
        # Comment
        try:
            driver.find_element_by_xpath("//textarea[contains(@aria-label,'Add a comment…')]").click()
            comment_input = driver.find_element_by_xpath("//textarea[contains(@aria-label,'Add a comment…')]")
            for i in random.choice(comment_items):
                comment_input.send_keys(i)
                time.sleep(random.uniform(0.2, 0.6))
            comment_input.send_keys(Keys.RETURN)
            time.sleep(random.uniform(2, 3))

        except:
            pass
        driver.find_element_by_xpath("//a[contains(@class,'coreSpriteRightPaginationArrow')]").click()
        time.sleep(random.uniform(2.5, 4.5))
        if like_counter % 10 == 0:
            print(like_counter)
        if like_counter > max_like:
            break
    driver.find_element_by_xpath("/html/body/div[2]/div/button").click()
    time.sleep(random.uniform(2.5, 4.5))
    return driver


def mass_like_and_comment(driver=None, search_items=None, comment_items=None, max_like=50, max_comment=50, search_tags=False):
    for each_search_item in search_items:
        if search_tags:
            each_search_item = each_search_item if str(each_search_item).startswith('#') else '#' + each_search_item
            driver = search_ins_tags(driver=driver, tag_input=each_search_item)
            driver = loop_and_like(driver=driver, comment_items=comment_items)
    return driver


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):

        # Login
        driver = ins_login(user_name='a.wen.z')

        # Search Keyword
        driver = mass_like_and_comment(driver=driver, search_items=random.sample(ins_tags['a.wen.z'], 20), comment_items=ins_comments['a.wen.z'], search_tags=True)

        driver.close()



