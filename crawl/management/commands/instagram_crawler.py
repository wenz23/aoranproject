import threading
import time
from queue import Queue
from threading import Thread

import requests
import simplejson as json
import urllib3
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils import timezone

from crawl.models import StateEnum, SocialDetails

urllib3.disable_warnings()


def parse_webpage(req=None, urldetail_obj=None, q=None):
    soup = BeautifulSoup(req.content, 'html.parser')

    # YouTube
    if 'youtube.com' in req.url:
        try:
            related_links   = [li.find('a').get('href') for li in soup.findAll('li', {'class': 'channel-links-item'})]
        except:
            related_links   = None
        try:
            stats           = '; '.join([span.text for span in soup.find('div', {'class': 'about-stats'}).findAll('span')])
        except:
            stats           = None
        try:
            descr           = soup.find('pre').text
        except:
            descr           = None
        try:
            country         = soup.find('span', {'class': 'country-inline'}).text
        except:
            country         = None
        try:
            biz_email       = True if soup.find('span', {'class': 'business-email-label'}) else False
        except:
            biz_email       = None
        try:
            similar_links   = [a.get('href') for a in soup.find_all('a', class_='ux-thumb-wrap')]
        except:
            similar_links   = None

        details_dict = {'related_links': related_links,
                        'stats': stats,
                        'descr': descr,
                        'country': country,
                        'biz_email': biz_email,
                        'similar_links': similar_links}

        urldetail_obj.details = json.dumps(details_dict)
        if len(details_dict) > 4:
            urldetail_obj.parse_state = StateEnum.Parse_Success
        else:
            urldetail_obj.parse_state = StateEnum.Parse_Failed
        urldetail_obj.save()


def parse_via_q(q):
    while not q.empty():

        # Create social detail object
        urldetail_obj = q.get()
        if (timezone.now() - urldetail_obj.created_at).days > 5:
            urldetail_obj = SocialDetails(social_id=urldetail_obj.social_id,
                                          source_type=urldetail_obj.source_type,
                                          created_at=timezone.now())
            urldetail_obj.save()

        # Request social url
        req = proxy_request(urldetail_obj=urldetail_obj)

        # Parse web page
        if req:
            parse_webpage(req=req, urldetail_obj=urldetail_obj, q=q)
        if q.qsize() % 20 == 0:
            print("Q Size # ", q.qsize())
    return True


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        q = Queue()

        starting_list = [am for am in SocialDetails.objects.exclude(parse_state=600)]

        for i in starting_list:
            q.put(i)
        print("Starting Queue Size # ", q.qsize())

        # setting up queue
        sys_threads = threading.active_count()
        threads = 10
        c = 0

        #############################
        # parse_via_q(q)
        #############################

        while not q.empty():
            try:
                c += 1
                tc = threading.active_count()
                if tc < (threads + sys_threads):
                    print('Active Threads::' + str(tc))
                    worker = Thread(target=parse_via_q, args=(q,))
                    worker.daemon = True
                    worker.start()
                    time.sleep(0.1)
                else:
                    time.sleep(150)
            except Exception as e:
                print(e)
