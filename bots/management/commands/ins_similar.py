# -*- coding: utf-8 -*


import time

import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from crawl.models import InstagramMap
from settings.production import ins_passwords


def ins_login(user_name=None):
    try:
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36")
        opts.add_argument("window-size=1500,800")
        driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=opts)

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


def mass_find_similar(driver=None, people_list=None):
    if people_list:
        for i in people_list:
            driver = search_ins_people(driver=driver, ins_map_obj=i)
    pass


def loop_similar_people(driver=None, max_loop=5, ins_map_obj=None):
    counter = 0
    try:
        time.sleep(random.uniform(4, 6))
        driver.find_element_by_xpath("//div[contains(@class,'coreSpriteDropdownArrowWhite')]").click()
        time.sleep(random.uniform(3, 4))
        while counter < max_loop:
            counter += 1
            new_guys = [am.get_attribute('href') for am in
                        driver.find_elements_by_xpath("//a[contains(@style,'width: 54px; height: 54px;')]")]
            for i in new_guys:
                ins_username = i.split('/')[3]
                isp_obj, created = InstagramMap.objects.get_or_create(latest_username=str(ins_username).lower())

            try:
                driver.find_elements_by_xpath("//div[contains(@class,'coreSpritePagingChevron')]")[1].click()
                time.sleep(random.uniform(3, 4))
            except:
                driver.find_element_by_xpath("//div[contains(@class,'coreSpritePagingChevron')]").click()
                time.sleep(random.uniform(3, 4))
        ins_map_obj.ins_find_similar = True
        ins_map_obj.latest_similar_at = timezone.now()
        ins_map_obj.save()
        return driver
    except Exception as e:
        print(e)
        return driver
        pass


def type_in_search_box(driver=None, type_input=None):
    if driver and type_input:
        # time.sleep(random.uniform(2, 4))
        # driver.execute_script("window.scrollTo(0," + str(random.randint(80, 140)) + ")")
        time.sleep(random.uniform(3, 4))
        driver.find_element_by_xpath("//span[contains(@class,'coreSpriteSearchIcon')]").click()
        input_box = driver.find_element_by_xpath("//input[contains(@placeholder, 'Search')]")
        for i in type_input:
            time.sleep(random.uniform(0.4, 0.7))
            input_box.send_keys(i)
        # Enter Twice
        time.sleep(random.uniform(2, 4))
        input_box.send_keys(Keys.ENTER)
        time.sleep(random.uniform(2, 4))
        input_box.send_keys(Keys.ENTER)

        time.sleep(random.uniform(5, 6))
        print('Search:', type_input)
    return driver


def search_ins_people(driver=None, ins_map_obj=None):

    if driver and ins_map_obj:
        try:
            driver = type_in_search_box(driver=driver, type_input=ins_map_obj.latest_username)
        except:
            print('Search Error')
            pass
        try:
            driver = loop_similar_people(driver=driver, ins_map_obj=ins_map_obj)
        except:
            print('Loop Error')
            pass

        return driver


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):

        ins_people_list = [am for am in InstagramMap.objects.filter(latest_follower_count__gte=3000,
                                                                    ins_find_similar=False
                                                                    ).order_by('created_at')[:150]]

        # Login
        driver = ins_login(user_name='ranaoyang@outlook.com')  # a.wen.z

        for i in ins_people_list:
            driver = search_ins_people(driver=driver, ins_map_obj=i)

        time.sleep(3)
        driver.close()
