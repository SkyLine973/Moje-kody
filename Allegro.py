import requests
from requests.auth import HTTPBasicAuth
import datetime as dt
import pandas as pd
import smtplib
import time
import os

client_id=r"id"
client_secret=r"id"
auth=HTTPBasicAuth(client_id,client_secret)

def main():
    while True:
        plik=weryfi_plik()
        if plik!=False:
            wer_token=weryfi_token(plik)
            if wer_token==1 or wer_token==3:
                token=autoryzacja_user(client_id,auth)
                print("Autoryzacja",dt.datetime.now())
                mail(token)
                for x in range(0,10):
                    temp=autoryzacja_device(token,auth)
                    if temp=='<Response [400]>':
                        print("Nie uzyskano autoryzacji. Ponowię próbę za 6 min")
                        time.sleep(360)
                    elif temp==False:
                        print("Wystąpił błąd podczas autoryzacji",dt.datetime.now())
                        break
                    else:
                        wpisz_token(temp)
                        print("Wpisanie tokena",dt.datetime.now())
                        break
            elif wer_token==2:
                wpisz_token(refresh_token(auth,plik))
                print("wykonano refresh",dt.datetime.now())
                continue
            elif wer_token==4:
                dane=obrabianie_zwrotki(kategorie(plik))
                if len(dane)>=1:
                    mail(dane)
                    print("Wysłano maile",dt.datetime.now())
                else:
                    print("Brak danych do wysłania",dt.datetime.now())
                time.sleep(3600)
        else:
            print("Brak dostępu do lokalizacji. Może pomóc uruchomienie jako administrator",dt.datetime.now())
            time.sleep(3600)


def autoryzacja_user(client_id, auth):
    authUrl = r"https://allegro.pl/auth/oauth/device"
    data={"Accept": r"application/vnd.allegro.public.v1+json", "client_id":client_id}
    r=requests.post(url=authUrl, auth=auth, data=data)
    device=r.json()
    return device

def autoryzacja_device(device,auth):
    token=r"https://allegro.pl/auth/oauth/token?grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Adevice_code&device_code={}".format(device["device_code"])
    r=requests.post(url=token, auth=auth)
    weryfikacja=str(r)
    if weryfikacja=='<Response [400]>':
        return weryfikacja
    elif weryfikacja=='<Response [200]>':
        a_token=r.json()
        return a_token
    else:
        return False

def refresh_token(auth, tokeny):
    token=r"https://allegro.pl/auth/oauth/token"
    data={"grant_type": "refresh_token", "refresh_token": tokeny[1]}
    r=requests.post(url=token, auth=auth, data=data)
    r_token=r.json()
    return r_token

def kategorie(token):
    urls=r"https://api.allegro.pl/offers/listing?phrase=sekiro&option=SMART&sort=price&category.id=146702"
    #urls=r"https://api.allegro.pl/sale/categories?parent.id=9"
    data={"Authorization":"Bearer " + token[0], "Accept":"application/vnd.allegro.public.v1+json"}
    r=requests.get(url=urls, headers=data)
    kat=r.json()
    return kat

def weryfi_token(plik):
    if len(plik)<=0:
        return 1
    else:
        roznica=dt.datetime.now()-dt.datetime.strptime(plik[3],"%Y-%m-%d %H:%M:%S.%f")
        roznica=(roznica.days*86400)+roznica.seconds
        if roznica>int(plik[2])*0.7 and roznica<int(plik[2]):
            return 2 #trzeba zrobić refresh_token
        elif roznica>=int(plik[2]):
            return 3 #refresh_token wygasł
        else:
            return 4 #token jest OK

def wpisz_token(token):
    path = (r"{}\token.txt").format(os.getcwd())
    file=open(path, "w")
    file.write(token['access_token'])
    file.write("\n")
    file.write(token['refresh_token'])
    file.write("\n")
    file.write(str(token['expires_in']))
    file.write("\n")
    file.write(str(dt.datetime.now()))
    file.close()

def weryfi_plik():
    path=(r"{}\token.txt").format(os.getcwd())
    plik = []
    if os.path.exists(path)==True:
        with open(path, "r") as file:
            for row in file:
                plik.append(row.replace("\n", ""))
        return plik
    else:
        try:
            file=open(path,"w+")
            file.close()
            return plik
        except:
            return False

def obrabianie_zwrotki(zwrotka):
    rez=[]
    for klucze in zwrotka['items'].keys():
        klucz=zwrotka['items'][klucze]
        for produkty in klucz:
            produkty_norm=pd.json_normalize(produkty)
            rez.append(produkty_norm)
    df=pd.concat(rez,ignore_index=True)
    df=df.where(df['sellingMode.price.amount']<'150').dropna()
    return df[['id','name','sellingMode.price.amount','seller.superSeller','stock.available']]

def mail(dane):
    user='notymailapp@gmail.com'
    password='pass'
    mailTo=['przemo973111@gmail.com']
    mailSubject='Powiadomienia z Allegro'
    if str(type(dane))=="<class 'dict'>":
        mailBody='''\n\nWymagana autoryzacja: {}'''.format(dane['verification_uri_complete'])
    else:
        i=0
        temp=[]
        while i<len(dane):
            ss="Tak" if dane['seller.superSeller'].iloc[i]==True else "Nie"
            temp.append('''\n\nLink: https://allegro.pl/oferta/{}\nNazwa: {}\nKwota: {} zl\nCzy Super Sprzedawca: {}\nIlosc: {}\n\n'''.format(dane['id'].iloc[i],dane['name'].iloc[i],dane['sellingMode.price.amount'].iloc[i],ss,dane['stock.available'].iloc[i]))
            i+=1
        mailBody="".join(temp)

    message='''From: {}
Subject: {}
{}
'''.format(user,mailSubject,mailBody).encode("utf-8")

    try:
        server=smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.ehlo()
        server.login(user,password)
        server.sendmail(user,mailTo,message)
        server.close()
        return True
    except:
        return False

main()


