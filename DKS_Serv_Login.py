import web, os, json
from web.wsgiserver import CherryPyWSGIServer
from DKS_AURLToken.aurltoken import CreateAURLToken
from validate_email import validate_email
import DKS_Functions

render = web.template.render('DKS_html/', base='layout')
conn = web.database(dbn='sqlite', db='DKS_Databases/dks-login.sqlite')	
conn.appreg = web.database(dbn='sqlite', db='DKS_Databases/dks-regsubscript.sqlite')	


urls = (
	'/?', 'login_program',
	'/external/.*', 'external_login_program',
)

class login_program:
	def __init__(self):
		self.session = web.ctx.session
		
	def GET(self):
		return render.login_index()

	def POST(self):
		uri = web.input()

		emailaddress = str(uri.email) #web.input(name="email")['email']
		
		is_valid = validate_email(emailaddress)
		
		if is_valid:
			tempvars = dict(emailcheck=emailaddress)
			selectemails = conn.select("users", tempvars, where="email = $emailcheck")
			emailresults = list(selectemails)
			
			if not emailresults: # something came up
				conn.insert("users", email=emailaddress)

			# EMAIL USER THEIR ID LOGIN
		
			newtoken = CreateAURLToken(emailaddress, DKS_Functions.GetUserIPv4(), DKS_Functions.GetUserAgent(), "home", 30)

			return render.login_donecheck()
		return False


class external_login_program:
	def __init__(self):
		self.session = web.ctx.session

	def GET(self):
		return render.login_regorlogin()
		
		
	# External Login Page
	#def POST(self):
	def POST(self):
		# procecss for this:
		# when a post response comes in we check if their registration id# exists,
		# we then check the forwarded finger print data to check if this is correct.
		#
		#
		
		
		################## NEED STUFF TO CHECK IT UP #################################
		
		_POST = web.input()
		#uri = web.input()

		appidscrubed = _POST['app-regid']

		tempvars = dict(appid=appidscrubed)
		appselect = conn.appreg.select("registeredApplications", tempvars, where="appid = $appid")
		applist = list(appselect)
	
		appip = str(applist[0]['host'])
		host = str(_POST['server-host'])
		
		if _POST['server-host'] == appip:

			emailaddress = str(_POST['client-email']) #web.input(name="email")['email']
			
			is_valid = validate_email(emailaddress)
			
			if is_valid:
				tempvars = dict(emailcheck=emailaddress)
				selectemails = conn.select("users", tempvars, where="email = $emailcheck")
				emailresults = list(selectemails)
				
				if not emailresults: # something came up
					conn.insert("users", email=emailaddress)
			
			
			
			newtoken = CreateAURLToken(emailaddress, DKS_Functions.GetUserIPv4(), [DKS_Functions.GetUserAgent(), _POST['client-user-agent']], host, 30)
	
	
			# EMAIL USER THEIR ID LOGIN
			
			
			web.header('Content-Type', 'application/json')
	
			return render.login_donecheck() #json.dumps({"logged": True, "email": emailaddress, "regid": _POST['regid']}) #render.login_donecheck()
			
		#return "390jmoglv"
		return False 


app_login = web.application(urls, locals())  
