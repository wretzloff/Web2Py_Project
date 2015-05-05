def getTimestamp() :
    import time
    return time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S")

def printToLog(stringToPrint, newline = 0) :
    if newline:
        print '\n'
    print getTimestamp() + '\t' + stringToPrint
