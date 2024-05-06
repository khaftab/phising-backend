from bs4 import BeautifulSoup
import urllib
import urllib.request

url = urllib.parse.quote("vercel.com")
rank = BeautifulSoup(urllib.request.urlopen("https://www.semrush.com/website/google.com/overview/").read(), "html").find("engagement-list__item-value")

print(rank)