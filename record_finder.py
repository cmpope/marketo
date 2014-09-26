#### This file allows you to use the Marketo Leads API to check if a record 
#### exists in the datbase by searching for email address.  If multiple records
#### exist with the same email address, the program will return the count of 
#### the duplicate records existing in the system.

import requests, json

### --- INSERT MARKETO API CREDENTIALS HERE --- ####
client_id = "INSERT CLIENT ID HERE"
client_secret = "INSERT CLIENT SECRET HERE"
endpoint = "INSERT ENDPOINT HERE"
identity_url   = "INSERT IDENTITY URL HERE"

bearer_token_request_url = """%s/oauth/token?grant_type=client_credentials&client_id=%s&client_secret=%s""" % (identity_url, client_id, client_secret)

request_token = requests.get(bearer_token_request_url)

request_token_to_json = request_token.json()
access_token = request_token_to_json["access_token"]
state = 'continue'

while state == 'continue':
  if request_token.status_code == 200:
    print ("\nEnter an email address to search for in Marketo\n")
    email_input = raw_input("...")

    url = "%s/v1/leads.json?filterType=email&filterValues=%s&access_token=%s" % (endpoint, email_input, access_token)

    response = requests.get(url)
    response_json = response.json()
    y = 0

    for x in response_json['result']:
        if x['id']:
          print ("\nID[%i]: %i") % (y, x["id"])
          y += 1

    if y < 1:
      print ('\nThere were no records found with that email address')

    elif y == 1:
      print ('\nThere is only 1 record with the email address %s') % email_input

    else:
      print ('\nThere are %i records with that email address %s') % (y, email_input)

    print ("\nWhat would you like to do next? \nType 'quit' to exit or 'continue' to run again\n")
    state = raw_input("...")

  else:
    print (access_token.status_code)
