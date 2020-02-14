import piexif
import os
from PIL import Image

rozmiary={"600":(600,600),"400":(400,400),"227":(227,227), "200":(200,200)}
zdjecia=r"C:\Users\szyprz\Pictures\test"
output=r"C:\Users\szyprz\Pictures\output"

def Zmiana_rozmiaru(rozmiar,input,output):
        img=Image.open(input)
        img.thumbnail(rozmiar, Image.ANTIALIAS)
        img.save(output, "JPEG")

def Szczegoly(user_input,opis,path):
    tagi=user_input.encode("utf-16")
    tekst=opis.encode("utf-16")
    dane = {40095:list(tekst),40094: list(tagi)}
    exif_bytes = piexif.dump({"0th":dane})
    piexif.insert(exif_bytes,path)

tagi=input().replace(" ","")
descr=input().replace(" ","")

for photo in os.listdir(zdjecia):
    if photo[-3:]=="jpg":
        for roz_val in rozmiary:
            nazwa=str(photo[:-4]) + str(roz_val) + ".jpg"
            Zmiana_rozmiaru(rozmiary[roz_val],zdjecia+"\\"+str(photo),output+"\\"+nazwa)
            Szczegoly(tagi,descr,output+"\\"+nazwa)
