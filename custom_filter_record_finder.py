import requests, json

client_id = "CLIENT ID"
client_secret = "CLIENT SECRET"
endpoint = "ENDPOINT"
identity_url   = "IDENTITY URL"

bearer_token_request_url = """%s/oauth/token?grant_type=client_credentials&client_id=%s&client_secret=%s""" % (identity_url, client_id, client_secret)

request_token = requests.get(bearer_token_request_url)

request_token_to_json = request_token.json()
access_token = request_token_to_json["access_token"]
state = 'continue'

while state == 'continue':
  if request_token.status_code == 200:

    def input_filter_type():
      print ("\nWhat filter would you like to use (email, twitterId, sATScore)")
      filter_type_input = raw_input("...")
      return filter_type_input

    filter_type = input_filter_type()

    while filter_type not in ["email", "sATScore", "twitterId"]:
      print ("ERROR: Not a valid filter type")
      filter_type = input_filter_type()

    if filter_type == "email":
      print ("\nEnter an %s to search for in Marketo") % filter_type
      filter_input = raw_input("...")

    elif filter_type == "sATScore":
      print ("\nEnter a %s number to search for in Marketo") % filter_type
      filter_input = raw_input("...")

    elif filter_type == "twitterId":
      print ("\nEnter a %s to search for in Marketo") % filter_type
      filter_input = raw_input("...")

    else:
      print ("ERROR: filter type not available")

    url = "%s/v1/leads.json?filterType=%s&filterValues=%s&access_token=%s" % (endpoint, filter_type, filter_input, access_token)

    response = requests.get(url)
    response_json = response.json()
    y = 0

    def print_record_info(y):
      for x in response_json['result']:
          if x['id']:
            print ("\n\tMarketo ID[%i]: %i") % (y, x["id"])
            print ("\tName: %s %s") % (x["firstName"], x["lastName"])
            print ("\t%s: %s") % (filter_type, filter_input)
            y += 1
    
    def print_query_summary(y): 
      for x in response_json['result']:
        if x ['id']:
          y += 1
      
      if y < 1:
        print ('\nThere were no records found with that %s') % filter_type

      elif y == 1:
        print ('\nThere is only 1 record with the %s: "%s"') % (filter_type, filter_input)

      else:
        print ('\nThere are %i records with the %s: "%s"') % (y, filter_type, filter_input)

    print_query_summary(y)
    print_record_info(y)

    print ("\nWhat would you like to do next? \nType 'quit' to exit or 'continue' to run again\n")
    state = raw_input("...")

  else:
    print ("AUTHENTICATION ERROR, CODE:", access_token.status_code)
