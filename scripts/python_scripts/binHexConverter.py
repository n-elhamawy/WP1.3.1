def convertBinToHex(string):
	temp = len(string) % 4
	if temp > 0:
		zeros = "0"*(4-temp)
		string = zeros + str(string)
	result = ""
	for i in range(0,len(string),4):
		if string[i:i+4] == "0000":
			result = result + "0"
		elif string[i:i+4] == "0001":
			result = result + "1"
		elif string[i:i+4] == "0010":
			result = result + "2"
		elif string[i:i+4] == "0011":
			result = result + "3"
		elif string[i:i+4] == "0100":
			result = result + "4"
		elif string[i:i+4] == "0101":
			result = result + "5"
		elif string[i:i+4] == "0110":
			result = result + "6"
		elif string[i:i+4] == "0111":
			result = result + "7"
		elif string[i:i+4] == "1000":
			result = result + "8"
		elif string[i:i+4] == "1001":
			result = result + "9"
		elif string[i:i+4] == "1010":
			result = result + "A"
		elif string[i:i+4] == "1011":
			result = result + "B"
		elif string[i:i+4] == "1100":
			result = result + "C"
		elif string[i:i+4] == "1101":
			result = result + "D"
		elif string[i:i+4] == "1110":
			result = result + "E"
		elif string[i:i+4] == "1111":
			result = result + "F"
		else:
			result = result + "X"	
	return result
	
def convertToBin(hexVal):
	result = ""
	for i in range(0,len(hexVal)):
		if hexVal[i] == "0":
			result += "0000"
		elif hexVal[i] == "1":
			result += "0001"
		elif hexVal[i] == "2":
			result += "0010"
		elif hexVal[i] == "3":
			result += "0011"
		elif hexVal[i] == "4":
			result += "0100"
		elif hexVal[i] == "5":
			result += "0101"
		elif hexVal[i] == "6":
			result += "0110"
		elif hexVal[i] == "7":
			result += "0111"
		elif hexVal[i] == "8":
			result += "1000"
		elif hexVal[i] == "9":
			result += "1001"
		elif hexVal[i].upper() == "A":
			result += "1010"
		elif hexVal[i].upper() == "B":
			result += "1011"
		elif hexVal[i].upper() == "C":
			result += "1100"
		elif hexVal[i].upper() == "D":
			result += "1101"
		elif hexVal[i].upper() == "E":
			result += "1110"
		elif hexVal[i].upper() == "F" :
			result += "1111"																
	return result
