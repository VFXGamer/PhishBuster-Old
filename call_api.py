from urllib.parse import urlparse
import requests
import re

def url_syntax(url_changes):
    url_search_http = re.search("http", url_changes) # for finding http using regular expressions
    if url_search_http is None:
        url_http = "http://" + url_changes # adding http:// at the start if it is not present
    else:
        url_http = url_changes # if http:// is present the return the input url
    return url_http # Returns the url with 'http://'
def api_call(inurl, seurl,country, store = 'False'):
    '''
    "inurl" is the input url which is suspected to be phishing site.
    "seurl" is the select url in which only the domain name of the orginal site is to be given as in put.
    "country" here is the iso code of the country that is 'in' for 'India' etc.
    '''
    iinurl = inurl.lower()
    seurl = seurl.lower()
    country = country.lower()
    check = url_syntax (inurl) # adds http:// if not there in the url
    inurl = urlparse(check).netloc # removing path and https:// from a url
    # inurl is the input url, seurl is the orginal domain and store is the permission to store data if it is a phishing site
    URL = "http://phishbuster-web.herokuapp.com/api/"+ inurl + '+' + seurl + '+' + country + '+' + store
    req = requests.get(url = URL) # sends a get request to the PhishBuster API
    return req.json() # Reading data with json

if __name__ == '__main__':
    print(api_call(inurl='https://www.microsoft.com~@www.google.com/wsgrye/ruygfbryu/gijgnuf',seurl='google.com',country='in',store='False'))

