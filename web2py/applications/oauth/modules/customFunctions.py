def test() :
    return 'testtest'

def getTimestamp() :
    import time
    return time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S")

def printToLog(stringToPrint) :
    print getTimestamp() + '\t' + stringToPrint