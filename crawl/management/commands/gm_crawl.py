import random
import time

from django.core.management.base import BaseCommand
from selenium import webdriver
from crawl.models import GoogleMap
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

    while times < 50:
        results = [am for am in driver.find_elements_by_xpath('//div[contains(@jsaction, "hero_carousel_call_to_action_card_shown")]') if am.is_displayed()]

        for result in results:
            try:
                result.click()
                time.sleep(random.randint(3, 5))

                # Parse Here
                driver = gm_parser(driver=driver)

                driver.find_elements_by_xpath('//span[contains(@class,"kp-header-icon")]')[0].click()
                time.sleep(random.randint(3, 5))
            except Exception as e:
                print(str(e))
                pass

        time.sleep(random.uniform(2, 4))
        times += 1
        scroll += 550
        driver.execute_script("window.scrollTo(0, " + str(scroll) + ");")


def gm_parser(driver=None):
    try:
        cid = driver.find_element_by_xpath('//div[@data-cid!=""][@data-fid!=""]').get_attribute('data-cid')
    except Exception as e:
        print(e)
        cid=None
        pass
    try:
        name = driver.find_element_by_xpath('//div[@style="opacity: 1; z-index: 2;"]').text
    except Exception as e:
        print(e)
        name = None
    try:
        rating = driver.find_element_by_xpath('//span[contains(@class, "rtng")][@aria-hidden="true"]').text
    except Exception as e:
        print(e)
        rating = None
    try:
        reviews = driver.find_element_by_xpath('//span[contains(@aria-label, " reviews")]').text
    except Exception as e:
        print(e)
        reviews = None
    try:
        website = driver.find_element_by_xpath('//a[contains(@class, "lua-button")][contains(@href, "http")][contains(@ping, "url")]').get_attribute('href')
    except Exception as e:
        print(e)
        website = None
        pass
    try:
        descr = driver.find_element_by_xpath('//div[@role="button"][contains(@jsl, "$x 1;")]').text
    except Exception as e:
        print(e)
        descr = None
        pass
    try:
        address = driver.find_element_by_xpath('//div[@aria-label="Address:"]/following-sibling::div').text
    except Exception as e:
        print(e)
        address = None
        pass
    try:
        phone = driver.find_element_by_xpath('//span[@aria-label="Phone:"]/following-sibling::span').text
    except Exception as e:
        print(e)
        phone = None
        pass
    try:
        gm_obj, created = GoogleMap.objects.get_or_create(cid=cid)
        gm_obj.name = name
        gm_obj.phone = phone
        gm_obj.rating = rating
        gm_obj.reviews = reviews
        gm_obj.website = website
        gm_obj.description = descr
        gm_obj.save()
    except Exception as e:
        print(e)
        pass


    return driver


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        driver = search_page(city_name='San Francisco', category_name='Boutique Shop')
        nav_to_result_page(driver=driver)
