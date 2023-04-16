from threading import Thread

from nicegui import ui, app
import re
import pickle

import Methods
from Item import Item
from threading import Event
from datetime import datetime

eventArray = []

app.add_static_files("/images", "images")
with ui.row():
    ui.avatar("img:/images/skinportsnipe.png", font_size="100%")
    ui.label("SkinPortSnipe").style('color: #6E93D6; font-size: 300%; font-weight: 200')

columDict = {"columnDefs": [
    {"headerName": "URL", "field": "url"}, {"headerName": "Name", "field": "name"},
    {"headerName": "Maximaler Preis", "field": "maxprice"}
]}

rowDict = {"rowData": [
    {"url": "https://google.de", "name": "Google", "maxprice": "400"},
    {"url": "https://gutefrage.net", "name": "Gutefrage", "maxprice": "10"},
]}


def getCurrentTime():
    time = datetime.now()
    currentTime = time.strftime("%H:%M:%S")
    return currentTime


def createAndStartThreads():
    global eventArray

    for i in range(len(rowDict["rowData"])):
        event = Event()
        rData = rowDict["rowData"][i]
        item = Item(rData["url"], rData["name"], int(rData["maxprice"]))
        itemThread = Thread(target=item.run, args=(event,))
        eventArray.append(event)
        itemThread.start()
        currentTime = getCurrentTime()
        print(f"{currentTime}: Thread gestartet: {item.getName()}")
        ui.notify("Thread gestartet")


def stopThreads():
    currentTime = getCurrentTime()
    global eventArray
    if eventArray:
        for t in eventArray:
            t.set()
            ui.notify("Thread beendet")
            print(f"{currentTime}: Thread beendet")
        eventArray = []


def saveToFile():
    with open("link.save", "wb") as fp:
        pickle.dump(rowDict, fp)
    ui.notify("Liste gespeichert")


def readFromFile():
    with open("link.save", "rb") as fp:
        global rowDict
        rowDict = pickle.load(fp)


readFromFile()

table = ui.aggrid(columDict | rowDict)

with ui.dialog() as dialog, ui.card():
    ui.label("Löschen bestätigen?")
    with ui.row():
        ui.button('Löschen', on_click=lambda: dialog.submit('Yes')).tailwind.background_color("green")
        ui.button('Abbrechen', on_click=lambda: dialog.submit('No')).tailwind.background_color("red")


async def show(msg):
    result = await dialog
    if result == "Yes":
        handle_click(msg)
        ui.notify("Erfolgreich gelöscht")
    else:
        ui.notify("Löschen abgebrochen")


def handle_click(msg):
    for i in range(len(rowDict["rowData"])):
        data = rowDict["rowData"]
        if (data[i]["url"] == msg["args"]["data"]["url"]) and (data[i]["maxprice"] == msg["args"]["data"]["maxprice"]):
            del data[i]
            table.update()
            break


table.on('cellClicked', show)


def appendDictFromInput():
    urlText = url.value
    if not re.search("^https:\/\/(www)?skinport.com", urlText):
        ui.notify("Bitte gültige Email angeben")
        return
    nameText = name.value
    maxpriceText = maxprice.value
    if not re.search("[0-9]+(\\.[0-9]+)?", maxpriceText):
        ui.notify("Bitte gültigen Preis angeben")
        return
    rowDict["rowData"].append({"url": urlText, "name": nameText, "maxprice": maxpriceText})
    table.update()
    ui.notify("Item hinzugefügt")


with ui.row():
    url = ui.input(label="URL", placeholder="enter url here")
    name = ui.input(label="Name", placeholder="enter name here")
    maxprice = ui.input(label="Maximaler Preis", placeholder="enter max price here")
    button = ui.button("Hinzufügen", on_click=appendDictFromInput)
    saveButton = ui.button("Speichern", on_click=saveToFile)
    startThreads = ui.button("Start", on_click=createAndStartThreads).tailwind.background_color("green")
    stopThreads = ui.button("Stop", on_click=stopThreads).tailwind.background_color("red")


ui.run(title="SkinPortSnipe")
