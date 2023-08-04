import http.client, urllib.request, urllib.parse, urllib.error, base64,json,pygame,sys,time
from pygame.locals import *
pygame.init()
screen=pygame.display.set_mode((200,300))
Font=pygame.font.Font("freesansbold.ttf",16)
text=Font.render("Test",True,tuple(255 for i in range(3)),tuple(0 for i in range(3)))
colors={'OR':(255,128,0), 'RD':(255,0,0), 'BL':(0,0,255), 'GR':(0,255,0), 'SV':tuple(255 for i in range(3)), 'YL':(255,255,0),"No":tuple(128 for i in range(3)),None:tuple(128 for i in range(3))}
headers = {
    # Request headers
    'api_key': '{put your key here}',
}
params = urllib.parse.urlencode({

})
stations=json.load(open("stationlist.json"))

stationdict={}
[stationdict.__setitem__(station["Code"],station["Name"]) for station in stations["Stations"]]
timedict={str(i):i for i in range(1,61)}
#trains that are boarding or arriving are in the station and will be treated as 0 minutes away
timedict["ARR"]=0
timedict["BRD"]=0
#we do not know when this train is coming and will treat it as 1000 minutes i.e. the longest time
timedict[""]=1000

try:
    conn = http.client.HTTPSConnection('api.wmata.com')
    conn.request("GET", "/StationPrediction.svc/json/GetPrediction/C08?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    info=[i for i in json.loads(data)["Trains"]]
    print(info[0]["LocationName"])
    print("LN CAR DEST MIN" )
    conn.close()
    print(info)
    pygame.display.set_caption(info[0]["LocationName"])
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
starttime=time.time()
nextcheck=time.time()+min([timedict[thing["Min"]] for thing in info if thing["Min"] in timedict.keys()])*60
timecolors=lambda x: (255,255,0) if x not in ("BRD","ARR") else (255,0,0)
while True:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            quit()
            sys.exit()
    if time.time()>=nextcheck:
        print("Prepping API call")
        #current time for measuring durations
        starttime=time.time()
        #get the greatest of either the closest train or 30 seconds from now
        nextcheck=time.time()+max(min([timedict[thing["Min"]] for thing in info if thing["Min"] in timedict.keys()])*60,30)
        #print the time of the next api call, this is to make sure that no rate limits are being exceeded
        print(f"next call at {time.ctime(nextcheck)}")
        
        
        try:
            conn = http.client.HTTPSConnection('api.wmata.com')
            conn.request("GET", "/StationPrediction.svc/json/GetPrediction/C08?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            info=[i for i in json.loads(data)["Trains"]]
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
    else:
        #if a minute has passed, advance the time
        if time.time()-starttime>=60:
            if all([thing["Min"] in [str(i) for i in range(2,61)] for thing in info if thing["Min"] in timedict.keys()]):
                [thing.__setitem__("Min",str(timedict[thing.get("Min")]-1)) for thing in info]
                #reset time for counting minutes to present
                starttime=time.time()
            
        height=10
        width=0
        screen.fill((0,0,0))
        text=Font.render("LN",True,(255,0,0),tuple(0 for i in range(3)))
        textRect=text.get_rect()
        textRect.center=(textRect[2]//2,height)
        screen.blit(text,textRect)
        width+=textRect[2]
        text=Font.render("CAR",True,(255,0,0),tuple(0 for i in range(3)))
        textRect=text.get_rect()
        textRect.center=(width+textRect[2]//2+10,height)
        screen.blit(text,textRect)
        width+=textRect[2]+10
        text=Font.render("DEST",True,(255,0,0),tuple(0 for i in range(3)))
        textRect=text.get_rect()
        textRect.center=(width+textRect[2]//2+20,height)
        screen.blit(text,textRect)
        width+=textRect[2]+10
        text=Font.render("MIN",True,(255,0,0),tuple(0 for i in range(3)))
        textRect.center=(210-textRect[2]//2,height)
        screen.blit(text,textRect)
        height+=16
        for thing in info:
                width=0
                if thing["Line"] in colors.keys():
                    #text box rectangle width was not corresponding to the width of the visible textbox.
                    text=Font.render(f"{thing['Line']}",True,colors[thing["Line"]],tuple(0 for i in range(3)))
                    textRect=text.get_rect()
                    textRect.center=(textRect[2]//2,height)
                    screen.blit(text,textRect)
                    width+=textRect[2]+10
                    text=Font.render(f"{thing['Car']}",True,colors[thing["Line"]],tuple(0 for i in range(3)))
                    width+=textRect[2]+10
                    textRect.center=(width+textRect[2]//2-4,height)
                    screen.blit(text,textRect)
                    width+=textRect[2]
                    text=Font.render(f"{thing['Destination']}",True,colors[thing["Line"]],tuple(0 for i in range(3)))
                    textRect=text.get_rect()
                    textRect.center=(width+textRect[2]/2,height)
                    screen.blit(text,textRect)
                    text=Font.render(f"{thing['Min']}",True,timecolors(thing["Min"]),tuple(0 for i in range(3)))
                    textRect=text.get_rect()
                    textRect.center=(200-textRect[2]//2,height)
                    screen.blit(text,textRect)
                height+=16

        pygame.display.update()
