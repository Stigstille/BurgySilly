def findBurgy(divLine, cell, wks, burgyNames):
    burgyNames = str(burgyNames).split(">, <Cell ")
    burgyNames.pop(0)
    for burgy in burgyNames:
        burgy = str(burgy)
        burgy = burgy.split(' \'')
        burgy[1] = burgy[1].split('\'')[0]
        
        if burgy[1] == divLine[1]:
            sillyColumn = burgy[0].split('2')[0]
            sillyRow = cell[0].split('A')[1]
            origVal = wks.get_value(f'{sillyColumn}{sillyRow}')
            if origVal != "":
                origVal = int(origVal)
                print(f"Original Value: {origVal}")
                wks.update_value(f'{sillyColumn}{sillyRow}', str(origVal + 1))
            else:
                print(f"New Burgy!!")
                wks.update_value(f'{sillyColumn}{sillyRow}', str(1))
    return