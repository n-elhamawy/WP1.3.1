import os
import sys

def writeNewWaveForm(waveFormName,period):
	waveForm  = "\tWaveformTable \"%s\" {\n"%waveFormName
	waveForm += "\t\tPeriod \'%dns\';\n"%period
	waveForm += "\t\tWaveforms {\n"
	waveForm += "\t\t\t\"clk_i\" { 0 { \'0ns\' D; } }\n"
	waveForm += "\t\t\t\"clk_i\" { P { \'0ns\' D; \'%dns\' U; \'%dns\' D; } }\n"%(period/2,period)
	waveForm += "\t\t\t\"clk_i\" { 1 { \'0ns\' U; } }\n"
	waveForm += "\t\t\t\"clk_i\" { Z { \'0ns\' Z; } }\n"
	waveForm += "\t\t\t\"rst_ni\" { 0 { \'0ns\' D; } }\n"
	waveForm += "\t\t\t\"rst_ni\" { P { \'0ns\' U; \'%dns\' D; \'%dns\' U; } }\n"%(period/2,period)
	waveForm += "\t\t\t\"rst_ni\" { 1 { \'0ns\' U; } }\n"
	waveForm += "\t\t\t\"rst_ni\" { Z { \'0ns\' Z; } }\n"
	waveForm += "\t\t\t\"_default_In_Timing_\" { 0 { \'0ns\' D; } }\n"
	waveForm += "\t\t\t\"_default_In_Timing_\" { 1 { \'0ns\' U; } }\n"
	waveForm += "\t\t\t\"_default_In_Timing_\" { Z { \'0ns\' Z; } }\n"
	waveForm += "\t\t\t\"_default_In_Timing_\" { N { \'0ns\' N; } }\n"
	waveForm += "\t\t\t\"_default_Out_Timing_\" { X { \'0ns\' X; } }\n"
	waveForm += "\t\t\t\"_default_Out_Timing_\" { H { \'0ns\' X; \'%dns\' H; } }\n"%(period/2)
	waveForm += "\t\t\t\"_default_Out_Timing_\" { T { \'0ns\' X; \'%dns\' T; } }\n"%(period/2)
	waveForm += "\t\t\t\"_default_Out_Timing_\" { L { \'0ns\' X; \'%dns\' L; } }\n"%(period/2)
	waveForm += "\t\t}\n"
	waveForm +=  "\t}\n"
	waveForm +=  "}\n"
	return waveForm

def writeNewProcedures(waveFormName,inputs,outputs):
	procedures  = "Procedures {\n"
	procedures += "\t\"load_unload\" {\n"
	procedures += "\t\tW \"%s\";\n"%waveFormName
	procedures += "\t\tC { \"sin\"=0; \"clk_i\"=0; \"rst_ni\"=1; \"se\"=1; }\n"
	procedures += "\t\tShift {          W \"%s\";\n"%waveFormName
	procedures += "\t\t\tV { \"_si\"=#; \"_so\"=#; \"clk_i\"=P; }\n"
	procedures += "\t\t}\n"
	procedures += "\t}\n"
	procedures += "\t\"capture_clk_i\" {\n"
	procedures += "\t\tW \"%s\";\n"%waveFormName
	procedures += "\t\tC { \"se\"=0; \"_po\"=\\r%d X ; }\n"%outputs
	procedures += "\t\t\"forcePI\": V { \"_pi\"=\\r%d # ; }\n"%inputs
	procedures += "\t\t\"measurePO\": V { \"_po\"=\\r%d # ; }\n"%outputs
	procedures += "\t\tC { \"_po\"=\\r%d X ; }\n"%outputs
	procedures += "\t\t\"pulse\": V { \"clk_i\"=P; }\n"
	procedures += "\t}\n"
	procedures += "\t\"capture_rst_ni\" {\n"
	procedures += "\t\tW \"%s\";\n"%waveFormName
	procedures += "\t\tC { \"_po\"=\\r%d X ; }\n"%outputs
	procedures += "\t\t\"forcePI\": V { \"_pi\"=\\r%d # ; }\n"%inputs
	procedures += "\t\t\"measurePO\": V { \"_po\"=\\r%d # ; }\n"%outputs
	procedures += "\t\tC { \"_po\"=\\r%d X ; }\n"%outputs
	procedures += "\t\t\"pulse\": V { \"rst_ni\"=P; }\n"
	procedures += "\t}\n"
	procedures += "\t\"capture\" {\n"
	procedures += "\t\tW \"%s\";\n"%waveFormName
	procedures += "\t\tC { \"_po\"=\\r%d X ; }\n"%outputs
	procedures += "\t\t\"forcePI\": V { \"_pi\"=\\r%d # ; }\n"%inputs
	procedures += "\t\t\"measurePO\": V { \"_po\"=\\r%d # ; }\n"%outputs
	procedures += "\t}\n"
	procedures += "}\n"
	procedures += "MacroDefs {\n"
	procedures += "\t\"test_setup\" {\n"
	procedures += "\t\tW \"%s\";\n"%waveFormName
	procedures += "\t\tV { \"clk_i\"=0; \"rst_ni\"=1; \"se\"=0; \"sin\"=0;}\n"
	procedures += "\t}\n"
	procedures += "}\n"
	return procedures

def editSPFFile(spfFile,period,newWaveForm):
	spFile  = open(spfFile,'r')
	text    = ""
	addNewWave = False
	inputFlag = False
	outputFlag = False
	for line in spFile:
		if "Ann" in line:
			if "clk_i" in line or "rst_ni" in line:
				line = line.replace("5",str(period-1))
		elif line == "Timing {\n":
			addNewWave = True	
		elif addNewWave and line == "}\n":
			text += writeNewWaveForm(newWaveForm,period)
			addNewWave = False
			continue
		elif "\"_pi\"" in line:
			inputFlag = True
		elif "\"_po\"" in line:	
			outputFlag = True
		elif inputFlag:
			if "// #signals=" in line:
				inputs = int(line[line.index("=")+1:])
				inputFlag = False
		elif outputFlag:
			if "// #signals=" in line:
				outputs = int(line[line.index("=")+1:])
				outputFlag = False		
		elif "Procedures" in line:
			text += writeNewProcedures(newWaveForm,inputs,outputs)
			break
		text += line
	spFile.close()
	os.remove(spfFile)
	tmp = open(spfFile,'w')
	tmp.write(text)
	tmp.close()

def main():
	spfFile = sys.argv[1]
	period	= int(sys.argv[2])
	newWaveForm = sys.argv[3]
	editSPFFile(spfFile,period,newWaveForm)
	
if __name__ == "__main__":
    main()		
