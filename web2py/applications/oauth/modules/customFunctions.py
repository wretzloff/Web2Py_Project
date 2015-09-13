import logging
def getTimestamp() :
    import time
    return time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S")

def printToLog(stringToPrint, newline = 0) :
    if newline:
        print '\n'
    print getTimestamp() + '\t' + stringToPrint
	#logger = logging.getLogger('myapp')
	#hdlr = logging.FileHandler('C:\Users\Will\Desktop\myapp.log')
	#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	#hdlr.setFormatter(formatter)
	#logger.addHandler(hdlr) 
	#logger.setLevel(logging.DEBUG)
	#logger.debug(stringToPrint)
