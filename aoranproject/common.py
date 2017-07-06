import requests


def request(url=None, proxy=False, counter=0, max_request=5):
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome\
            /55.0.2883.95 Safari/537.36',
        'accept-language': 'en-US,en;q=0.8',
        'X-Proxy-Country': 'US'}

    if counter > max_request:
        return None
    else:

        try:
            # Actual Request
            if proxy:
                raw_proxy = "charityengine.services:20000"  # workdistribute.charityengine.com:20000 / charityengine.services
                ce_proxies = {'https': 'https://41b129a39e6c4a1db44a795691a0b6af: @' + raw_proxy,
                              'http': 'http://41b129a39e6c4a1db44a795691a0b6af: @' + raw_proxy
                              }
                proxies = {'proxy': ce_proxies}
                req = requests.request('GET', url=url, headers=header, timeout=25, verify=False, proxies=proxies['proxy'])
            else:
                req = requests.request('GET', url=url, headers=header, timeout=25, verify=False)

            #
            if req.status_code == 404 and counter > 3:
                return None
            elif req.status_code != 200:
                request(url=url, proxy=proxy, counter=counter + 1, max_request=max_request)
            else:
                return req
        except Exception as e:
            if counter == max_request - 1:
                print("Request Max Times, URL: ", url, ', Error: ', e)
            else:
                request(url=url, proxy=proxy, counter=counter + 1, max_request=max_request)
