import os
import shutil
import datetime
import time

Sciezka_Do_Faktur=r"C:\TEMP"
Sciezka_Docelowa=r"C:\Users\wydruk\Polimex.net Sp. z o.o. Sp. k\Administracja - Kopie Faktur"
Sciezka_Docelowa2=r"\\10.1.1.59\fk\kopie faktur"
Lacznik_PDF_To_Folder={"FS_02_":"02 Lodz","FSW_02":"02 wysylka","FS_04_":"04 Poznan","FS_05_":"05 Rzgow Katowicka Tkaniny","FS_06_":"06 Pszczyna","FS_07_":"07 Rzgów Pabianicka Flora","FSW_07":"07 wysylka"}

def Kopia(Wszystkie_PDF):
    for Cala_Sciezka_Do_Konkretnego_PDF in Wszystkie_PDF:
        try:
            if os.path.basename(Cala_Sciezka_Do_Konkretnego_PDF)[5:8]=="FS_":
                Data=datetime.datetime.strptime(os.path.basename(Cala_Sciezka_Do_Konkretnego_PDF)[18:28], "%Y-%m-%d")
            else:
                Data=datetime.datetime.strptime(os.path.basename(Cala_Sciezka_Do_Konkretnego_PDF)[19:29], "%Y-%m-%d")

            if not os.path.exists(os.path.join(Sciezka_Docelowa,Lacznik_PDF_To_Folder[os.path.basename(Cala_Sciezka_Do_Konkretnego_PDF)[5:11]],str(Data.year),str(Data.month))):
                os.makedirs(os.path.join(Sciezka_Docelowa,Lacznik_PDF_To_Folder[os.path.basename(Cala_Sciezka_Do_Konkretnego_PDF)[5:11]],str(Data.year),str(Data.month)))
            if not os.path.exists(os.path.join(Sciezka_Docelowa2,Lacznik_PDF_To_Folder[os.path.basename(Cala_Sciezka_Do_Konkretnego_PDF)[5:11]],str(Data.year),str(Data.month))):
                os.makedirs(os.path.join(Sciezka_Docelowa2,Lacznik_PDF_To_Folder[os.path.basename(Cala_Sciezka_Do_Konkretnego_PDF)[5:11]],str(Data.year),str(Data.month)))

            shutil.copy2(Cala_Sciezka_Do_Konkretnego_PDF,os.path.join(Sciezka_Docelowa,Lacznik_PDF_To_Folder[os.path.basename(Cala_Sciezka_Do_Konkretnego_PDF)[5:11]],str(Data.year),str(Data.month),os.path.basename(Cala_Sciezka_Do_Konkretnego_PDF)))
            shutil.move(Cala_Sciezka_Do_Konkretnego_PDF,os.path.join(Sciezka_Docelowa2,Lacznik_PDF_To_Folder[os.path.basename(Cala_Sciezka_Do_Konkretnego_PDF)[5:11]],str(Data.year),str(Data.month),os.path.basename(Cala_Sciezka_Do_Konkretnego_PDF)))
        except Exception as e:
            Wpisz_Do_Pliku(e)

def Sciezka_Do_Konkretnego_Pliku():
    Lista_Wszystkich_Folderow=["02","04","05","06","07","Wysylka","WysylkaFlora"]
    PDFY_Z_Katalogow=[]
    for Nazwa_Folderu in Lista_Wszystkich_Folderow:
        Pliki_W_Katalogu=os.listdir(os.path.join(Sciezka_Do_Faktur,Nazwa_Folderu))
        for Plik in Pliki_W_Katalogu:
            PDFY_Z_Katalogow.append(os.path.join(Sciezka_Do_Faktur,Nazwa_Folderu,Plik))
    Kopia(PDFY_Z_Katalogow)

def Wpisz_Do_Pliku(e):
    print(str(e))
    filename="C:\\Error.txt"
    file=open(filename, "a")
    file.write(str(datetime.datetime.now()))
    file.write(str(e))
    file.write("\n")
    file.close()

while True:
    Sciezka_Do_Konkretnego_Pliku()
    time.sleep(900)
