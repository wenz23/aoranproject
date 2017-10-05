# -*- coding: utf-8 -*
import logging
import random
import time

from django.core.management.base import BaseCommand
from django.utils import timezone
from selenium import webdriver

from crawl.models import InstagramMap, StateEnum
from settings.base import BASE_DIR, phantom_js_driver_path, ins_passwords

log = logging.getLogger('phantomjs_crawler')


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
                                     service_log_path=BASE_DIR + '/logs/ghostdriver.log')

        for key, value in enumerate(headers):
            capability_key = 'phantomjs.page.customHeaders.{}'.format(key)
            webdriver.DesiredCapabilities.PHANTOMJS[capability_key] = value

        driver.set_window_size(random.randint(1500, 1560), random.randint(800, 820))

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
        for i in ins_passwords[user_name][0]:
            password.send_keys(i)
            time.sleep(random.uniform(0.2, 0.6))
        time.sleep(random.uniform(2, 3))

        # Click Login
        driver.find_element_by_xpath(
            "//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/span/button").click()
        time.sleep(random.uniform(7, 9))

        try:
            driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/button").click()
            time.sleep(random.uniform(2, 3))
        except:
            pass
        log.info("%s %s %s", user_name, "Login time: ", str("%.2f" % (time.time() - login_start_time)))

        return driver
    except Exception as e:
        log.error("%s %s %s", user_name, "Login Error", str(e))
        # driver.save_screenshot(BASE_DIR + '/phantomjs_screenshots/login_error.png')
        return None


def loop_similar_people(driver=None, max_loop=5, ins_map_obj=None, user_name=None):
    loop_counter, new_similar_counter, exist_similar_counter = 0, 0, 0

    try:
        time.sleep(random.uniform(6, 7))
        driver.find_element_by_xpath("//div[contains(@class,'coreSpriteDropdownArrowWhite')]").click()
        time.sleep(random.uniform(2, 3))

        while loop_counter < max_loop:
            loop_counter += 1
            new_guys = [am.get_attribute('href') for am in
                        driver.find_elements_by_xpath("//a[contains(@style,'width: 54px; height: 54px;')]")]
            for i in new_guys:
                ins_username = i.split('/')[3]
                isp_obj, created = InstagramMap.objects.get_or_create(latest_username=str(ins_username).lower())

                if ins_map_obj.project_info and ins_map_obj.project_info != {}:
                    isp_obj.project_info = {**isp_obj.project_info, **ins_map_obj.project_info}
                    isp_obj.save()

                if created:
                    new_similar_counter += 1
                else:
                    exist_similar_counter += 1
            try:
                driver.find_elements_by_xpath("//div[contains(@class,'coreSpritePagingChevron')]")[1].click()
                time.sleep(random.uniform(1.5, 2))
            except:
                driver.find_element_by_xpath("//div[contains(@class,'coreSpritePagingChevron')]").click()
                time.sleep(random.uniform(1.5, 2))
        ins_map_obj.ins_find_similar = True
        ins_map_obj.latest_similar_at = timezone.now()
        ins_map_obj.save()
        log.info(" ".join([user_name, "Similar Results:", ins_map_obj.latest_username, ":",
                           "Loop:", str(loop_counter),
                           "; New:", str(new_similar_counter),
                           "; Existing:", str(exist_similar_counter)]))
        return driver
    except Exception as e:
        log.error("%s %s %s", user_name, "Loop Error", ins_map_obj.latest_username)
        # try:
        #     # driver.save_screenshot(BASE_DIR + '/phantomjs_screenshots/'+str(ins_map_obj.latest_username)+'loop_error.png')
        # except:
        #     pass
        return driver
        pass


def type_in_search_box(driver=None, type_input=None, user_name=None):
    found_this_guy = False

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

        search_results = driver.find_elements_by_xpath(
            "//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a")
        for each_result in search_results:
            if "/tags/" not in each_result.get_attribute('href') and "/explore/locations/" not in each_result.get_attribute('href'):
                each_result.click()
                found_this_guy = True
                break
        time.sleep(random.uniform(5, 6))
        if found_this_guy:
            pass
            # log.info("%s %s %s", user_name, "Search  Finish :", str(type_input))
        else:
            log.info("%s %s %s", user_name, "Search Not Find:", str(type_input))
    return driver, found_this_guy


def search_ins_people(driver=None, ins_map_obj=None, user_name=None):
    if driver and ins_map_obj:
        try:
            driver, found_this_guy = type_in_search_box(driver=driver, type_input=ins_map_obj.latest_username, user_name=user_name)
        except Exception as e:
            found_this_guy = False
            ins_map_obj.latest_crawl_state = StateEnum.Other_Error
            ins_map_obj.save()
            log.error("%s %s %s", user_name, "Search Error. Reason: ", str(e))
            pass

        if found_this_guy:
            try:
                driver = loop_similar_people(driver=driver, ins_map_obj=ins_map_obj, user_name=user_name)
            except Exception as e:
                log.error("%s %s %s %s", user_name, ins_map_obj.latest_username, "Loop Error. Reason:", str(e))
                pass
        else:
            ins_map_obj.latest_crawl_state = StateEnum.User_Not_Exist
            ins_map_obj.save()

        return driver


def get_list(order=None, skip=150, queue_length=240, focus_project=False):
    if focus_project:
        ins_people_list = [am for am in InstagramMap.objects.exclude(project_info={})]

    else:
        ins_people_list = [am for am in InstagramMap.objects.filter(latest_follower_count__gte=10000,
                                                                    latest_follower_count__lte=400000,
                                                                    ins_find_similar=False
                                                                    ).exclude(latest_crawl_state=404
                                                                              ).order_by('created_at')]

        ins_people_list = ins_people_list[skip + queue_length * order:skip + queue_length * order + queue_length]

    return ins_people_list


def get_parameters(options=None, focus_project=None):
    usr, order, st = options['usr'][0], ins_passwords[options['usr'][0]][1], time.time()

    i_list = get_list(order=order, focus_project=focus_project)
    log.info("%s %s %s; %s %s",
             str(usr), "Process Start:", str(timezone.now().isoformat()), "List Size:", str(len(i_list)))
    return usr, st, i_list


def end_process(driver=None, st=None, user_name=None):
    driver.close()
    log.info("%s %s %s %s", user_name, "End", "Total time spent: ", str("%.2f" % (time.time() - st)))


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--usr', nargs='+')

    def handle(self, *args, **options):

        # Get Parameters Ready
        usr, st, i_list = get_parameters(options=options, focus_project=False)

        # Login
        driver = ins_login(user_name=usr)

        for i in i_list:
            driver = search_ins_people(driver=driver, ins_map_obj=i, user_name=usr)

        # End Process
        end_process(driver=driver, st=st, user_name=usr)
