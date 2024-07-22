from readInScanChainFile import *
import os

def writeWaveFile(topModule,prefix,scanChainFile):
	chainOrder,temp0,temp1 = readInScanChainFile(scanChainFile)
	sortedChain = []
	for cell in chainOrder:
		if cell not in sortedChain:	
			sortedChain.append(cell.replace(".","/"))
	chainOrder = []
	for i in range(0,len(sortedChain)):
		if sortedChain[i] in chainOrder:
				continue
		cellSplit = sortedChain[i].split("/")
		if len(cellSplit) == 1:
			chainOrder.insert(0,sortedChain[i])
		else:
			for mod in cellSplit[:-1]:
				temp = []
				for j in range(i,len(sortedChain)):
					if mod in sortedChain[j]:
						temp.append(sortedChain[j])
				temp.sort(key=len)
				chainOrder.extend(temp)		
	text = ""
	for wave in chainOrder:
		text += "vcd add %s%s\n"%(prefix,wave)

	print(os.getcwd())
	waveFile = open(os.getcwd()+"/%s_scanWaves.do"%(topModule),"w+")
	waveFile.write(text)
	waveFile.close()
	
def main():
	topModule 		= sys.argv[1]
	prefix  			= sys.argv[2]
	scanChainFile = sys.argv[3]

	writeWaveFile(topModule,prefix,scanChainFile)

if __name__ == "__main__":
    main()	
