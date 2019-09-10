#!/usr/bin/env python3

# import httplib2
import json
from sys import exit
import requests

####-- set up the URL parm variables

base_url = 'http://test.dmtclearinghouse.esipfed.bluedotapps.org/api/dmt/search'
#
login_data = {
    'username': 'api.persona',
    'password': 'api.persona'}

'''--- varName changed to headerString so that parameterName
			 and variable name are not the same---JCP '''

headerString = {'Content-type': 'application/json'}

print()
####-- logging in

r = requests.post(url = base_url+ '/user/login', headers = headerString, data = json.dumps(login_data) )
print('loginStatusCode: '+str(r.status_code))

'''--- saw evidence of a cookie in the response back from your original code:
					http = httplib2.Http()
					response, json_content = http.request(base_url + '/user/login',
					'POST',
					headers=headers,
					body=json.dumps(login_data)
					)
					print(response)
					
				so I guessed that cookies might be why David's instructions 
				worked in FireFox but not for you in python 
	
	note: I used this page for docs on cookies:
			http://docs.python-requests.org/en/latest/api/#requests.Response
	where I learned two things:
		1/ response can include a cookies object
		2/ parms for requests accept cookiesObject on the "send" side of the process
 ---JCP '''
print('loginText: \n'+r.text)
print('loginCookies: \n'+str(r.cookies) )

'''--- here we store the cookies object that comes back from login ---JCP'''
cookieObj=r.cookies
print()
#sys.exit()

####-- get a token

'''--- and here we send cookiesObject along with our request for token ---JCP'''
r = requests.post(url = base_url+ '/user/token.json', cookies=cookieObj, headers = headerString, data = json.dumps(login_data) )
print( 'tokenStatusCode" '+str(r.status_code))

'''--- as in Firefox, the "text" coming back from the query contains the token ---JCP'''
print( 'tokenText" '+r.text)

'''--- probably a nicer way to clean up the token, but crude worked :-) ---JCP'''
tokenTxt=r.text.replace('{','').replace('}','').replace("token",'').replace('"','').replace(':','')
print( 'cleanedUpToken: '+tokenTxt)
print()
'''--- make a new header string, per instructions for Firefox by David ---JCP'''
headerString = {'X-CSRF-TOKEN' : tokenTxt}

####-- send David's first "search" example

'''--- and here we send cookiesObject, this time with get_query ---JCP'''
get_query = requests.get(base_url+'/search_api/search_index_dmt_clearinghouse.json', cookies=cookieObj, headers = headerString)
print( 'getQueryStatusCode: '+str(get_query.status_code) )
print()
'''--- and a reponse that looks like what came back in Firefox pops out here ---JCP'''
print( 'getQueryText: \n'+get_query.text)
print()

'''--- In a live situation, one would likely have a person "login"
			after which the various search--response iteration(s) 
			during a "session" would use the same cookiesObject and token

			In this code snippet environment, each pass thru the code
			gets a new cookie and a new token 
			
			That in constract to when I was testing
			using Firefox's RESTer per David's outline, where the "login" step
			failed after the first time I started testing (cuz the browser
			stored the cookie and every time I asked for a "token" I
			got the same token) ... which token in conjuction with the browser
			stored cookieObj let me run all of David's examples successfully
			in Firefox
			
			Hope that makes sense.
			
			[BTW: <flame> I really hate cookies :-(  </flame>]
---'''				
				


exit()
