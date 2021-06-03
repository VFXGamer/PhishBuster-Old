from urllib.parse import urlparse
import re
import tldextract

def url_syntax(url_changes):
    url_search_http = re.search("http", url_changes)
    if url_search_http == None:
        url_http = "http://" + url_changes
    else:
        url_http = url_changes
    return url_http # Returns the url with 'http://' if not there in the input url

def subdomain_re(domain_url):
    sub_addr = tldextract.extract(domain_url).subdomain
    if sub_addr != None:  
        extract_domain = tldextract.extract(domain_url).domain
        extract_ext = tldextract.extract(domain_url).suffix
        filtered_sub = extract_domain + '.' + extract_ext
    else:
        filtered_sub = domain_url
    return filtered_sub # Removes subdomain and returns the value

def phishbuster_url(url_input): # removes ~@ (which are used for disgusing the url) and path
    corrected_url = url_syntax(url_input)
    url_search = re.search("~@", corrected_url)
    if url_search != None:
        domain = urlparse(corrected_url).netloc
        remove_to_hide_element = re.split("~@", domain)
        domain_url = remove_to_hide_element[1]
    else:
        domain = urlparse(corrected_url).netloc
        domain_url = domain
    return domain_url # returns a domain name eg. google.com / with sub domain www.google.com

def comparing_url(url_phish,url_org):
    input_url = phishbuster_url(url_phish)
    final_url = subdomain_re(input_url)
    if final_url == url_org:
        output_comparison = bool(False) # Returns False
    else:
        output_comparison = bool(True) # Returns True
    return output_comparison
    

if __name__ == "__main__":
    print(comparing_url('https://www.microsoft.com~@www.google.com/wsgrye/ruygfbryu/gijgnuf','google.com'))
