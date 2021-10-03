import requests
import time
import sys
import os
import json
from PySide2 import QtWidgets, QtGui
from multiprocessing import Process
import shutil

importantinfo = json.load(open('importantinfo.json', 'r'))

spotify_user_id = importantinfo["user_id"]
refresh_token = importantinfo["refresh_token"]
base_64 = importantinfo["base_64"]
sleeptime = 1

PIDFILE = 'isrunning.pid'

def now_playing():
    global response_json
    query = "https://api.spotify.com/v1/me/player/currently-playing"
    response = requests.get(query, headers={"Content-Type": "application/json",
                                            "Authorization": "Bearer {}".format(token)})
    response_json = response.json()
    print(response)
    
def is_running():
    try:
        with open(PIDFILE) as f:
            pid = int(next(f))
        return os.kill(pid, 0)
    except Exception:
        return False

def refresh():
    global token
    query = "https://accounts.spotify.com/api/token"

    response = requests.post(query,
                            data={"grant_type": "refresh_token",
                                   "refresh_token": refresh_token},
                            headers={"Authorization": "Basic " + base_64})

    token = response.json()['access_token']
    print("token refreshed")

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip("spotify webapi thing")
        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
       
        if reason == self.DoubleClick:
            print("Exiting")
            sys.exit(app.exec_())

app = QtWidgets.QApplication(sys.argv)
w = QtWidgets.QWidget()
tray_icon = SystemTrayIcon(QtGui.QIcon("icon.png"), w)

def main_loop():
    refresh()
    refreshtimer = 1
    image2 = ""
    while True:
        try:
            time.sleep(sleeptime)

            if(refreshtimer == 300/sleeptime):
                refresh()
                refreshtimer = 1
            refreshtimer = refreshtimer + 1
            
            now_playing()
            image = (response_json['item']['album']['images'][0]['url'])       #grabs image url

            album = (response_json['item']['album']['name'])                   #grabs album name

            song_name = (response_json['item']['name'])                        #grabs song name

            progress = ((response_json['progress_ms'])/60000)                  #progress in mins

            length = ((response_json['item']['duration_ms'])/60000)            #grab time in mins

            artists = []                                                       #grab artist's names
            for name in response_json['item']['artists']:
                artists.append(name['name'])

            info = {
                "image": image ,
                "album": album,
                "song_name": song_name, 
                "progress": progress,  
                "length": length, 
                "artists": ", ".join(artists)
                }
            jsonString = json.dumps(info, ensure_ascii=True, indent=0)

            #print(valid_jonson)

            if(image2 != image):
                
                r = requests.get(image, stream = True)

                if(r.status_code == 200):
                    r.raw.decode_content = True

                    with open("DownloadFile\cover.png",'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                        image2 = image



            log_file = open("output","w")

            sys.stdout = log_file

            print(jsonString)

            sys.stdout = sys.__stdout__

            log_file.close()

            if(b.is_alive() != False):
                sys.exit()
    
        except:
            if(refreshtimer == 300/sleeptime):
                refresh()
                refreshtimer = 1
            refreshtimer = refreshtimer + 1
            pass

def quit_thing():
    tray_icon.show()
    if is_running():
        sys.exit()
    with open(PIDFILE, 'w') as f:
        f.write(f'{os.getpid()}\n')
    app.exec_()

if __name__ == '__main__':

    a = Process(target=main_loop)
    b = Process(target=quit_thing)
    b.start()
    a.start()
    b.join()
    a.terminate()