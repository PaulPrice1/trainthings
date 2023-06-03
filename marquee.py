import http.client, urllib.request, urllib.parse, urllib.error, base64,json,termcolor
from termcolor import colored,cprint
headers = {
    # Request headers
    'api_key': '{putyourkeyhere}',
}

params = urllib.parse.urlencode({

})
stations=json.load(open("stationlist.json"))
stationdict={}

for station in stations['Stations']:
    stationdict[station["Code"]]=station["Name"]

try:
    conn = http.client.HTTPSConnection('api.wmata.com')
    conn.request("GET", "/StationPrediction.svc/json/GetPrediction/B08?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    info=[i for i in json.loads(data)["Trains"] if i["Group"]=='2']
    print(info[0]["LocationName"])
    print("LN CAR DEST MIN" )
    for thing in info:
        text=colored(thing["Line"],{"BL":"blue","YL":"yellow","RD":"red","GR":'green'}[thing["Line"]])+" "+colored(thing["Car"],{'8':'green','6':'yellow',"-":'red'}[thing["Car"]])+" "+colored(thing["DestinationName"],{"BL":"blue","YL":"yellow","RD":"red"}[thing["Line"]])+" "
        text+=colored(thing["Min"],dict(zip([str(i) for i in range(1,60)]+["---"]+["ARR","BRD"]+[''],['yellow' for i in range(1,61)]+['red' for i in range(2)]+['blue']))[thing["Min"]])
        print(text)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
