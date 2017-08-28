import urllib3

urllib3.disable_warnings()


def ins_clean_url(url=None, return_id=False):
    try:
        temp_id = url.split('?')[0].split('instagram.com')[1].replace('/', '')
        if temp_id == '' or temp_id is None or temp_id == ' ' or temp_id == '/' or temp_id == '//':
            return None

        if return_id:
                return temp_id
        else:
            return 'https://www.instagram.com/' + url.split('?')[0].split('instagram.com')[1].replace('/', '') + '/'
    except Exception as e:
        print('Parse ins url failed; URL:' + url + '; Error: ' + str(e))
        return None
