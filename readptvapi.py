__author__ = 'sudhaselvaraj'

import hmac
import json
import csv


from hashlib import sha1

# pip install slackclient to install SlackClient library
from slackclient import SlackClient
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


def test_slack(sc):
    # use for debugging
    print("Testing API")
    print(80 * "=")
    sc.api_call("api.test")
    print (sc.api_call("api.test"))

def getUrl(request):
    #PTV timetable api- developer id
    devId = 3000326
    #PTV timetable api- key
    key = '870a825e-8577-4bd5-ae3b-7f91abfde88d'

    request = request + ('&' if ('?' in request) else '?')
    raw = request+'devid={0}'.format(devId)
    hashed = hmac.new(key, raw, sha1)
    #Signature has to be appended  with the URL to access PTV API
    signature = hashed.hexdigest()
    return 'http://timetableapi.ptv.vic.gov.au'+raw+'&signature={1}'.format(devId, signature)

def read_ptv_alert_CSV():
    #Open CSV file that has information about disruption alert details
    f = open('/Users/sudhaselvaraj/Desktop/ptvalert.csv','r')
    alert_list = csv.reader(f)
    alert_list = {rows[1].strip():rows[0].strip() for rows in alert_list}
    return alert_list

def sc_post_message(sc, data):
     #PTV timetable Json data
    ptv_timetable = json.loads(data)
    alert_list = read_ptv_alert_CSV()
    for route in ptv_timetable['disruptions']['metro_train']:
        if route and route['disruption_status'] == 'Current':
            if len(route['routes'])>1:
                for route_info in route['routes']:
                    if alert_list.has_key(route_info['route_name']):
                        sc.api_call("chat.postMessage", channel="{}{}".format('@', alert_list[route_info['route_name']]), text="{}: {}".format(route_info['route_name'], route['description'].encode('utf-8')), username='sudhaselvaraj587')
            elif len(route['routes']) == 1:
                print alert_list.has_key(route['routes'][0]['route_name'])
                if alert_list.has_key(route['routes'][0]['route_name']):
                    sc.api_call("chat.postMessage", channel="{}{}".format('@', alert_list[route['routes'][0]['route_name']]), text="{}: {}".format(route['routes'][0]['route_name'], route['description'].encode('utf-8')), username='sudhaselvaraj587')
            else:
                sc.api_call("chat.postMessage", channel="#alert", text=route['title'], username='sudhaselvaraj587')

def main():
    #Slack Api Token
    token = "xoxp-215257861361-215791929762-220219682147-66d629875c686e1c33094f1182474f94"
    # connect to Slack
    sc = SlackClient(token)
    #Test Slack client
    test_slack(sc)
    #PTV metro train timetable API URL
    url = getUrl('/v3/disruptions?route_types=metro-train')
    response = urlopen(url)
    data = response.read().decode("utf-8")
    sc_post_message(sc, data)

main()
