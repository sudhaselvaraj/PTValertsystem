__author__ = 'sudhaselvaraj'

import hmac
import binascii
import json
import csv

from hashlib import sha1
from slackclient import SlackClient
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


#Slack Api Token
token = "xoxp-215257861361-215791929762-217466879622-45e401e4abd5cfd5d55ea714ba205fe4"

def getUrl(request):
    #PTV timetable api- developer id
    devId = 3000326
    #PTV timetable api- key
    key = '870a825e-8577-4bd5-ae3b-7f91abfde88d'

    request = request + ('&' if ('?' in request) else '?')
    raw = request+'devid={0}'.format(devId)
    hashed = hmac.new(key, raw, sha1)
    #Signature has to be appended  with URL to access PTV API
    signature = hashed.hexdigest()
    return 'http://timetableapi.ptv.vic.gov.au'+raw+'&signature={1}'.format(devId, signature)


url = getUrl('/v3/disruptions?route_types=metro-train')
response = urlopen(url)
data = response.read().decode("utf-8")
#PTV timetable Json data
ptv_timetable = json.loads(data)

#Slack Client to post messages
sc = SlackClient(token)

#Open CSV file that has information about disruption alert details
f = open('/Users/sudhaselvaraj/Desktop/ptvalert.csv','rb')
alert_list = csv.reader(f)

for route in ptv_timetable['disruptions']['metro_train']:
    if route['disruption_status'] == 'Current':
        for route_info in route['routes']:
            for alert in alert_list:
                if route_info['route_name'] == alert[1]:
                    #Post alert to the corresponding person
                    sc.api_call("chat.postMessage", channel="{}{}".format('@',alert[0]), text=route['description'], username='sudhaselvaraj')