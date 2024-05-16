# -*- coding: utf-8 -*-
"""Feature extraction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/185Zs6R9J7QLdacOZeb6VmQcRZukpic0t
"""

# importing required packages for this section
from urllib.parse import urlparse,urlencode
import ipaddress
import re

def havingIP(url):
  try:
    ipaddress.ip_address(url)
    ip = 1
  except:
    ip = 0
  return ip

def haveAtSign(url):
  if "@" in url:
    at = 1
  else:
    at = 0
  return at

def getLength(url):
    # Remove common prefixes
    prefixes = ['http://', 'https://']
    for prefix in prefixes:
        if url.startswith(prefix):
            url = url[len(prefix):]

    # Remove 'www.' if present
    url = url.replace('www.', '')

    # Return the length of the remaining URL
    if len(url) < 54:
      length = 0
    else:
      length = 1
    return length


def getDepth(url):
  s = urlparse(url).path.split('/')
  depth = 0
  for j in range(len(s)):
    if len(s[j]) != 0:
      depth = depth+1
  return depth


def redirection(url):
  pos = url.rfind('//')
  if pos > 6:
    if pos > 7:
      return 1
    else:
      return 0
  else:
    return 0


def httpDomain(url):
  domain = urlparse(url).netloc
  if 'https' in domain:
    return 1
  else:
    return 0


def secureHttp(url):
    return int(urlparse(url).scheme == 'https')

shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

# 8. Checking for Shortening Services in URL (Tiny_URL)
def tinyURL(url):
    match=re.search(shortening_services,url)
    if match:
        return 1
    else:
        return 0


# 9.Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1            # phishing
    else:
        return 0            # legitimate


import re
# !pip install python-whois
# !pip install tldextract
import whois
import urllib
import urllib.request
from datetime import datetime
import requests

from datetime import datetime

def domainAge(domain_info):
    try:
        # domain = url.split("//")[-1].split("/")[0]
        # whois_info = whois.whois(domain)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if isinstance(creation_date, datetime):
            now = datetime.now()
            age = now - creation_date
            return age.days
    except Exception as e:
        print(f"Error: {e}")
    return 1


# Subdomains Count:

import tldextract

def subdomainsCount(url):
    extracted = tldextract.extract(url)
    return len(extracted.subdomain.split('.'))


# End Period of Domain


def domainEnd(domain_info):
    try:
        # domain = url.split("//")[-1].split("/")[0]
        # domain_info = whois.whois(domain)
        expiration_date = domain_info.expiration_date

        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        if isinstance(expiration_date, datetime):
            current_time = datetime.now()
            remaining_time = expiration_date - current_time
            remaining_months = remaining_time.days / 30

            if remaining_months < 3:
                return 1  # Phishing
            else:
                return 0  # Legitimate
    except Exception as e:
        print(f"Error: {e}")

    return 1


import requests
from bs4 import BeautifulSoup

def iframe(response):
    if response == "":
        return 1
    try:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            iframes = soup.find_all('iframe')
            for iframe in iframes:
                src = iframe.get('src', '')
                if not src:
                    return 1  # Phishing
                iframe_response = requests.get(src)
                if iframe_response.status_code != 200:
                    return 1  # Phishing
            return 0  # Legitimate
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    return 0  # Return 0 for legitimate URLs by default


def fakeStatusBar(response):
    if response == "":
        return 1
    try:
        if response.status_code == 200:
            if not response.text:  # Check if response is empty
                return 1  # Phishing
            # Search for onmouseover event in the response text
            if re.search(r"onmouseover", response.text):
                return 1  # Phishing
            return 0  # Legitimate
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    return 0  # Return 0 for legitimate URLs by default



def rightClick(response):
    if response == "":
        return 1
    try:
        if response.status_code == 200 and "oncontextmenu" in response.text:
            return 1
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    return 0



def forwarding(response):
  if response == "":
    return 1
  else:
    if len(response.history) <= 2:
      return 0
    else:
      return 1

def addHttpPrefix(domain):
  parts = domain.split('#', 1)
  domain_part = parts[0]
  fragment_part = '#' + parts[1] if len(parts) > 1 else ''

  if domain_part.startswith('http://') or domain_part.startswith('https://'):
      return domain_part + fragment_part
  else:
      return 'http://' + domain_part + fragment_part

def featureExtraction(url):
  url = addHttpPrefix(url)
  features = []
  #Address bar based features (10)
  # features.append(getDomain(url))
  # features.append((url))
  features.append(haveAtSign(url))
  features.append(getLength(url))
  features.append(getDepth(url))
  features.append(redirection(url))
  features.append(httpDomain(url))
  features.append(tinyURL(url))
  features.append(prefixSuffix(url))

  #Domain based features (4)
  dns = 0
  try:
    # domain_name = whois.whois(urlparse(url).netloc)
      domain = url.split("//")[-1].split("/")[0]
      domain_info = whois.whois(domain)
  except:
    dns = 1

  features.append(dns)
  # features.append(web_traffic(url))
  features.append(1 if dns == 1 else domainAge(domain_info))
  features.append(1 if dns == 1 else domainEnd(domain_info))
  features.append(subdomainsCount(url))

  try:
    response = requests.get(url, timeout=60)
    # print(response.status_code)
  except requests.Timeout:
    print("Timeout error: The request timed out")
    response = ""
  except requests.RequestException as e:
    print("Request error:", e)
    response = ""

  features.append(iframe(response))
  features.append(fakeStatusBar(response))
  features.append(rightClick(response))
  features.append(forwarding(response))

  return features

#converting the list to dataframe
feature_names = ['Have_At','URL_Length','URL_Depth','Redirection','Http_In_Domain',
'Tiny_URL','Prefix/Suffix','DNS','Domain_Age','Domain_End','Subdomains_Count','iFrame','Fake_Status_Bar','Right_Click','Forwarding']

# print(featureExtraction('https://google.com/'))

