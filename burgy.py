import sys
import os.path
import requests
import pygsheets

from findBurgy import *

version = "1.0.5"
url="DISCORDWEBHOOKURL" # NEVER PUBLISH THIS!!!!

if len(sys.argv) != 2:
    print(f'Please run command as `python {sys.argv[0]} [Burgy File Name]`')
    exit()

if not os.path.isfile(sys.argv[1]):
    print("Please use a real file")
    exit()

try:
  client = pygsheets.authorize()
except Exception as ex:
  if os.path.exists("./sheets.googleapis.com-python.json"):
    os.remove("./sheets.googleapis.com-python.json")
    client = pygsheets.authorize()
    print("Bwaa!! You have reconnected!! Time to read the silly sheet :3")
    
  else:
    print("Error encountered...")
    print(ex)
    exit()

sh = client.open_by_key('1jtn3i6jaRMc0NQhJtZkJZ1cWgbYdRdn1e51dksYrhes')
wks = sh.worksheet_by_title('Burgacha')

data = {
    "content" : f"Using Burgy Uploader v{version}",
    "username" : f"Burgy Uploader v{version}"
}
requests.post(url, json=data)
wks.cell('A1').note = f"Using Burgy Uploader v{version}"
newBurgys = 0
totalBurgys = 0
newUsers = 0
totalUsers = 0
try:
    lines = open(sys.argv[1]).read().splitlines()
    for line in lines:
        usrnms = wks.range('A:A')
        burgyNames = wks.range('2:2')
        if line == "------ NEW DAY ------":
            print("----STARTING NEW DAY----")
        else:
            totalBurgys += 1
            divLine = line.split(" got ")
            divLine[1] = divLine[1].split("!")[0]
            print(divLine)
            if divLine[0] != "":
                madeNew = False
                found = False
                for cell in usrnms:
                    cellData = [cell[0].label, cell[0].value]
                    if (cellData[1].lower() == divLine[0].lower()) and not found:
                        foundBurgy = findBurgy(divLine, cellData, wks, burgyNames)
                        data["content"] = f"{divLine[0]} now has {foundBurgy} {divLine[1]}!!"
                        if foundBurgy == "their first":
                            newBurgys += 1
                        requests.post(url, json=data)
                        found = True
                    elif (cellData[1] == "") and not found:
                        if not madeNew:
                            if cellData[0] != "A3":
                                newUsers += 1
                                newBurgys += 1
                                wks.update_value(f'{cellData[0]}', divLine[0])
                                madeNew = True
                                data["content"] = f"# NEW USER!!\n{divLine[0]} now has {findBurgy(divLine, cellData, wks, burgyNames)} {divLine[1]}!!"
                                requests.post(url, json=data)
                                found = True

                        
            else:
                print(f"This burgy ({divLine[1]}) was triggered manually (10 Day Streak)")
                data["content"] = f"There was a burgy ({divLine[1]}) that was triggered manually (10 Day Streak)"
                requests.post(url, json=data)
    usrnmsFinal = wks.range('A:A')
    for cell in usrnmsFinal:
        if (not cell[0].label in ["A1","A2","A3"]) and (cell[0].value != ""):
            totalUsers += 1
    data["content"] = f"<:BURGYBUTCLOSEUP:1202870909178875985> DAILY BURGY STATS <:BURGYBUTCLOSEUP:1202870909178875985> \nNew Burgies rolled today: {newBurgys}\nFirst Time Burgy rollers: {newUsers}\nTotal Burgies rolled: {totalBurgys}\nTotal Burgy Enjoyers: {totalUsers}\nBurgy uploader created by: Stigstille"
    requests.post(url, json=data)
except IOError:
    print("Could not read file:", sys.arv[1])
except Exception as ex:
    print(f'Unknown error! Please send a screenshot or copy/paste of your console to @stigstille on discord')
    print(ex)
