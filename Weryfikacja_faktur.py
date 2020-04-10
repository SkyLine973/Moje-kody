import os

Folder={"02":"02 Lodz","02W":"02 wysylka","04":"04 Poznan","05":"05 Rzgow Katowicka Tkaniny","06":"06 Pszczyna","07":"07 Rzgów Pabianicka Flora","07W":"07 wysylka"}

def Sciezka_do_faktur():
    homedir=os.path.join(os.path.expanduser("~"),"Polimex.net Sp. z o.o. Sp. k\Administracja - Kopie Faktur")
    if os.path.exists(homedir):
        print("Ścieżka do faktur pobrana prawidłowo")
    else:
        print("Brak domyślnej ścieżki!")
        while True:
            homedir= input("Podaj ścieżkę: ")
            if os.path.exists(homedir):
                break
            else:
                print("Zła ścieżka")
                continue
    return homedir

def Test_faktur(fak0,fak1,a,b):
    flag=True
    try:
        int(fak0[a:b])
        int(fak1[a:b])
    except:
        flag=False
    return flag

def User_Input(homedir):
    print("Jeżeli wpisujesz zakres danych rozdziel je przecinkiem nie używając spacji.")
    magazyn=input("Numer magazynu: ").replace("*","02,02W,04,05,06,07,07W").split(",")
    rok=input("Rok: ").replace("*","2018,2019,2020").split(",")
    miesiac=input("Miesiąc: ").replace("*","01,02,03,04,05,06,07,08,09,10,11,12").split(",")
    for mag_folder in magazyn:
        for rok_folder in rok:
            for mie_folder in miesiac:
                if os.path.exists(os.path.join(homedir, Folder[mag_folder],rok_folder, mie_folder)):
                    homedir2=os.path.join(homedir, Folder[mag_folder],rok_folder, mie_folder)
                    Faktury=os.listdir(homedir2)
                    Weryfikacja_Faktur(Faktury, Folder[mag_folder],homedir2)
                else:
                    continue

def Weryfikacja_Faktur(Lista_Faktur,Magazyn, sciezka):
    if Magazyn=="02 wysylka" or Magazyn=="07 wysylka":
        a,b,c,d=12,18,19,29
    else:
        a,b,c,d=11,17,18,28
    print("\n\nAktualnie sprawdzany magazyn:",Magazyn,"\nData:",sciezka[-2:],sciezka[-7:-3],"\nLiczba faktur",len(Lista_Faktur),end="\n\n")
    i=0
    suma=0
    while i<(len(Lista_Faktur)-1):
        if Test_faktur(Lista_Faktur[i],Lista_Faktur[i+1],a,b)==False:
            print("Coś poszło nie tak przy fakturach",Lista_Faktur[i],"oraz",Lista_Faktur[i+1])
            i+=1
            continue
        liczba = int(Lista_Faktur[i+1][a:b]) - int(Lista_Faktur[(i)][a:b])
        typ = Lista_Faktur[i][-3:]
        waga=os.stat(os.path.join(sciezka,Lista_Faktur[i]))
        if (liczba>1):
            suma+=liczba-1
            print("Brakuje faktur z przedziału: ", int(Lista_Faktur[i][a:b]),"-",int(Lista_Faktur[i+1][a:b])," zakres dni: ",Lista_Faktur[(i)][c:d],"-",Lista_Faktur[(i+1)][c:d])
        if (typ!="pdf"):
            suma+=1
            print("Zła nazwa pliku: ",int(Lista_Faktur[i][a:b])," data: ",Lista_Faktur[(i)][c:d])
        if (waga.st_size==0):
            suma+=1
            print("Zły rozmiar pliku: ",int(Lista_Faktur[i][a:b])," data: ",Lista_Faktur[(i)][c:d])
        i+=1
    print("\nŁącznie faktur do naprawy:",suma,end="\n\n")
    return

while True:
    User_Input(homedir=Sciezka_do_faktur())



