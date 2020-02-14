import tkinter as tk
import requests

#91da59a96a556a8656b81bde14b21775
#api.openweathermap.org/data/2.5/forecast?q={city name},{country code}
HEIGHT=500
WIDTH=600

def Format(pogoda):
    try:
        nazwa=pogoda["name"]
        opis=pogoda["weather"][0]['description']
        temp=round(pogoda["main"]["temp"])
        string="Miejscowość: %s \nPogoda: %s \nTemperatura: %s" % (nazwa,opis,temp)
    except:
        string="Coś poszło nie tak"

    return string

def pobierz_pogode(miasto):
    klucz="91da59a96a556a8656b81bde14b21775"
    url="https://api.openweathermap.org/data/2.5/weather"
    params={"APPID":klucz, "q":miasto, "units":"metric", "lang":"pl"}
    response=requests.get(url, params=params)
    odp=response.json()
    label["text"]=Format(odp)

root=tk.Tk()

canvas=tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image=tk.PhotoImage(file="landscape.png")
background_label=tk.Label(root, image=background_image)
background_label.place(x=0,y=0,relwidth=1,relheight=1)

frame=tk.Frame(root, bg="#80c1ff", bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor="n")

entry=tk.Entry(frame, font=("Courier",15))
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text="Pogoda", font=("Courier",15), command=lambda: pobierz_pogode(entry.get()))
button.place(relx=0.7, relheight=1,relwidth=0.3)

lower_frame=tk.Frame(root, bg="#80c1ff", bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor="n")

label=tk.Label(lower_frame, font=("Courier",15), anchor="nw",justify="left")
label.place(relwidth=1, relheight=1)

root.mainloop()

