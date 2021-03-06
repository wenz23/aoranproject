from simplejson import loads

import requests
from django.core.management.base import BaseCommand


def request_func(url=None):
    header = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        "accept-language": "en-US,en;q=0.8",
        "X-Proxy-Country": "US"
    }

    try:
        req = requests.request('GET', url=url, headers=header, timeout=25, verify=False)
        if req.status_code == 200:
            return True, req.content
        else:
            return False, {"error": "request failed: not 200", "status code": str(req.status_code), "url": url}
    except:
        return False, {"error": "request failed: request function try except", "url": url}


def parse_ins(req_content=None):
    try:
        html = req_content
        text = html[html.index(str("window._sharedData = ").encode("utf-8")) + 21:]
        text = (text[:text.index(str("};</script>").encode("utf-8"))] + str("}").encode("utf-8")).replace(
            str('\\"').encode("utf-8"), str("").encode("utf-8"))
        dictionary = loads(text)
        return dictionary
    except Exception as e:
        return {'error': 'parse ins function try except'+ str(e)}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        try:
            url = "https://www.instagram.com/animeromance___/"
            success, content = request_func(url=url)
            if success:
                return parse_ins(req_content=content)
            else:
                return content
        except Exception as e:
            return {"error": "handler function try except: " + str(e)}
