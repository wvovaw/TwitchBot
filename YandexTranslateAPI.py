from urllib.request import urlopen, Request
from urllib.parse import quote
import re

AUTHKEY = 'trnsl.1.1.20191202T210131Z.0efaaf74a79b747b.66acfde631d5a271bca8f55e333f0f42e668fdc7'
HOST = 'https://translate.yandex.net/api/v1.5/tr/translate'

def translate(origin_text, target_lang):
    query = HOST + '?key=' + AUTHKEY + '&text=' + quote(origin_text)  + '&lang=' + quote(target_lang) + '&format=plain'
    try:
        request = Request(query)
    except:
        print('ERROR: Bad query: ' + query)
        return None
    try:
        response = urlopen(request)
    except:
        print('ERROR: Bad request')
        return None
    xml = response.read()
    response.close()
    xml = xml.decode('utf-8')
    xml = xml.split('<text>')
    xml = xml[1].split('</text>')
    return xml[0]   
