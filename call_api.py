from urllib.parse import urlparse
import requests
import re

def url_syntax(url_changes):
    url_search_http = re.search("http", url_changes)
    if url_search_http is None:
        url_http = "http://" + url_changes
    else:
        url_http = url_changes
    return url_http # Returns the url with 'http://' if not there in the input url

def api_call(inurl, seurl):
    '''
    "inurl" is the input url which is suspected to be phishing site.
    "seurl" is the select url in which only the domain name of the orginal site is to be given as in put.
    '''
    check = url_syntax (inurl)
    inurl = urlparse(check).netloc
    URL = "https://phishbuster-web.herokuapp.com/api/"+ inurl + '+' + seurl
    req = requests.get(url = URL)
    return req.json()

if __name__ == '__main__':
    print(api_call('https://www.microsoft.com~@www.google.com/wsgrye/ruygfbryu/gijgnuf','google.com'))

