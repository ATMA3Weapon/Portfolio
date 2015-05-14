import web
import sqlite3
import re
import mechanize
import cookielib
from bs4 import BeautifulSoup


# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def scrape_amazon(url):
	
	if "amazon.com" not in url: return "Error: Must use an amazon.com URL."

	r = br.open(url)  #'http://www.amazon.com/Carlson-0930PW-Extra-Wide-Walk-Thru-White/dp/B000JJDI0G/ref=sr_1_1?ie=UTF8&qid=1395809917&sr=8-1&keywords=B000JJDI0G')
	html = r.read()

	soup = BeautifulSoup(html, "html5lib")

#	print soup

	productname =  soup.find("h1", {"id": "title"}) #.span.text
	prodname = productname.span.text
	
	bucketli = soup.find("td", {"class": "bucket"}) #.div.ul
	info = bucketli.find_all("li")
	
	print info[0]
	
	#bucketli = bucketli.div.ul
	#print dir(bucketli)

	#info = bucketli.findall("li")
	

	#demen1removed = info[0].b.extract()
	#demensions = info[0].text

	#weight1removed = info[1].b.extract()
	#weight2removed = info[1].a.extract()
	#weight = str(info[1].text).strip("()")

	#ansi1removed = info[4].b.extract()
	#ansi = info[4].text

	#stockfind = soup.find("div", {"id": "availability"})
	#inventory = stockfind.span.text

	#namefind = soup.find("span", {"id": "productTitle"})
	#name = namefind.text

	#findlistprice = soup.find("td", {"class": "a-span12 a-color-secondary a-size-base a-text-strike"})
	#listprice = findlistprice.text

	#findsaleprice = soup.find("span", {"id": "priceblock_ourprice"})
	#saleprice = findsaleprice.text

	#finddescription = soup.find("div", {"class": "aplus"})
	#description = finddescription.p.text
	
	#findseller = soup.find("div", {"id": "merchant-info"})
	#sellerinfo = findseller.text
	
	#findimage = soup.find("img", {"id": "landingImage"})
	#imageurl = findimage['src']

	#producturl = r.geturl()

	return "Success"

scrape_amazon("http://www.amazon.com/Meow-Mix-Indoor-Formula-14-2-Pound/dp/B000M5U6CU/")
