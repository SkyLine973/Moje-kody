import requests
from requests.auth import HTTPBasicAuth
import time


auth=HTTPBasicAuth(client_id,client_secret)

Token=""

def autoryzacja_user(client_id, auth):
    authUrl = r"https://allegro.pl/auth/oauth/device"
    data={"Accept": r"application/vnd.allegro.public.v1+json", "client_id":client_id}
    r=requests.post(url=authUrl, auth=auth, data=data)
    device=r.json()
    print(device)
    device_code=device["device_code"]
    time.sleep(20)
    token=r"https://allegro.pl/auth/oauth/token?grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Adevice_code&device_code={}".format(device_code)
    r=requests.post(url=token, auth=auth)
    a_token=r.json()
    print(a_token)
    wpisz(a_token)

def refresh_token(auth, token_json):
    token=r"https://allegro.pl/auth/oauth/token"
    data={"grant_type": "refresh_token", "refresh_token": token_json["refresh_token"]}
    r=requests.post(url=token, auth=auth, data=data)
    r_token=r.json()
    return r_token

def kategorie(token):
    urls=r"https://api.allegro.pl/offers/listing?phrase=sekiro"
    data={"Authorization":"Bearer " + str(token), "Accept":"application/vnd.allegro.public.v1+json"}
    r=requests.get(url=urls, headers=data)
    kat=r.json()
    print(kat)
    return kat

def wpisz(token):
    filename="C:\\Users\\przem\\Dysk Google\\Programowanie\\untitled1\\token.txt"
    file=open(filename, "w")
    file.write(token['access_token'])
    file.write("\n")
    file.write(token['refresh_token'])
    file.write("\n")
    file.write(str(token['expires_in']))
    file.close()

def open_plik():
    file = open(r"C:\Users\przem\Dysk Google\Programowanie\untitled1\token.txt", "r")
    token=file.read
    file.close()
    return token

autoryzacja_user(client_id,auth)

