import sys
import re
import os

def checkForNumbers(string):
	return ''.join(re.findall(r'\d+',string))

def checkForArrayIndices(string):
	return re.findall(r'\[\d+\]',string)

def renameIndexScanSigName(string):
	return ''.join(re.findall(r'\_\d+',string))	
def checkForVariables(string):
	return ''.join(re.findall(r'[a-zA-Z]+',string))

def doubleUnderScore(string):
	return re.findall(r'\_\_',string)
				
def translateScanSigName(string):
	arrayIndices = []
	isUserDefined = False
	regIndex = string.rfind("_reg_")
	reg = "_reg_"
	if regIndex > -1:
#		regIndex = string.index(reg)
		sigName = string[:regIndex]
		sigName = sigName.replace("__","/")
		if renameIndexScanSigName(sigName):
			index = int(checkForNumbers(renameIndexScanSigName(sigName)))            
			sigName = sigName.replace(renameIndexScanSigName(sigName),"[%d]"%index)
		sigRemainingPart = string[regIndex+len(reg):]
		if checkForVariables(sigRemainingPart):
			isUserDefined = True
		if sigRemainingPart[-1] == "_":
			sigRemainingPart = sigRemainingPart[:-1]
		if doubleUnderScore(sigRemainingPart):
			possibleArrays = sigRemainingPart.split("/")[-1] 
			nameSplit = possibleArrays.split("__")
			for n in nameSplit:
				if n.isnumeric():
					arrayIndices.append(int(n))
				else:
					sigName += ".%s"%n
		else:
			if sigRemainingPart.isnumeric():
				arrayIndices.append(int(sigRemainingPart))
			else:
				sigName += ".%s"%sigRemainingPart
	else:
		reg = "_reg"
#		print(string)
		regIndex = string.index(reg)
		sigName = string[:regIndex]		
		if checkForArrayIndices(string[regIndex:]):
			tmpN = checkForArrayIndices(string[regIndex:])
			for n in tmpN:
				if checkForNumbers(n):
					arrayIndices.append(int(checkForNumbers(n)))		
	sigFeatures = {}
	sigFeatures.update({'name':sigName})
	sigFeatures.update({'isUserDefined':isUserDefined})
	sigFeatures.update({'isArray':arrayIndices})
	return sigFeatures
	
def readInScanChainFile(scanChainFile):
	print("Reading scan chain order ...")
	scanChainDef = False
	scanChainFile = open(scanChainFile,'r')
	scanChain = []
	isUserDefinedType = []
	arrayIndices =  {}
	n = 0                                                      
	for line in scanChainFile: ## read in the scan chain info
		if "FLOATING" in line:
			scanChainDef = True
			start = line.index("FLOATING") +len("FLOATING")
			lineSplit = line[start:].split()
		elif "ORDERED" in line:
			start = line.index("ORDERED") +len("ORDERED")
			lineSplit = line[start:].split()
		else:
			lineSplit = line.split()
		if scanChainDef:
			if "+" in line and "+ ORDERED" not in line  and "+ FLOATING" not in line :
				break
			if lineSplit[0][-1].isnumeric():
				scanSig = lineSplit[0][:-1]
			else:
				scanSig = lineSplit[0]
#			print(scanSig)
			sigFeatures = translateScanSigName(scanSig)
			scanChain.append(sigFeatures["name"])
			isUserDefinedType.append(sigFeatures["isUserDefined"])
			arrayIndices.update({n:sigFeatures['isArray']})
			n += 1
		else:
			continue	
	return scanChain,isUserDefinedType,arrayIndices		

def main ():
	
	scanChainFile = sys.argv[1]	
	scanChain,isUserDefinedType,arrayIndices = readInScanChainFile(scanChainFile)

if __name__ == "__main__":
    main()		
