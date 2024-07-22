import sys
import os
import shutil
import math
#from writeTestbench import *
from translatePatterns import *

def debugFailingPatts(fpfileName,scanChainFile,topModule):
	fpFile = open(fpfileName,'r')
	chainOrder,temp = getScanChainOrder(scanChainFile,topModule)
	chainOrder = chainOrder[::-1] ## reverse order to match STIL order
	failingCells = {}
	for line in fpFile:
		lineSplit = line.split()
		if lineSplit[0].isnumeric():
#			pattNo = int(lineSplit[0]) ## can be used to get the time 20*pattNo -10 for pattNo > 0
			signal = lineSplit[1]
			if lineSplit[2].isnumeric():
				index = int(lineSplit[2])
			elif checkForArrayIndices(lineSplit[1]):
				index = int(checkForNumbers(''.join(checkForArrayIndices(lineSplit[1]))))
				signal = signal[:signal.index('[')]
			else:
				index = -1
			if signal == "sout" and index != -1: ##scanPatterns
				failingCells.update({"%s[%d]"%(signal,index):chainOrder[index]}) 
#			else: ## patterns
#				if signal == "sout":
#				
#				else:
#	
		else:
			continue
	for cell in failingCells:
		print(cell,failingCells[cell])



def main():
	topModule 		= sys.argv[1]
	scanChainFile = sys.argv[2]
	fpFileName 		= sys.argv[3]
	
	debugFailingPatts(fpFileName,scanChainFile,topModule)
	
if __name__ == "__main__":
    main()						
