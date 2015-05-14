# - jobs main loop   - events loop
# - - read database  - database stuff
# - - create loop to read list - database stuff
# - - - check time - db stuff
# - - - yes  - db stuff
# - - - - create thread - thread stuff
# - - - - - scrape URL
# - - - - - Do stuff
# - - - - - set next check 
# - - sleep 
#
#
# endless loop:
# - read database
# - check loop
# - - read row
# - - - check time 
#
#
#
#import sqlite3, os
#
#dbpath = os.path.abspath('../../database/')
#
#conn  = sqlite3.connect(os.path.join(dbpath, 'DKS-scrapekwik.db'))
#curse = conn.cursor() 

import sqlite3, os, sys, logging, time, datetime, threading, json, random
import mechanize, cookielib
import jobs
import scrape
from collections import OrderedDict


dbpath = os.path.abspath('../../database/')
lgpath = os.path.abspath('../../logging/')

conn  = sqlite3.connect(os.path.join(dbpath, 'DKS-scrapekwik.sqlite'))
curse = conn.cursor()

def nextscrapetime(currenttimestamp, intervalarray): # time.time, dictionary of days of week with lists of times
	currenttimetupple = time.gmtime(currenttimestamp)   #time.localtime() #lets get the current time into a time tuple for working with it
	
	todaysday = time.strftime("%a", currenttimetupple)  # convert the time to the day name
	todaysdate = time.strftime("%Y-%m-%d", currenttimetupple) # convert the time to a year-month-day 
	
	
	# make a time from a string and convert it to the time for our day order 
	day1 = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d").strftime("%a") # today
	day2 = datetime.datetime.strptime(str(datetime.date.today() + datetime.timedelta(days=1)), "%Y-%m-%d").strftime("%a") # now get the next 6 days after.
	day3 = datetime.datetime.strptime(str(datetime.date.today() + datetime.timedelta(days=2)), "%Y-%m-%d").strftime("%a")
	day4 = datetime.datetime.strptime(str(datetime.date.today() + datetime.timedelta(days=3)), "%Y-%m-%d").strftime("%a")
	day5 = datetime.datetime.strptime(str(datetime.date.today() + datetime.timedelta(days=4)), "%Y-%m-%d").strftime("%a")
	day6 = datetime.datetime.strptime(str(datetime.date.today() + datetime.timedelta(days=5)), "%Y-%m-%d").strftime("%a")
	day7 = datetime.datetime.strptime(str(datetime.date.today() + datetime.timedelta(days=6)), "%Y-%m-%d").strftime("%a")

	newinvertvalarraymap =  [day1, day2, day3, day4, day5, day6, day7] # arrange the days in order for a key list
	
	newintervalarray = OrderedDict(sorted(intervalarray.items(), key=lambda i:newinvertvalarraymap.index(i[0]))) # create an ordered dictionary with keys as the day of the week and the value as a list of times and range of times to scrape in.
	
	# we now loop through each day of the week starting with today. 
	# convert each hour of the day into a unix timestamp decimal and find the first time that is larger then the current time 
	for dayofweektoscrape in newintervalarray:
		key = dayofweektoscrape
		val = newintervalarray[dayofweektoscrape] #checkintervallists
		
		daysaway = newinvertvalarraymap.index(key)
		
		for scrapetimes in val:
			timestring_one = str(datetime.date.today() + datetime.timedelta(days=daysaway)) + " " + str(scrapetimes[0])
			timestamp_one = time.mktime(datetime.datetime.strptime(timestring_one, "%Y-%m-%d %I:%M:%S%p").timetuple())
			
			#print timestring_one, currenttimestamp, timestamp_one
			
			if timestamp_one > currenttimestamp: 
				if len(scrapetimes) == 1:
					return timestamp_one
				
				elif len(scrapetimes) == 2:
					timestring_two = str(datetime.date.today() + datetime.timedelta(days=daysaway)) + " " + str(scrapetimes[1])
					timestamp_two = time.mktime(datetime.datetime.strptime(timestring_two, "%Y-%m-%d %I:%M:%S%p").timetuple())
					
					timestamp_range = random.uniform(timestamp_one, timestamp_two)
					
					return timestamp_range

class scrapeThread(threading.Thread):
	def __init__(self, asin, invact, url, profilesite, profilepage, profilexmltemplate):
		logging.info("New Thread Created") # % (asin,)
		print "New thread created."
		#print ("asdfasdf")
		self.asin   = asin
		self.invact = invact
		self.url    = url
		self.profilesite = profilesite
		self.profilepage = profilepage
		self.profilexmltemplate = os.path.join("profiles", profilexmltemplate) 
		
		
		self.dbpath = os.path.abspath('../../database/')

		self.connDropkwik  = sqlite3.connect(os.path.join(self.dbpath, 'DKS-dropkwik.sqlite'))
		self.curseDropkwik = self.connDropkwik.cursor()
		
		self.connScrapekwik  = sqlite3.connect(os.path.join(self.dbpath, 'DKS-scrapekwik.sqlite'))
		self.curseScrapekwik = self.connScrapekwik.cursor()
		
		self.run()
		#asin
		#pageprofile

	def run(self):
		# open a randomly selected browser/operating system mechanize setup and read out the page html.
		#print ("RUNNING")
		# Browser
		self.mechabrowser = mechanize.Browser()
		
		# Cookie Jar
		self.cooklibjar = cookielib.LWPCookieJar()
		self.mechabrowser.set_cookiejar(self.cooklibjar)
		
		# Browser options
		self.mechabrowser.set_handle_equiv(True)
		self.mechabrowser.set_handle_gzip(True)
		self.mechabrowser.set_handle_redirect(True)
		self.mechabrowser.set_handle_referer(True)
		self.mechabrowser.set_handle_robots(False)
	
		#self.mechabrowser.set_debug_http(True)
		self.mechabrowser.set_debug_redirects(True)
	
		# Follows refresh 0 but not hangs on refresh > 0
		self.mechabrowser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

		#	 User-Agent (this is cheating, ok?)
		self.mechabrowser.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 8.0; AOL 9.6; AOLBuild 4340.5002; Windows NT 6.1; WOW64; Trident/4.0; GTB7.3; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; BRI/2; MAGW; InfoPath.3; .NET4.0C)")]

		self.readout = self.mechabrowser.open(self.url)  #("http://www.amazon.com/Meow-Mix-Indoor-Formula-14-2-Pound/dp/B000M5U6CU/ref=sr_1_1?ie=UTF8&qid=1396553928&sr=8-1&keywords=cat+food")

		self.htmloutput = self.readout.read()
	
		self.response = self.mechabrowser.response()  # this is a copy of response
		self.headers = self.response.info()
		self.charset = str(self.headers["Content-Type"]).split("=")[1]

		# SCRAPE THE PAGE!!! WOO
		scrapedoutput = scrape.scrape_by_template_page(self.profilesite, self.profilepage, self.profilexmltemplate, self.charset, self.htmloutput)
		#print scrapedoutput

		if scrapedoutput is not False:
	
			# check the inventory file for either the ASIN or URL if it doesnt exist insert, if one does exist, use it to update.
			self.curseDropkwik.execute("SELECT * FROM products_inventory WHERE asin = ?", (self.asin,))
			self.asinexists = self.curseDropkwik.fetchone()
			
			self.curseDropkwik.execute("SELECT * FROM products_inventory WHERE url = ?", (self.url,))
			self.urlexists = self.curseDropkwik.fetchone()
			

			
			#print asin, url
			
			#print self.asinexists, self.urlexists
			
			if (self.asinexists == None) and (self.urlexists == None):

				asin = scrapedoutput['asin']
				active = False
				url = self.url
				name = scrapedoutput['productname']
				seller = scrapedoutput['seller']
				price_listed = scrapedoutput['price_listed']
				price_sale = scrapedoutput['price_sale']
				price_currency = "USD"
				weight = scrapedoutput['weight']
				dimensions = None #scrapedoutput['dimensions']
				inventory = scrapedoutput['inventory']
				description = scrapedoutput['description']
				image = None #scrapedoutput['image']
					
				#print "INSERT INTO products_inventory (asin, active, url, name, seller, price_listed, price_sale, price_currency, weight, dimensions, inventory, description, image) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (asin, active, url, name, seller, price_listed, price_sale, price_currency, weight, dimensions, inventory, description, image)
				self.curseDropkwik.execute("INSERT INTO products_inventory (asin, active, url, productname, seller, price_listed, price_sale, price_currency, weight, dimensions, inventory, description, image) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (asin, active, url, name, seller, price_listed, price_sale, price_currency, weight, dimensions, inventory, description, image))
				logging.info("Inserted new data")
				print ("Inserted new data")
			
			else:
	
				if self.asinexists is not None: # or self.urlexists:
					logging.info("Inserted data via ANSI")
					print ("Inserted data via ANSI")
					
					# update the rows depending on which ones are wanted to update
					# updates by asin or url
					for key, value in self.invact.iteritems():
						if value == True:
							self.curseDropkwik.execute("UPDATE products_inventory SET "+key+"=? WHERE asin=?", (scrapedoutput[str(key)], self.asin,))
							
					self.curseScrapekwik.execute("SELECT * FROM jobs WHERE asin=?", (self.asin,))
	
					wresult = self.curseScrapekwik.fetchone()
	
					if wresult is not None:
	
						ldk = str(wresult[10])
						self.checkintervals = json.loads(ldk)
					
						self.newtime = time.time()
					
						self.curseScrapekwik.execute("UPDATE jobs SET last_check=? WHERE asin=?", (self.newtime, self.asin,))
						self.nextscrapetag = nextscrapetime(self.newtime, self.checkintervals)
					
						self.curseScrapekwik.execute("UPDATE jobs SET next_check=? WHERE asin=?", (self.nextscrapetag, self.asin,))
					
				elif self.urlexists is not None: # or self.urlexists:
					logging.info("Inserted data via URL")
					print ("Inserted data via URL")
					
					#print scrapedoutput
					
					# update the rows depending on which ones are wanted to update
					# updates by asin or url
					for key, value in self.invact.iteritems():
						if value == True:
							self.curseDropkwik.execute("UPDATE products_inventory SET "+key+"=? WHERE url=?", (scrapedoutput[str(key)], self.url,))
							
					self.curseScrapekwik.execute("SELECT * FROM jobs WHERE url=?", (self.url,))
					
					wresult = self.curseScrapekwik.fetchone()
					if wresult is not None:

						ldk = str(wresult[10])
						self.checkintervals = json.loads(ldk)
						
						self.newtime = time.time()
						
						self.curseScrapekwik.execute("UPDATE jobs SET last_check=? WHERE url=?", (self.newtime, self.url,))
						self.nextscrapetag = nextscrapetime(self.newtime, self.checkintervals)
						self.curseScrapekwik.execute("UPDATE jobs SET next_check=? WHERE url=?", (self.nextscrapetag, self.url,))
			
			logging.info("Commiting data to database")
			print ("Commiting data to database")
			
			self.connDropkwik.commit() # update the database
			self.connDropkwik.close()
			
			self.connScrapekwik.commit()
			self.connScrapekwik.close()

def checktime(timetocheck, currenttime):
	if timetocheck == 1: # a first time check. so we return true to scrape it and set the next scrape time
		return True
	
	else:
		if currenttime > timetocheck:
			return True
	
	return False



def main():
	logging.info("Main Event: Started main event loop")
	print       ("Main Event: Started main event loop")
	
	dbread = curse.execute("SELECT * FROM jobs")
	dbrows = dbread.fetchall()
	for row in dbrows:
		
		if row[1] == u"True": isactive = True
		elif row[1] == u"False": isactive = False
		else: isactive = False

		if isactive == False: # True:
			rowtime = float(row[7])
			thistime = time.time()
			
			if checktime(rowtime, thistime):
				asin = str(row[0])
				invact = json.loads(str(row[4]))
				url  = str(row[5])
				profilesite = str(row[8])
				profilepage = str(row[9])
				profiletemplate = str(row[11])
				
				scrapeThread(asin, invact, url, profilesite, profilepage, profiletemplate)

	logging.info("Main Event: Finished main event loop")
	print       ("Main Event: Finished main event loop")
	time.sleep(100)
	

if __name__ == "__main__":
	logging.basicConfig(filename=os.path.join(lgpath, 'scrapekwik-main.log'), level=logging.INFO, format='%(asctime)s %(message)s')
	
	#sys.stdout = logging
	
	while True: # endless loop
		main()  # main event loop












