import sys
import os.path

import pygsheets

from findBurgy import *


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
try:
    lines = open(sys.argv[1]).read().splitlines()
    for line in lines:
        usrnms = wks.range('A:A')
        burgyNames = wks.range('2:2')
        if line == "------ NEW DAY ------":
            print("----STARTING NEW DAY----")
        else:
            divLine = line.split(" got ")
            divLine[1] = divLine[1].split("!")[0]
            print(divLine)
            if divLine[0] != "":
                madeNew = False
                found = False
                for cell in usrnms:
                    cellData = [cell[0].label, cell[0].value]
                    if (cellData[1].lower() == divLine[0].lower()) and not found:
                        findBurgy(divLine, cellData, wks, burgyNames)
                        found = True
                    elif (cellData[1] == "") and not found:
                        if not madeNew:
                            if cellData[0] != "A3":
                                wks.update_value(f'{cellData[0]}', divLine[0])
                                madeNew = True
                                findBurgy(divLine, cellData, wks, burgyNames)
                                found = True

                        
            else:
                print(f"This burgy ({divLine[1]}) was triggered manually (10 Day Streak)")

except IOError:
    print("Could not read file:", sys.arv[1])
except Exception as ex:
    print(f'Unknown error! Please send a screenshot or copy/paste of your console to @stigstille on discord')
    print(ex)