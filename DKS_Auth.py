import web, os, hashlib, json
from uuid import getnode as get_mac

conn = web.database(dbn='sqlite', db='DKS_Databases/dks-aurltoken.sqlite')

def auth_required(func):
	def proxyfunc(self, *args, **kw):
		#emailCookie = web.cookies().get('useremail')
		"""
		listdata = json.dumps([emailCookie, web.ctx['ip'], web.ctx.env['HTTP_USER_AGENT'], get_mac()])
		print "%^^^^^^^^^^^^^^^^^^^"
		hashdata = hashlib.sha1(listdata).hexdigest()
		cookiename = "Token-"+ hashdata	
		tokenCookie = web.cookies().get(cookiename)
		if tokenCookie:
			print "$$$$$$$$$$$$$$$$$$$$$$$$$$$@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
			tempvars = dict(emailaddress=emailCookie, tokenurl=tokenCookie, ipaddress=web.ctx['ip'], useragent=pickle.dumps(str(web.ctx.env['HTTP_USER_AGENT'])))
			
			tokencheck = conn.select("tokens", tempvars, where="email = $emailaddress AND token = $tokenurl AND ip = $ipaddress AND useragent = $useragent")
			tokenresults = list(tokencheck)			
			if tokenresults:
				if web.ctx.session["loged"] == True:
					return func(self, *args, **kw)
		"""
		# simplifieds
		if web.ctx.session["loged"] == True:
			return func(self, *args, **kw)
		
		
		raise web.seeother("../login/registerorlogin")

	return proxyfunc



"""
def auth_required(func):
	def proxyfunc(self, *args, **kw):
		try:
			print "1"
			tempvars = dict(tokenurl=web.cookies().get("token"), ipaddress=web.ctx['ip'], useragent=web.ctx.env['HTTP_USER_AGENT'])
			conn.select("tokens", tempvars, where="token = $tokenurl AND ip = $ipaddress AND useragent = $useragent")
			tokenresults = list(tokencheck)			
			print "2"
			if web.ctx.session["loged"] == True:
				print "3"
				if web.cookies().get("token") == web.ctx.session["token"]:
					print "4"
					if tokenresults:
						print "5"
						return func(self, *args, **kw)
			
			elif web.cookies().get("loged") == "True":
				print "6"
				if tokenresults:
					print "7"
					self.session['token'] = tokenresults[0]['token']
					self.session['loged'] = True
					self.session['email'] = tokenresults[0]['email']
					self.session['expiration'] = tokenresults[0]['expiration']
					
					print "8"
					return func(self, *args, **kw)
		except:
			print "9"
			pass
		
		print "10"
		raise web.seeother("../login/registerorlogin")
	return proxyfunc

"" "
			#print "trying"
			#print web.ctx.session["token"], web.cookies().get("token"), web.ctx.session["loged"]
			#if web.ctx.session["token"] == web.cookies().get("token"):
			#	#print "1"
			#	if str(web.ctx.session["loged"]) == str("True"): # user is logged in
			#		#print "2"
			#		if str(web.cookies().get("loged")) == str("True"):
			#			#print "3"
			#			return func(self, *args, **kw)
			#			#print "4"
def subscription_required(func):
	
	def proxyfunc(self, *args, **kw):
		
		try:
			
			# stuff for logging in
			
		except:
			pass
			
		raise web.seeother("../subscriptions")
		
	return proxyfunc


def auth_required(func):
	def proxyfunc(self, *args, **kw):
		try:
			if web.ctx.session["loged"] == True:
				# stuff for logging in
				return func(self, *args, **kw)
		except:
			pass
			
		raise web.seeother("../subscriptions")
		
	return proxyfunc


"""
