from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import random
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import pandas as pd
from django.core.management.base import BaseCommand
import time
import os


def get_pitchbook_table_ready():

    username = "Nathan.Zhang@ftpartners.com"
    password = "Mission555555"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) " \
                 "AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"

    opts = Options()
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36")
    opts.add_argument("window-size=1500,800")
    driver = webdriver.Chrome(chrome_options=opts)

    # Login
    driver.get("https://www.pitchbook.com")

    time.sleep(random.uniform(56, 57))  # Manual login, go to deals view page
    iframe = driver.find_elements_by_tag_name('iframe')[0]
    driver.switch_to_frame(iframe)

    #
    # iframe = driver.find_elements_by_tag_name('iframe')[0]
    # driver.switch_to_frame(iframe)
    #
    # usr_field = driver.find_element_by_name("login")
    # usr_field.send_keys(username)
    # time.sleep(random.uniform(1, 2))
    #
    # psd_field = driver.find_element_by_name("password")
    # psd_field.send_keys(password)
    # time.sleep(random.uniform(1, 2))
    #
    # psd_field.send_keys(Keys.RETURN)
    # time.sleep(random.uniform(1, 2))
    #
    # time.sleep(30)

    # driver\
    #     .find_element(By.CLASS_NAME, "hdr-mm-level1")\
    #     .find_element(By.XPATH, "//div[@data-id='COMPANY']").click()
    # print("Click COMPANIES & DEALS.")

    # time.sleep(6)
    # driver.find_element(By.XPATH, "//li[@id='fts_fingers_Industry_finger']").click()
    # print("Click Industry.")
    #
    # time.sleep(2)
    # driver.find_element(By.XPATH, "//*[contains(text(), '2. Consumer Products')]").click()
    # print("Click 2. Consumer Products")

    # time.sleep(2)
    # driver.find_element(By.CLASS_NAME, "as-top-search-button-wrapper").click()
    # print("Click SEARCH.")
    #
    # time.sleep(6)
    #
    # print("5 sec...")
    #
    # time.sleep(6)

    return driver


def get_data_on_this_page(driver=None):

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # left column
    left_col = soup \
        .find('div', {'class': 'sr-tv-body'}) \
        .find('div', {'class': 'sr-tv-column fixed', 'data-id': 'investorName'}, recursive=False) \
        .find('div', {'class': 'sr-tv-cells-container'}, recursive=False) \
        .find_all('div', {'class': 'sr-tv-cell'}, recursive=False)

    names_list = []  # list contains 250 company names
    for name in left_col:
        names_list.append(name
                          .find('div', {'class': 'title'}, recursive=False)
                          .find('a', {'class': 'prf-tooltip'})
                          .text)

    col_name = soup \
        .find('div', {'class': 'sr-tv-body'}) \
        .find('div', {'class': 'sr-tv-column fixed', 'data-id': 'investorName'}, recursive=False).get('data-id')

    left_col_df = pd.DataFrame({col_name: names_list})

    # right columns
    right_cols = soup\
        .find('div', {'class':'sr-tv-body'}) \
        .find('div',{'class':'sr-tv-movable-columns'}, recursive=False) \
        .find('div', {'class': 'scroller-container'}, recursive=False) \
        .find('div', {'class': 'scroller-content resizable-content ui-draggable ui-draggable-handle'}, recursive=False) \
        .find_all('div', {'class': 'sr-tv-column ui-resizable'}, recursive=False)

    right_cols_df = pd.DataFrame()

    for single_col in right_cols:
        col_name = single_col.get('data-id')
        col_value = []
        single_col = single_col.find_all('div', {'class': 'sr-tv-cell'})
        for row in single_col:
            col_value.append(row.text)
        right_single_col_df = pd.DataFrame({col_name: col_value})

        right_cols_df = pd.concat([right_cols_df, right_single_col_df], axis=1)

    single_page_df = pd.concat([left_col_df, right_cols_df], axis=1)

    return single_page_df


class Command(BaseCommand):

    help = 'get PB companies through table on PB'

    def handle(self, *args, **kwargs):

        total_time = time.time()
        driver = get_pitchbook_table_ready()

        # format://username:password@host:port/database
        engine = create_engine('postgresql://ranaoyang:1991627yar@aoranprojectdb.csbmq0o4oy2b.us-west-1.rds.amazonaws.com:5432/aoranprojectdb')
        print("Database Connected")

        i = 0
        wait_time = 0

        while True:

            start_time = time.time()
            single_df = get_data_on_this_page(driver)
            single_df.to_sql('pb_top_investors', engine, if_exists='append')
            i += 1
            print("Page", "%04d" % i, "Done;", "Wait", "{0:.2f}".format(wait_time), "sec;", "Run",
                  "{0:.2f}".format(time.time() - start_time), "sec;")

            try:
                driver.find_element(By.CSS_SELECTOR, ".right-holder.disabled")
                print("Done with all pages", "Total Time:", "{0:.2f}".format(time.time() - total_time), "sec;")
                break

            except NoSuchElementException:

                driver.find_element(By.CLASS_NAME, "right-holder").click()
                wait_time = time.time()
                WebDriverWait(driver, 1000).until(
                    lambda driver: driver.find_element(By.CLASS_NAME, "sr-tv-movable-columns") or
                                   driver.find_element(By.CLASS_NAME, "login-popup-wrap")
                )

                try:
                    driver.find_element(By.CLASS_NAME, "login-popup-wrap").find_element(By.CLASS_NAME,
                                                                                        "login-page-log-in").click()
                except:
                    pass
                wait_time = time.time() - wait_time

