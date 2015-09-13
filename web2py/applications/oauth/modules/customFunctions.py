import logging
import os
def getTimestamp() :
    import time
    return time.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S")

def printToLog(stringToPrint, newline = 0) :
	if newline:
		print '\n'
	print getTimestamp() + '\t' + stringToPrint
	#logger = logging.getLogger('log')
	#hdlr = logging.FileHandler(os.getcwd() + '\logs\log.txt')
	#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	#hdlr.setFormatter(formatter)
	#logger.addHandler(hdlr) 
	#logger.setLevel(logging.DEBUG)
	#logger.debug(stringToPrint)
