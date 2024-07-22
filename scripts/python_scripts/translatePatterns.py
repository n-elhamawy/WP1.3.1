from datetime import timedelta
import time
import timeit
import sys
import re
import os
import gc
from importlib import import_module
from readInScanChainFile import *
#from tp import types
#from enumerations import enums
#import specialTypes
import shutil
import math
from binHexConverter import *

def doubleUnderScore(string):
	return re.findall(r'\_\_',string)

def removeQuotationMarks(string):
	return ''.join(re.findall(r'[a-zA-Z-0-9_.]+',string))

def renameIndexScanSigName(string):
	return ''.join(re.findall(r'\_\d+',string))

def matchPortAssignment(string):
	return ''.join(re.findall(r'(<\d+)',string))
	
def matchTimeStamp(string):
	return ''.join(re.findall(r'(#\d+)',string))

def checkForIndices(string):
	return re.findall(r'\d+',string)

def checkForArrayIndices(string):
	return re.findall(r'\[\d+\]',string)

def getMSB(cellSplit,topModule):
	specialTypes = import_module("specialTypes")
	temp = dir(specialTypes)
	for item in temp:
		if item in topModule:
			module = str(item)
			break
	modTypes = getattr(specialTypes,module)
	tp = import_module("tp")
	types = getattr(tp,"types")
	tmp = types[modTypes[cellSplit[0]]]
	i = 1
	while(type(tmp)!=list):
		tmp = tmp[cellSplit[i]]
		i += 1
	return tmp[0]	

def getLSB(cellSplit,topModule):
	specialTypes = import_module("specialTypes")
	temp = dir(specialTypes)
	for item in temp:
		if item in topModule:
			module = str(item)
			break
	print(cellSplit,topModule)
	modTypes = getattr(specialTypes,module)
	tp = import_module("tp")
	types = getattr(tp,"types")
	tmp = types[modTypes[cellSplit[0]]]
	i = 1
	while(type(tmp)!=list):
		tmp = tmp[cellSplit[i]]
		i += 1
	return tmp[-1]	
		
def readSTIL(stilFileName):
	print("Reading scan design information ...")
	stilFile = open(stilFileName,'r')
#	chainLength = 0
	inputFlag = False
	outputFlag = False
	signalOrderPI = []
	signalOrderPO = []
	for line in stilFile:
		## get number of input signals
		if not signalOrderPI:
			if "\"_pi\"" in line:
				inputFlag = True
				strippedLine= line.replace('\"','')
				strippedLine = strippedLine.replace(' ','')
				strippedLine = strippedLine.replace('\'','')
				strippedLine = strippedLine.replace(';','')
				strippedLine = strippedLine.strip()
				start = strippedLine.index("=") +1
				signalOrderPI += strippedLine[start:].split("+")
		elif inputFlag:
			if "// #signals=" in line:
				strippedLine= line.replace('\"','')
				strippedLine = strippedLine.replace(' ','')
				strippedLine = strippedLine.replace('\'','')
				strippedLine = strippedLine.replace(';','')
				strippedLine = strippedLine.strip()
				end = strippedLine.index("//")
				if (strippedLine[:end]):
					signalOrderPI += strippedLine[:end].split("+")
				inputFlag = False
			else:
				strippedLine= line.replace('\"','')
				strippedLine = strippedLine.replace(' ','')
				strippedLine = strippedLine.replace('\'','')
				strippedLine = strippedLine.replace(';','')
				strippedLine = strippedLine.strip()
				signalOrderPI += strippedLine.split("+")
		## get number of output signals
		elif not signalOrderPO:
			if "\"_po\"" in line:
				outputFlag = True
				strippedLine= line.replace('\"','')
				strippedLine = strippedLine.replace(' ','')
				strippedLine = strippedLine.replace('\'','')
				strippedLine = strippedLine.replace(';','')
				strippedLine = strippedLine.strip()
				start = strippedLine.index("=") +1
				signalOrderPO += strippedLine[start:].split("+")
		elif outputFlag:
			if "// #signals=" in line:
				strippedLine= line.replace('\"','')
				strippedLine = strippedLine.replace(' ','')
				strippedLine = strippedLine.replace('\'','')
				strippedLine = strippedLine.replace(';','')
				strippedLine = strippedLine.strip()
				end = strippedLine.index("//") 
				if (strippedLine[:end]):
					signalOrderPO += strippedLine[:end].split("+")
				outputFlag = False
			else:
				strippedLine= line.replace('\"','')
				strippedLine = strippedLine.replace(' ','')
				strippedLine = strippedLine.replace('\'','')
				strippedLine = strippedLine.replace(';','')
				strippedLine = strippedLine.strip()
				signalOrderPO += strippedLine.split("+")
		## get scan chain length						
#		elif "ScanLength" in line:
#			chainLength = int(checkForNumbers(line))
		else:
			continue
	
	stilFile.close()
	signalOrderPI = list(filter(lambda pi: pi != '', signalOrderPI))
	signalOrderPO = list(filter(lambda po: po != '', signalOrderPO))
	return signalOrderPI,signalOrderPO
		
def convertValues(zeroValue,oneValue,zeroReplacment,oneReplacement,value):
	value = value.replace(zeroValue,zeroReplacment)
	value = value.replace(oneValue,oneReplacement)
	return value.upper()		

def readEVCDPatterns(eVCDFileName):
	startTime = timeit.timeit()
	print("Reading eVCD patterns from:"+eVCDFileName)
	eVCDFile = open(eVCDFileName,'r')
	patterns = {}
#	inputs = {}
#	outputs = {}
	ports = {}
	time = -1
	vcdclose = False
	portSizes = {}
	reversedOrder = {}
	for line in eVCDFile:
		lineSplit = line.split()	
		if not lineSplit:
			continue
		if "$var port" in line:
			size = lineSplit[2]
			idNum =  checkForNumbers(lineSplit[3]) ##TODO idnUm might contain chars
			signal = lineSplit[4]
			portSizes[signal] = size
			ports[idNum] = signal
#			if signal[-2:] == "_o":
#				outputs[idNum] = signal
#			else:
#				inputs[idNum] = signal
#			if size !=  "1": ## reg width > 1 
#				indices = checkForIndices(size)
#				if indices:
#					if int(indices[0]) < int(indices[1]): ##[::-1] to align indices to python indexing
#						reversedOrder[signal] = True ## big endian
#					else:
#						reversedOrder[signal] = False	## little endian	
		elif matchTimeStamp(line):
			if vcdclose:
				continue
			else:
				time = int(checkForNumbers(line))
				patterns[time] = {}	
		elif matchPortAssignment(lineSplit[-1]):
			idNum = checkForNumbers(lineSplit[-1])
			value = lineSplit[0]
			size = len(value) -1
			if value[1].upper() == "L" or value[1].upper() == "H" or value[1].upper() == "X": ##output value
				converted = convertValues("L","H","0","1",value[1:])
#				converted = convertValues("N","Z","X","Z",value[1:])
#				if inputs[idNum] in reversedOrder and reversedOrder[inputs[idNum]]:
#				converted = converted[::-1]
				patterns[time].update({ports[idNum]:converted[::-1]}) 
			else: ## input value
				converted = convertValues("D","U","0","1",value[1:])
#				converted = convertValues("X","T","X","Z",value[1:])
#				if outputs[idNum] in reversedOrder and reversedOrder[outputs[idNum]]:
#				converted = converted[::-1]
				patterns[time].update({ports[idNum]:converted[::-1]}) 
		elif "$vcdclose" in line:
			vcdclose = True		
		else:
			continue
	eVCDFile.close()
	endTime = timeit.timeit()
#	print("Elapsed Time: %f"%(endTime - startTime))
	return patterns,portSizes

#def translateScanSigName(string):
#	arrayIndices = []
#	isUserDefined = False
#	regIndex = string.rfind("_reg_")
#	reg = "_reg_"
#	if regIndex > -1:
##		regIndex = string.index(reg)
#		sigName = string[:regIndex]
#		sigName = sigName.replace("__","/")
#		if renameIndexScanSigName(sigName):
#			index = int(checkForNumbers(renameIndexScanSigName(sigName)))            
#			sigName = sigName.replace(renameIndexScanSigName(sigName),"[%d]"%index)
#		sigRemainingPart = string[regIndex+len(reg):]
#		if checkForVariables(sigRemainingPart):
#			isUserDefined = True
#		if sigRemainingPart[-1] == "_":
#			sigRemainingPart = sigRemainingPart[:-1]
#		if doubleUnderScore(sigRemainingPart):
#			possibleArrays = sigRemainingPart.split("/")[-1] 
#			nameSplit = possibleArrays.split("__")
#			for n in nameSplit:
#				if n.isnumeric():
#					arrayIndices.append(int(n))
#				else:
#					sigName += ".%s"%n
#		else:
#			if sigRemainingPart.isnumeric():
#				arrayIndices.append(int(sigRemainingPart))
#			else:
#				sigName += ".%s"%sigRemainingPart
#	else:
#		reg = "_reg"
#		print(string)
#		regIndex = string.index(reg)
#		sigName = string[:regIndex]		
#		if checkForArrayIndices(string[regIndex:]):
#			tmpN = checkForArrayIndices(string[regIndex:])
#			for n in tmpN:
#				if checkForNumbers(n):
#					arrayIndices.append(int(checkForNumbers(n)))		
#	sigFeatures = {}
#	sigFeatures.update({'name':sigName})
#	sigFeatures.update({'isUserDefined':isUserDefined})
#	sigFeatures.update({'isArray':arrayIndices})
#	return sigFeatures

def calculateFlattenedIndex(indices,dimensions,offset):
	index = 0
	for i in range(0,len(indices)-1):
		index += indices[i]*math.prod(dimensions[i+1:])	
	index += indices[-1] + offset
	return index
	
#def readInScanChainFile(scanChainFile):
#	print("Reading scan chain order ...")
#	scanChainDef = False
#	scanChainFile = open(scanChainFile,'r')
#	scanChain = []
#	isUserDefinedType = []
#	arrayIndices =  {}
#	n = 0                                                      
#	for line in scanChainFile: ## read in the scan chain info
#		if "FLOATING" in line:
#			scanChainDef = True
#			start = line.index("FLOATING") +len("FLOATING")
#			lineSplit = line[start:].split()
#		elif "ORDERED" in line:
#			start = line.index("ORDERED") +len("ORDERED")
#			lineSplit = line[start:].split()
#		else:
#			lineSplit = line.split()
#		if scanChainDef:
#			if "+" in line and "+ ORDERED" not in line  and "+ FLOATING" not in line :
#				break
#			if lineSplit[0][-1].isnumeric():
#				scanSig = lineSplit[0][:-1]
#			else:
#				scanSig = lineSplit[0]
#			print(scanSig)
#			sigFeatures = translateScanSigName(scanSig)
#			scanChain.append(sigFeatures["name"])
#			isUserDefinedType.append(sigFeatures["isUserDefined"])
#			arrayIndices.update({n:sigFeatures['isArray']})
#			n += 1
#		else:
#			continue	
#	return scanChain,isUserDefinedType,arrayIndices			

def getScanChainOrder(scanChainFile,topModule):
	scanChain,isUserDefinedType,arrayIndices = readInScanChainFile(scanChainFile)
	offset = {}
	dimensions = {}
	n = len(scanChain)
	for i in range(0,n): ## get the correct offset and dimensions for arrays
		signal = scanChain[i]
		sigSplit = signal.split(".")
		sigName = sigSplit[0]
		if isUserDefinedType[i]:
			if "/" in sigSplit[0]: ## check if this is a submodule signal
				subSigSplit = sigSplit[0].split("/")
				if subSigSplit[-2][0:3] == "i_":
					module = subSigSplit[-2][3:]
				elif subSigSplit[-2][-2:] == "_i":
					module = subSigSplit[-2][:-2]
				else:
					module = subSigSplit[-2]	
				sigSplit[0] = subSigSplit[-1]
			else:
				module = topModule
			if signal not in offset:
				offset.update({signal:getLSB(sigSplit,module)})
			if sigName not in dimensions:
				dimensions.update({sigName:[getMSB(sigSplit,module)+1]})
			else:
				tempIndex = getMSB(sigSplit,module)+1
				if tempIndex > dimensions[sigName][-1]:
					dimensions[sigName][-1] = tempIndex
		if len(arrayIndices[i]) > 0:
			if sigName in dimensions:
				if len(dimensions[sigName]) < len(arrayIndices[i]):
					temp = dimensions[sigName]
					dimensions[sigName] = arrayIndices[i].copy()
					j = len(arrayIndices[i])-1
					for item in temp:
						if arrayIndices[i][j]+1 > item:
							dimensions[sigName][j] = arrayIndices[i][j]+1
				else:
					for j in range(0,len(arrayIndices[i])):
						if dimensions[sigName][j] < arrayIndices[i][j]+1:
							dimensions[sigName][j] = arrayIndices[i][j]+1			
			else:
				arrayTemp = arrayIndices[i].copy()
				for x in range(0,len(arrayTemp)):
					arrayTemp[x] += 1 
				dimensions.update({sigName:arrayTemp})
	for k in range(0,n): ## calculate the indices
		signal = scanChain[k]
		sigName = signal.split(".")[0]
		if len(arrayIndices[k]) == 0: ## not an array
			if signal in offset: ## user-defined type
				scanChain[k] = sigName + "[%d]"%offset[signal]
			else: ## primitive type
				scanChain[k] = sigName	
		else:
			if signal in offset:
				offInd = offset[signal] ## user-defined type
			else:
				offInd = 0 ## primitive type	
			if sigName in dimensions:
				if len(dimensions[sigName]) > len(arrayIndices[k]): ## TODO generalize
					arrayIndices[k].append(0)
				if topModule == "perf_counters":
					arrayIndices[k][0] -= 2819
					if dimensions[sigName][0] > 0:
						dimensions[sigName][0] -= 2819	
				index = calculateFlattenedIndex(arrayIndices[k],dimensions[sigName],offInd)
			else:
				index = arrayIndices[k][0]
			scanChain[k] = sigName + "[%d]"%index
	return scanChain, isUserDefinedType

def readVCDPatterns(fileName,topModule):
	MODULE_DECL = re.compile(r"\$scope\s*(\w+)\s*(\w+)\s*\$end")
#	MOD_DECL = re.compile(r"\$scope\s*begin\s*(\w+)\s*\$end")
	END_DECL = re.compile(r"\$upscope\s*\$end")
	print("Reading VCD patterns from: "+fileName)
	vcdFile = open(fileName,'r')
	scanPatterns = {}
	sigID = {}
	size = {}
	offset = {}
	reversedOrder = {}
	modules = []
	for line in vcdFile:
		lineSplit = line.split()
#		print(lineSplit)
		if not lineSplit:
			continue
		if "$var reg" in line:
			idNum = lineSplit[3]
			signal = getSignalName(topModule,modules + [lineSplit[4]])
			sigID[idNum] = signal 
			size[idNum] = int(lineSplit[2])
			if checkForNumbers(lineSplit[5]):
				offset[signal] = int(lineSplit[5].split(":")[-1][:-1])
			if int(lineSplit[2]) > 1: ## reg width > 1 
				endian = lineSplit[5]
				indices = checkForIndices(endian)
				if indices:
					if int(indices[0]) > int(indices[1]): ##[::-1] to align indices to python indexing
						reversedOrder[signal] = True ## big endian
					else:
						reversedOrder[signal] = False	## little endian	
		elif "$scope" == lineSplit[0] :
			modules.append(lineSplit[2])
#		elif match := MOD_DECL.match(line):
#			print(match.group(1))
#			modules.append(match.group(1))	
		elif match := END_DECL.match(line):
			if modules:
				modules.remove(modules[-1])
		elif matchTimeStamp(line):
			time = int(checkForNumbers(line))
			scanPatterns[time] = {}
		elif line[0] == "0" or line[0] == "1" or line[0] == "x":
			temp = line[1:].strip()
			if temp in sigID:
				sig = sigID[temp]
				scanPatterns[time].update({sig:line[0]})
		elif lineSplit[-1] in sigID:
			if len(lineSplit[0][1:]) < size[lineSplit[-1]]:
				value = "0"*(size[lineSplit[-1]]-len(lineSplit[0][1:]))+lineSplit[0][1:]
			else:
				value = lineSplit[0][1:]
			sig = sigID[lineSplit[-1]]
			if sig in reversedOrder and reversedOrder[sig]:
				value = value[::-1]
			scanPatterns[time].update({sig:value}) 	
	return scanPatterns,offset

## TODO automatic detection
def nonScanValueOutput(topModule):
	if topModule == "ibex_core":
		return "crash_dump_o[95]","patterns"
	elif topModule == "ibex_if_stage":
		return "pc_id_o[31]","patterns"
	else:
		return "",""

def getSignalName(topModule,varSplit):	
	if "ibex_" in topModule and topModule != "ibex_core":
		topModule = topModule.replace("ibex_","")
	for n in range(len(varSplit)-1,-1,-1):
			if topModule in varSplit[n]:
				varName = '/'.join(varSplit[n+1:])
	return varName			

def readWaves(wvFile,topModule):
	sigList  = []
	loopVars = []
	isArray = False
	waveFile   = open(wvFile,"r")
	for line in waveFile:
		lineSplit = line.split()
		if len(lineSplit) > 0:
			if lineSplit[0] == "add":
				varSplit = lineSplit[-1].split("/")
				if isArray:
					loopVars.append(lineSplit[-1])
				else:
					sigList.append(lineSplit[-1])
			elif lineSplit[0] == "for":
				for i in range(1,len(lineSplit)):
					if checkForNumbers(lineSplit[i]):
						arraySize = int(checkForNumbers(lineSplit[i]))
						break
				isArray = True
			elif lineSplit[0] == "}":
				for i in range(arraySize,-1,-1):
					for var in loopVars:
						sigList.append(var.replace("$i",str(i)))
				isArray = False
				loopVars = []
		else:
			continue	
	return sigList

def readListFile(listFile,topModule,sigList):
	print("Starting data extraction ...")
	offset = 2
	## Import input values from the List file to the testbench
	## The file containing the list of values
	lstFile   = open(listFile,"r")
	patterns = {}
	varNames = []
	sizes = {}
	sizesBefore = {}
	print("Processing ...")
	for line in lstFile:
		lineSplit = line.split()
		if lineSplit[0].isnumeric():
			time = int(lineSplit[0])
			patterns[time] = {}
			for i in range(2,len(lineSplit)):
				varNameInd = i - offset
				if "*" not in lineSplit[i]:
					if "'b" in lineSplit[i]:
						ind = lineSplit[i].index("'b")
						val = lineSplit[i][ind+2:]
						varSize = int(lineSplit[i][:ind])
					else:
						val = lineSplit[i]
						varSize = 1
				else:
#					print(varNames[varNameInd],lineSplit[i],time)
					if varNames[varNameInd] in sizesBefore:
						print(sizesBefore[varNames[varNameInd]])
#					if varNames[varNameInd] == "commit_instr_o[1].op" or varNames[varNameInd] == "commit_instr_o[0].op":
#						varSize = 7
#						val = "0000000"		
				if not varNames[varNameInd] in sizesBefore:
					sizesBefore.update({varNames[varNameInd]:varSize})
				else:			
					if not val.isnumeric():
						for enum in enums:
							if val in enums[enum]["values"]:
								valEnum = enums[enum]["values"].index(val)
								bitLength = enums[enum]["bitLength"]
								val = bin(valEnum)[2:].zfill(bitLength)
								break
					else:
						if len(val) != sizesBefore[varNames[varNameInd]]:
							bitLength = sizesBefore[varNames[varNameInd]]
							val = bin(int(val))[2:].zfill(bitLength)
				if "." in varNames[varNameInd]:
					index = varNames[varNameInd].index(".")
					var = varNames[varNameInd][:index]
				else:
					var = varNames[varNameInd]
				varSplit = var.split("/")## to distinguish between instances and signals
				if checkForArrayIndices(varSplit[-1]):
					varSplit[-1] = varSplit[-1][:varSplit[-1].index("[")]
					var = '/'.join(varSplit)
				if var in patterns[time]:
					val = patterns[time][var] + val
					patterns[time].update({var:val})
					sizes[var] = len(val)
				else:
					patterns[time].update({var:val})
					sizes[var] = len(val)
		else:
			lineSplit.remove("ns")
			lineSplit.remove("delta")
			for i in range(0,len(lineSplit)):
				varTemp = lineSplit[i].split("/")
				if len(varTemp) > 1:
					varName = getSignalName(topModule,varTemp)
					sigList.pop(sigList.index(lineSplit[i]))
				else:
					for item in sigList:
						if varTemp[0] in item:							
							varName = getSignalName(topModule,item.split("/"))
							sigList.pop(sigList.index(item))
							break
				varNames.append(varName)
	## Close List file
	lstFile.close()
#	signalSize = dict(zip(varNames, varSizes))
#	return patterns,signalSize
	return patterns,sizes

def filterChanges(patterns):
	timings = list(patterns.keys())
	timings.remove(0)
	signals = list(patterns[0].keys())
	arraySize = len(signals)
	change = [0 for n in range(0,arraySize)]
	for timing in timings:
		for i in range(0,arraySize):
			if patterns[timing][signals[i]] == patterns[change[i]][signals[i]]:
				del patterns[timing][signals[i]]
			else:
				change[i] = timing
	return patterns

def writeSTILVector(patterns,signalOrder,pinCount,prevVector):	
	vector = ["" for n in range(pinCount)]
	for i in range(0,pinCount):
			sig = signalOrder[i]
			if checkForArrayIndices(sig):
				index = int(checkForNumbers(''.join(checkForArrayIndices(sig))))
				sigEnd = sig.index("[")
				sig = sig[:sigEnd]
			else:
				index = -1	
			if sig in patterns:
				if index > -1:
					value = patterns[sig]
					vector[i] = value[index]	
				else:
					vector[i] = patterns[sig]
			else:
				if sig == "se" or sig == "sin":
					vector[i] = "0"
				elif sig == "sout":
					continue
				else:	
#					print("Before:",prevVector[i],vector[i])
					vector[i] = prevVector[i]
#					print("After:",prevVector[i],vector[i])		
	return vector

def writeSTILSCANVector(scanPattern,scanChainOrder,chainLength,previous,scanOffset):
	scanVector = ""
	for j in range(0,chainLength):
		signal = scanChainOrder[j]
		sigSplit = signal.split("/") ## to distinguish between instances and signals
		if checkForArrayIndices(sigSplit[-1]):
			index = int(checkForNumbers(''.join(checkForArrayIndices(sigSplit[-1]))))
			sigSplit[-1] = sigSplit[-1][:sigSplit[-1].index("[")]
			signal = '/'.join(sigSplit)
		else:
			index = -1	
		if signal in scanPattern:
			value = scanPattern[signal]
			if index > -1:
				if signal in scanOffset:
					index = index - scanOffset[signal]
				scanVector = value[index] + scanVector ## left most bit is the first shifted in/out bit
			else:
				scanVector = value + scanVector ## left most bit is the first shifted in/out bit
		else:
#			print(scanChainOrder[j])
			scanVector = previous[::-1][j] + scanVector
	return scanVector			

def writeVerilogSCANVector(scanPattern,scanChainOrder,chainLength,previous):
	scanVector = ["" for i in range(0,chainLength)]
	scanChainOrder = scanChainOrder[::-1]
	for j in range(0,chainLength):
		signal = scanChainOrder[j]
		sigSplit = signal.split("/") ## to distinguish between instances and signals
		if checkForArrayIndices(sigSplit[-1]):
			index = int(checkForNumbers(''.join(checkForArrayIndices(sigSplit[-1]))))
			sigSplit[-1] = sigSplit[-1][:sigSplit[-1].index("[")]
			signal = '/'.join(sigSplit)
		else:
			index = -1	
		if signal in scanPattern:
			value = scanPattern[signal][::-1]
			if index > -1:
				scanVector[j] = value[index] 
			else:
				scanVector[j] = value
		else:
			scanVector[j] = previous[j]		 
	return scanVector		

def writeNonScanSTIL(topModule,demo,signalOrderPI,signalOrderPO,patterns,pSizes,breakFlag,breakAt):
	inputPinCount = len(signalOrderPI)
	outputPinCount = len(signalOrderPO)
	captureProcedure = "capture_clk_i"
	print("Translating imported patterns into STIL patterns ...")
	text  = "Pattern \"_pattern_\" {\n \t\tW \"CLOCK_ON\";\n"
	times = [x for x in range(10,list(patterns.keys())[-1],20)]
	times.insert(0,0)
	for time in times:
		if breakFlag:
			if time > breakAt:
				break	
		if time in patterns:
			## Write the capture update
			pi = ''.join(writeSTILVector(patterns[time],signalOrderPI,inputPinCount)) ## Write pi vector  
			po = ''.join(writeSTILVector(patterns[time],signalOrderPO,outputPinCount)) ## Write po vector
		text += "\t\tCall \"%s\" { \n"%captureProcedure
		text += "\t\t\t\"_pi\" = %s;\n"%pi.upper()
		text += "\t\t\t\"_po\" = %s; \n"%convertValues("0","1","L","H",po)
		text += "\t\t\t\"clk_i\" = P; }\n"
	text+= "}"
	return text

def writeScanSTIL(topModule,demo,signalOrderPI,signalOrderPO,patterns,portSizes,scanPatterns,scanOffset,scanChainOrder,isUserDefinedType,breakFlag,breakAt,spfFile):
	
	dst = os.getcwd()+"/%s_%s.stil"%(demo,topModule)
	if os.path.exists(dst):
		os.remove(dst)
	shutil.copy(spfFile,dst)
	spfFile = open(dst,'a+')
	inputPinCount = len(signalOrderPI) 
	outputPinCount = len(signalOrderPO)
	sinInd = signalOrderPI.index("sin")
	seInd = signalOrderPI.index("se")
	soutIndOrder = signalOrderPO.index("sout")
	patternID = 0
	lastSoutValue = ""
	soutVal,soutPattType = nonScanValueOutput(topModule)
	if checkForArrayIndices(soutVal):
		soutInd = int(checkForNumbers(''.join(checkForArrayIndices(soutVal))))
		soutVal = soutVal[:soutVal.index("[")]
	else:
		soutInd = -1	
#	scanChainOrderchainOrder = scanChainOrder[::-1] ## TODO merge writeSTILVector &writeSTILSCANVector
	chainLength = len(scanChainOrder)
	prevScanVector = ""
	prevPI = ""
	prevPO = ""
	print("Translating imported patterns into STIL patterns ...")
	captureProcedure = "capture_clk_i"
	text  = "Pattern \"_pattern_\" {\n \t\tW \"CLOCK_ON\";\n"
	text += "\t\t \"precondition all Signals\": C { \"_pi\"=\\r%d 0 ;\n\t\t\t\"_po\"=\\r%d X ; }\n"%(inputPinCount,outputPinCount)
	text += "\t\tMacro \"test_setup\";\n"
	sin = ""
	sout = "0"*chainLength
	lastTimeStamp = list(patterns.keys())[-1]
	if lastTimeStamp%2 == 0:
		lastTimeStamp -= 10
	times = [x for x in range(10,lastTimeStamp,20)]
	times.insert(0,0)
#	c = re.compile('[^01]')
#	for sig in patterns[0]:
#		print(sig,patterns[0][sig])
#	return

	for time in times:	
		if breakFlag:
			if time > breakAt:
				lastTimeStamp = time
				break	
		if time in patterns:
			if time in scanPatterns:## Write the loading/ unloading values of the scan chain
				sin = writeSTILSCANVector(scanPatterns[time],scanChainOrder,chainLength,prevScanVector,scanOffset)
				prevScanVector = sin
			pi = writeSTILVector(patterns[time],signalOrderPI,inputPinCount,prevPI)## Write the capture cycle,input values
			po = writeSTILVector(patterns[time],signalOrderPO,outputPinCount,prevPO)## Write the capture cycle,expected output values
			if soutInd > -1:
				if soutPattType == "patterns":
					if soutVal in patterns[time]:
						po[soutIndOrder] = patterns[time][soutVal][soutInd]
					else:
						po[soutIndOrder] = prevPO[soutIndOrder]	
				else:
					if time in scanPatterns and soutVal in scanPatterns[time]:
						po[soutIndOrder] = scanPatterns[time][soutVal][soutInd]
					else:
						po[soutIndOrder] = lastSoutValue
			else:
				if soutPattType == "patterns":
					if soutVal in patterns[time]:
						po[soutIndOrder] = patterns[time][soutVal]
					else:
						po[soutIndOrder] = prevPO[soutIndOrder]	
				else:
					if time in scanPatterns and soutVal in scanPatterns[time]:
						po[soutIndOrder] = scanPatterns[time][soutVal]
					else:
						po[soutIndOrder] = lastSoutValue
		lastSoutValue  = po[soutIndOrder]
		## Write pattern consisting of previous expected sout, load scan chain with sin then capture with pi & po 
#		print("Writing pattern %d to STIL file ..."%patternID)
		text += "\t\tAnn {* full_sequential *}\n"
		text += "\t\t\"pattern %d\": Call \"load_unload\" {\n"%patternID
		if time > 0:
			sout = sin
			text += "\t\t\t\"sout\" = %s; \n"%convertValues("0","1","L","H",sout)			
		text += " \t\t\t\"sin\" = %s;} \n"%sin.upper().replace("X","N")
		text += "\t\tCall \"%s\" { \n"%captureProcedure
		text += "\t\t\t\"_pi\" = %s;\n"%''.join(pi).upper()
		text += "\t\t\t\"_po\" = %s; \n"%convertValues("0","1","L","H",''.join(po))
		text += "\t\t\t\"clk_i\" = P; }\n"
		spfFile.write(text)
		text = ""
		patternID += 1
		prevPI = pi
		prevPO = po

	if lastTimeStamp in scanPatterns: ## Write  the last shift out value
		sout = writeSTILSCANVector(scanPatterns[lastTimeStamp],scanChainOrder,chainLength,prevScanVector,scanOffset)
	else:
		sout = prevScanVector
	text  = "\t\tAnn {* full_sequential *}\n"
	text += "\t\t\"end %d unload\": Call \"load_unload\" {\n"%(patternID-1)
	text += "\t\t\t\"sout\" = %s;"%convertValues("0","1","L","H",sout)	
	text += "}\n}\n"
	spfFile.write(text)
	spfFile.close()

#def writeSTILPatterns(spfFile,topModule,demo,text):
#	#make a copy of the file to work with
#	print("Writing patterns to STIL file ...")
#	dst = os.getenv("DEMOS_DIR")+"/STIL/%s/SCAN/%s.stil"%(demo,topModule)
#	if os.path.exists(dst):
#		os.remove(dst)
#	shutil.copy(spfFile,dst)
#	spfFile = open(dst,'a+')
#	spfFile.write(text)
#	spfFile.close()

def main():
	topModule 		= sys.argv[1]
	demo 					= sys.argv[2]
	spfFile 			= sys.argv[3]
	portsFile 		= sys.argv[4]
	scanFile  		= sys.argv[5]
	scanChainFile = sys.argv[6]	
	if len(sys.argv) > 7:
			breakAt			= int(sys.argv[7])
			breakFlag 	= True
#	startTime = time.time()

	signalOrderPI,signalOrderPO = readSTIL(spfFile)
	breakFlag 									= False
	breakAt											= -1
		
	patterns,portSizes = readEVCDPatterns(portsFile)
	scanPatterns,scanOffset = readVCDPatterns(scanFile,topModule)

	scanChainOrder,isUserDefinedType = getScanChainOrder(scanChainFile,topModule)
	writeScanSTIL(topModule,demo,signalOrderPI,signalOrderPO,patterns,portSizes,scanPatterns,scanOffset,scanChainOrder,isUserDefinedType,breakFlag,breakAt,spfFile)
#		VtbText = writeScanVerilogTb(topModule,demo,signalOrderPI,signalOrderPO,patterns,portSizes,scanPatterns,scanSizes,scanChainOrder,isUserDefinedType,breakFlag,breakAt)
	
#		VtbText = writeNonScanVerilogTb(topModule,demo,signalOrderPI,signalOrderPO,patterns,portSizes,breakFlag,breakAt)

#	writeSTILPatterns(spfFile,topModule,demo,text)
#	writeVerilogTbFile(VtbText,topModule,demo,designType)
#	endTime = time.time()
#	print("Elapsed Time: "+str(timedelta(seconds = (endTime-startTime))))
	
	
if __name__ == "__main__":
    main()	
