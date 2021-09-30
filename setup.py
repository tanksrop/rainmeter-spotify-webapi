import base64
import json
import webbrowser
import requests
import sys
import json
import re

def b64():
    global base_64
    idsecret = client_id + ":" + client_secret
    tobe_encoded = idsecret.encode('ascii')
    encoded = base64.b64encode(tobe_encoded)
    output = encoded.decode()
    base_64 = output

def auth():
        global refresh_token
        query = "https://accounts.spotify.com/api/token"

        response = requests.post(query,
                                data={"grant_type": "authorization_code",
                                       "code": code,
                                       "redirect_uri": "https://127.0.0.1/"},
                                headers={"Authorization": "Basic " + base_64})

        refresh_token = response.json()['refresh_token']


print("head over to https://developer.spotify.com/dashboard/applications and make an app")
print("then to click edit settings and put 'https://127.0.0.1/' as a redirect url on your app's dashboard")
print("then click save")
input("press enter to continue")

linktoprofile = input("Enter link to your profile : ")

linktoprofile2 = re.sub("\?si=.*","", linktoprofile)
user_id = re.sub("https:\/\/open.spotify.com\/user\/","", linktoprofile2)

client_id = input("Enter Client ID : ")

client_secret = input("Enter client secret : ")

b64()

authurl = ("https://accounts.spotify.com/authorize?client_id=" + client_id + "&response_type=code&redirect_uri=https%3A%2F%2F127.0.0.1%2F&scope=user-read-playback-state")

webbrowser.open(authurl, new=2)

code = input("Enter the entire url after loggin in : ")

code = re.sub("https:\/\/127.0.0.1\/\?code=", "", code)

auth()

user_info = {"client_id":client_id, "client_secret": client_secret, "base_64":base_64, "refresh_token":refresh_token, "user_id":user_id}

jsonString = json.dumps(user_info, indent=0)
valid_jonson = json.loads(jsonString)

log_file = open("importantinfo.json","w")
sys.stdout = log_file
print(jsonString)
sys.stdout = sys.__stdout__
log_file.close()

print("Setup Complete")
input("press enter to exit")