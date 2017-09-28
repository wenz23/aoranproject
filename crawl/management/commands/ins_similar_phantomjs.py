# -*- coding: utf-8 -*
import random
import time
from settings.base import BASE_DIR, phantom_js_driver_path, ins_passwords
from django.core.management.base import BaseCommand
from django.utils import timezone
from selenium import webdriver

from crawl.models import InstagramMap


def ins_login(user_name=None):
    login_start_time = time.time()
    try:
        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'accept-encoding': 'gzip, deflate, br',
                   'accept-language': 'en-US,en;q=0.8',
                   'upgrade-insecure-requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
                   }

        driver = webdriver.PhantomJS(executable_path=phantom_js_driver_path,
                                     service_log_path=BASE_DIR + '/phantom_js_screenshots/ghostdriver.log')

        for key, value in enumerate(headers):
            capability_key = 'phantomjs.page.customHeaders.{}'.format(key)
            webdriver.DesiredCapabilities.PHANTOMJS[capability_key] = value

        driver.set_window_size(random.randint(1500, 1560), random.randint(800, 820))

        # Login
        driver.get("https://www.instagram.com/")
        time.sleep(random.uniform(5, 7))
        driver.save_screenshot(BASE_DIR + '/phantom_js_screenshots/1-login-page.png')
        driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[2]/p/a").click()
        time.sleep(random.uniform(3, 5))

        # Username
        driver.find_element_by_xpath("//INPUT[@name='username']").click()
        username = driver.find_element_by_xpath("//INPUT[@name='username']")
        for i in user_name:
            username.send_keys(i)
            time.sleep(random.uniform(0.2, 0.6))
        driver.save_screenshot(BASE_DIR + '/phantom_js_screenshots/2-type-username.png')
        # Password
        driver.find_element_by_xpath("//INPUT[@name='password']").click()
        time.sleep(random.uniform(2, 3))
        password = driver.find_element_by_xpath("//INPUT[@name='password']")
        for i in ins_passwords[user_name][0]:
            password.send_keys(i)
            time.sleep(random.uniform(0.2, 0.6))
        time.sleep(random.uniform(2, 3))
        driver.save_screenshot(BASE_DIR + '/phantom_js_screenshots/3-type-password.png')

        # Click Login
        driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/span/button").click()
        time.sleep(random.uniform(7, 9))
        driver.save_screenshot(BASE_DIR + '/phantom_js_screenshots/4-logged-in.png')

        try:
            driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/button").click()
            time.sleep(random.uniform(2, 3))
        except:
            pass
        driver.save_screenshot(BASE_DIR + '/phantom_js_screenshots/5-homepage.png')
        print("Login time: ", str(time.time() - login_start_time))

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
        time.sleep(random.uniform(1, 2))
        while counter < max_loop:
            counter += 1
            new_guys = [am.get_attribute('href') for am in
                        driver.find_elements_by_xpath("//a[contains(@style,'width: 54px; height: 54px;')]")]
            for i in new_guys:
                ins_username = i.split('/')[3]
                isp_obj, created = InstagramMap.objects.get_or_create(latest_username=str(ins_username).lower())

            try:
                driver.find_elements_by_xpath("//div[contains(@class,'coreSpritePagingChevron')]")[1].click()
                time.sleep(random.uniform(1.5, 2))
            except:
                driver.find_element_by_xpath("//div[contains(@class,'coreSpritePagingChevron')]").click()
                time.sleep(random.uniform(1.5, 2))
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

        # Click on Search Box
        time.sleep(random.uniform(2, 3))
        driver.find_element_by_xpath("//span[contains(@class,'coreSpriteSearchIcon')]").click()
        time.sleep(random.uniform(1, 2))

        # Clean Search Box
        input_box = driver.find_element_by_xpath("//input[contains(@placeholder, 'Search')]")
        input_box.clear()

        # Type in Search Box
        for i in type_input:
            time.sleep(random.uniform(0.4, 0.7))
            input_box.send_keys(i)
        time.sleep(random.uniform(1, 2))

        # Select First Non-HashTag Element
        search_results = driver.find_elements_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a")
        for each_result in search_results:
            if "/tags/" not in each_result.get_attribute('href'):
                each_result.click()
                break

        time.sleep(random.uniform(5, 6))
        print('Search:', type_input)
    return driver


def search_ins_people(driver=None, ins_map_obj=None):

    if driver and ins_map_obj:
        try:
            driver = type_in_search_box(driver=driver, type_input=ins_map_obj.latest_username)
            try:
                driver.save_screenshot(BASE_DIR + '/phantom_js_screenshots/search_'+ins_map_obj.latest_username+'.png')
            except:
                print('Cannot save search png')
        except:
            print('Search Error')
            pass
        try:
            driver = loop_similar_people(driver=driver, ins_map_obj=ins_map_obj)
            try:
                driver.save_screenshot(BASE_DIR + '/phantom_js_screenshots/loop_'+ins_map_obj.latest_username+'.png')
            except:
                print('Cannot save loop png')
        except:
            print('Loop Error')
            pass

        return driver


def get_list(order=None, skip=150, queue_length=240):
    ins_people_list = [am for am in InstagramMap.objects.filter(latest_follower_count__gte=10000,
                                                                latest_follower_count__lte=400000,
                                                                ins_find_similar=False
                                                                ).order_by('created_at')]
    print("Starting Size: ", len(ins_people_list))

    ins_people_list = ins_people_list[skip + queue_length * order:skip + queue_length * order + queue_length]

    return ins_people_list


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):

        parser.add_argument('--usr', nargs='+')

    def handle(self, *args, **options):

        usr, order, st = options['usr'][0], ins_passwords[options['usr'][0]][1], time.time()
        i_list = get_list(order=order)

        # Login
        driver = ins_login(user_name=usr)

        for i in i_list:
            driver = search_ins_people(driver=driver, ins_map_obj=i)

        driver.close()
        print("Time spent: ", str(time.time() - st))
