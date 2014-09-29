import requests, json

def call_leads_api(request_body):
    client_id = "INSERT CLIENT SECRET HERE"
    client_secret = "INSERT CLIENT SECRET HERE"
    endpoint = "INSERT ENDPOINT HERE"
    identity_url   = "INSERT IDENTITY URL HERE"

    bearer_token_request_url = """%s/oauth/token?grant_type=client_credentials&client_id=%s&client_secret=%s""" % (identity_url, client_id, client_secret)

    request_token = requests.get(bearer_token_request_url)

    request_token_to_json = request_token.json()
    access_token = request_token_to_json["access_token"]

    post_url = ("%s/v1/leads.json?access_token=%s") % (endpoint, access_token)
    r = requests.post(post_url, data=request_body, headers={"content-type":"application/json"})

    print (r.text)
    return r.text

#### --- JSON BODY OPTIONS --- ####
action = "createOrUpdate"
#createOnly, updateOnly, createOrUpdate, createDuplicate

lookupField = "Email"
#(ex. id, email, cookie, custom field)

lead_info = {}

def get_lead_info():

    print ("Enter the first name:")
    lead_info_first = raw_input('...')
    lead_info["FirstName"] = lead_info_first

    print ("Enter the last name:")
    lead_info_last = raw_input('...')
    lead_info["LastName"] = lead_info_last

    print ("Enter the email address:")
    lead_info_email = raw_input('...')
    print ("%s\n") % lead_info_email
    lead_info["email"] = lead_info_email

    print ("Enter the phone number:")
    lead_info_phone = raw_input("...")
    lead_info["Phone"] = lead_info_phone

    return lead_info

get_lead_info()
lead_info_str = str(lead_info)
lead_info_str = lead_info_str.replace("'",'"')
lead_info_str = lead_info_str.replace(" ", "")

call_input = '{"action":"%s","lookupField":"%s","input":[%s]}' % (action, lookupField, lead_info_str)
call = call_leads_api(call_input)


