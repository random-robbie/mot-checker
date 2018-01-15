# Made by Random_Robbie
# DO NOT USE COMMERICALLY THIS IS FOR PERSON USE ONLY
# This uses the UK GOV website to check the vehicle's details.
# It was made as a test.

import requests
import re
import argparse

session = requests.Session()




def grab_details (REG):
	try:
		paramsPost = {"Vrm":REG,"Continue":""}
		headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0","Referer":"https://vehicleenquiry.service.gov.uk/","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate","Content-Type":"application/x-www-form-urlencoded"}
		response = session.post("https://vehicleenquiry.service.gov.uk/ConfirmVehicle", data=paramsPost, headers=headers)
		# Regex to scrape the details
		vmod = re.compile('<span><strong>(.+?)</strong></span>').findall(response.text)[0]
		vcol = re.compile('<span><strong>(.+?)</strong></span>').findall(response.text)[1]
		viewstate = re.compile('name="viewstate" type="hidden" value="(.+?)" /><input id').findall(response.text)[0]
		if "Vehicle details could not be found" in response.text:
			print "You Entered Registration: "+REG+""
			print "It looks like there might of been an error finding it"
			exit();
	
		# Print Reg and Color from confirm page
		print ("Reg: "+REG+"")
		print ("Color:"+vcol+"")
		print ("Make:"+vmod+"")
	except:
		print "Sorry it looks like that registration has not been found"
		print "Please try another registration."
		

	# Submit to 2nd page to grab the details of the MOT and Tax
	paramsPost2 = {"Vrm":REG,"Make":vmod,"viewstate":viewstate,"Continue":"","Correct":"True","Colour":vcol}
	headers2 = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0","Referer":"https://vehicleenquiry.service.gov.uk/ConfirmVehicle","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate","Content-Type":"application/x-www-form-urlencoded"}
	response2 = session.post("https://vehicleenquiry.service.gov.uk/ViewVehicle", data=paramsPost2, headers=headers2)
	
	# Regex to find the  Tax and MOT details.
	if "No MOT</h2>" in response2.text:
		print "This Vehicle has no MOT and current has a SORN registered for it."
		exit();
	if "No details held by DVLA" in response2.text:
		
		print "Road Tax Expires: "+tax+""
		print "MOT: No details held by DVLA"
		exit();
		
	
	tax = re.compile('<strong>Tax due:<br>(.+?)</strong></p>').findall(response2.text)[0]
	mot = re.compile('<strong>Expires:<br>(.+?)</strong></p>').findall(response2.text)[0]
	print "Road Tax Expires: "+tax+""
	print "Mot Expires: "+mot+"" 
	
	


# Instantiate the parser
parser = argparse.ArgumentParser(description='Vehicle Registration')

# Declare arguments
parser.add_argument('-r', '--reg', required=True, help='Vehicle Registration eg: W705 AVC')

# Parse the args
args = parser.parse_args()

if args.reg:
	REG = args.reg
	grab_details (REG)
else:
	print "Please Enter a Registration"
