import pygame,sys,json,pickle,http.client, urllib.request, urllib.parse, urllib.error, base64,json,time
from PIL import Image
from pygame.locals import *
from winsound import Beep
g=pickle.load(open("goend1.obj","rb"))
colors={'OR':(255,128,0), 'RD':(255,0,0), 'BL':(0,0,255), 'GR':(0,255,0), 'SV':tuple(255 for i in range(3)), 'YL':(255,255,0)}

headers = {
    # Request headers
    'api_key': '{your api key here}',
}
coords=pickle.load(open("goend1.obj","rb"))
pygame.init()
screen=pygame.display.set_mode(Image.open('Systemmap.png').size,RESIZABLE)
truesize=Image.open("Systemmap.png").size
map=pygame.image.load("Systemmap.png")
screen.blit(map,(0,0))
pygame.display.update()

try:
    conn = http.client.HTTPSConnection('api.wmata.com')
    conn.request("GET", "/TrainPositions/TrainPositions?contentType=json", "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
trainpositions=json.loads(data)["TrainPositions"]
print(time.ctime())
for position in trainpositions:
 if position["CircuitId"] in coords.keys() and position["LineCode"] in colors.keys():
    pygame.draw.circle(screen,colors[position["LineCode"]],tuple(g[position["CircuitId"]][i]*(screen.get_rect().size[i]/truesize[i]) for i in range(2)),6)
    pygame.display.update()
screensize=screen.get_rect().size  
starttime=time.time()
while True:
    #if screen has been resized, update image before next api call
    if screensize!=screen.get_rect().size:
        map=pygame.transform.scale(pygame.image.load("Systemmap.png"),screen.get_rect().size)
        screen.blit(map,(0,0))
        for position in trainpositions:
            #check if the current CircuitId is referenced in goend1.obj and if the train has an associated line color
            if position["CircuitId"] in coords.keys() and position["LineCode"] in colors.keys():
                #if so, draw a circle of the appropriate color at the appropriate coordinates
                pygame.draw.circle(screen,colors[position["LineCode"]],tuple(g[position["CircuitId"]][i]*(screen.get_rect().size[i]/truesize[i]) for i in range(2)),6)
    pygame.display.update()
    #get screensize
    screensize=screen.get_rect().size
    #request every 10 seconds
    if time.time()-starttime>=10:
        try:
            conn = http.client.HTTPSConnection('api.wmata.com')
            conn.request("GET", "/TrainPositions/TrainPositions?contentType=json", "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        trainpositions=json.loads(data)["TrainPositions"]
        print(time.ctime())
        for position in trainpositions:
            #check if the current CircuitId is referenced in goend1.obj and if the train has an associated line color
            if position["CircuitId"] in coords.keys() and position["LineCode"] in colors.keys():
                #if so, draw a circle of the appropriate color at the appropriate coordinates
                pygame.draw.circle(screen,colors[position["LineCode"]],tuple(g[position["CircuitId"]][i]*(screen.get_rect().size[i]/truesize[i]) for i in range(2)),6)
                pygame.display.update()
        #get the current time
        starttime=time.time()

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
