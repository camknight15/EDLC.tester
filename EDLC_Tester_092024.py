import pyvisa 
import os
import shutil
import sys
import time
import datetime
from timeit import default_timer as timer
import csv
import msvcrt
import logging
import serial
 
k_time = 0.3
#serialcomm = serial.Serial('COM10', 9600)
#serialcomm.timeout = 1

#set defaults
def defaults():
    global datafilename
    global logfilename
    global inputfilename
    global wait_time
    global logfilepath
    global app_log
    global datafilepath

    datafilename = 'ATE'
    logfilename = 'Log'
    wait_time = 300
    inputfilename = 'LANIDList'
    logfilepath = 'C:\\HQA\Software\\'
    #datafilepath = 'C:\\HQA\Software\\'

    #logging.basicConfig(filename="Amazon Current Log.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
    from logging.handlers import RotatingFileHandler
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    #logFile = 'C:\\HQA\\Software\\Amazon Current Log.log'
    #logfilename = "Log_File"
    #logFile = 'C:\\HQA\\Software\\' + logfilename + '.log'
    logFile = logfilepath + logfilename + '.log'
    my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.DEBUG)
    app_log = logging.getLogger('root')
    app_log.setLevel(logging.DEBUG)
    app_log.addHandler(my_handler)

defaults()

def logdata():
    global logfilename
    global logfilepath
    global app_log
    #logfilepath = 'C:\\HQA\Software\\'
    #logging.basicConfig(filename="Amazon Current Log.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
    from logging.handlers import RotatingFileHandler
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    #logFile = 'C:\\HQA\\Software\\Amazon Current Log.log'
    #logfilename = "Log_File"
    #logFile = 'C:\\HQA\\Software\\' + logfilename + '.log'
    logFile = logfilepath + logfilename + '.log'
    my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.DEBUG)
    app_log = logging.getLogger('root')
    app_log.setLevel(logging.DEBUG)
    app_log.addHandler(my_handler)

def InvalidSelection():
   print("Invalid Choice")

def Exit():
   sys.exit(0)

def DestroyFile():
    global datafilename
    file = datafilename + '.csv'
    if(os.path.isfile(file) and os.path.isfile(file)):
        print("Are you sure? press 'y'")
        while(1):
            if msvcrt.kbhit():
                ASCII_in = ord(msvcrt.getche())
                if ASCII_in == 121:
                    print("Erasing Contents")
                    app_log.debug("Erasing CSV")
                    os.remove(file)  
                    break 
                else:
                    break
    else:
        print(datafilename + ".csv file not found.  Cannot erase")
        app_log.debug("attempting to destroy csv. cannot find file")

def Setup():
    global DAQ_address
    rm = pyvisa.ResourceManager()
    rm.list_resources()
    DAQ_list = []
    DAQ_list = rm.list_resources()

    if not DAQ_list:
        print("no DAQ connected.  Please connect and try again")
        app_log.debug("no daq connected.  try again")
        main()
    else:
        for x in range(len(DAQ_list)):
            print("\n\nDAQ Selection:")
            print("|DAQ #| |DAQ Address|")
            print(" " + str(x) + "       " + DAQ_list[x])
            #print(DAQ_list[x])
        DAQ_comp = int(input("\nType DAQ number to connect (9 to exit):    "))
        #DAQ_address = str(DAQ_list[DAQ_comp])  
        
        #add error check input against list for out of range condition
        if DAQ_comp == 9:
            #print("here debug") #debug
            main()
        if DAQ_comp +1 <= len(DAQ_list) and DAQ_comp >= 0:
            DAQ_address = str(DAQ_list[DAQ_comp])  
        else:
            print("Error!  Input out of range.")
            Setup()
        
        if DAQ_address in DAQ_list:
            my34970A = rm.open_resource(DAQ_address)
            DAQ_status = my34970A.query("*IDN?")
            print("Serial:" + DAQ_status)
            app_log.debug("Serial: %s" + DAQ_status)
            '''
            CARD_list1 = []
            my34970A.write("SYST: CTYP? 100")
            str0 = my34970A.read()

            print("card 100: ", str0)
            list = str.split(",")
            for i in list:
                CARD_list1.append(i)
            if CARD_list1[1] == "34901A":
                print("Card 100 OK")
                CARD_list2 = []
                my34970A.write("SYST: CTYP? 200")
                str1 = str(my34970A.read())
                print("card 200: ", str1)
                list1 = str1.split(",")
                for a in list1:
                    CARD_list2.append(a)
                if CARD_list2[1] == "34903A":
                    print("Card 200 OK")
                    CARD_list3 = []
                    my34970A.write("SYST: CTYP? 300")
                    str2 = str(my34970A.read())
                    print("card 300: ", str2)
                    list2 = str2.split(",")
                    for b in list2:
                        CARD_list2.append(b)
                    if CARD_list3[1] == "34903A":
                        print("Card 300 OK")
                    else:
                        print("Incorrect card slot 300.  Insert correct card and try again.")
                        Setup()
                else:
                    print("Incorrect card slot 200.  Insert correct card and try again.")
                    Setup()
            else:
                print("Incorrect card slot 100.  Insert correct card and try again.")
                Setup()'''
        else:
            print("ERROR - Check DAQ Connection")
            app_log.debug("ERROR - Check DAQ Connection.  Something isn't right.")
            Setup()
                    
def checkDAQ():
    global DAQ_address
    rm = pyvisa.ResourceManager()
    DAQ_list = []
    DAQ_list = rm.list_resources()
    if not DAQ_list:
        print("DAQ Connection Error... Stopping Program")
        print("Ensure DAQ Connected and try again")
        app_log.debug("DAQ Connection error.  program stopped. back to main menu")
        main()
    else:
        print("DAQ Status OK")
        app_log.debug("DAQ Status OK")

def DEBUG_TEST():
    global DAQ_address
    global counter
    Setup()
    rm = pyvisa.ResourceManager()
    my34970A = rm.open_resource(DAQ_address)

    #setup
    my34970A.timeout=5000
    my34970A.write("*CLS")
    my34970A.write("*RST")

    #timebetduts = 1
    #scanlist = "(@121)"
    #my34970A.write("CONF:CURR:DC AUTO, DEF, (@121)")
    #my34970A.write("ROUTE:SCAN " + scanlist)
    #my34970A.write("ROUT:CHAN:DELAY:AUTO ON, (@121)")
    #my34970A.write("ROUT:OPEN (@301)")
    #my34970A.write("ROUT:CLOS (@301)")
    print("press z to stop running")
    print("press c to close or o to open 301")
    while (1):
        if msvcrt.kbhit():
            ASCII_in = ord(msvcrt.getche())
            if ASCII_in == 111:
                print("open switch... delay for 10 seconds")
                my34970A.write("ROUT:OPEN (@301)")
                #time.sleep(10)
                for i in range (10,0,-1):
                    print(str(i) +" s")
                    time.sleep(1)
                print("select another option")
            if ASCII_in == 99:
                print("close switch... delay for 10 seconds")
                my34970A.write("ROUT:CLOS (@301)")
                #time.sleep(10)
                for j in range (10,0,-1):
                    print(str(j) +" s")
                    time.sleep(1)
                print("select another option")
            if ASCII_in == 122:
                print("exit to menu")
                break
        else:
            #print("enter selection o or c")
            time.sleep(1)
    my34970A.close()

def BreakBeforeMake():
    #keep as an example for logging, csv, etc.
    global DAQ_address
    global counter
    global datafilename
    global logfilename
    global wait_time
    global inputfilename
    global app_log
    global datafilepath
    
    Setup()
    rm = pyvisa.ResourceManager()
    my34970A = rm.open_resource(DAQ_address)

    #setup
    my34970A.timeout=5000
    my34970A.write("*CLS")
    my34970A.write("*RST")

    timebetduts = 1
    #timebetalllans = 30
    scanlist = "(@121,122)"
    my34970A.write("CONF:CURR:DC AUTO, DEF, (@121,122)")
    my34970A.write("ROUTE:SCAN " + scanlist)
    my34970A.write("ROUT:CHAN:DELAY:AUTO ON, (@121,122)")


    if os.path.isfile(datafilename + '.csv'):
        print("Found " + datafilename + ".csv file!")
        app_log.debug("CSV file found")
        if os.path.isfile(inputfilename + '.txt'):
            with open(inputfilename + ".txt") as LanList:
                lines = LanList.readlines()

                DUTNo = []
                LANID = []
                DAQ_ch_import = []

                for l in lines:
                    as_list=l.split(",")
                    DUTNo.append(as_list[0])
                    LANID.append(as_list[1])
                    DAQ_ch_import.append(as_list[2].replace("\n",""))
                print ("DUT Nos: ")
                print(DUTNo)
                print("LAN ID List: ")
                print (LANID)
                print("DAQ Switching Channels in use")
                print(DAQ_ch_import)
                app_log.debug("DUTs imported %s", DUTNo)
                app_log.debug("LAN IDs imported %s", LANID)
                app_log.debug("DAQ Channels imported %s", DAQ_ch_import)
                LanList.close()
            #All DUTs Disconnected from Switching System
            my34970A.write("ROUT:CLOS (@201:220,301:320)")
            time.sleep(1)
            print("Running... press 'z' 3x to stop program")
            app_log.debug("program start press z 3x to stop")
            while 1:
                if msvcrt.kbhit():
                    ASCII_in = ord(msvcrt.getche())
                    if ASCII_in == 122:
                        print("Exiting Program")
                        app_log.debug("exiting program")
                        #my34970A.write("ROUT:CLOS (@201:220,301:320)")
                        #time.sleep(1)
                        break
                for x in range(len(LANID)):
                    if msvcrt.kbhit():
                        ASCII_in = ord(msvcrt.getche())
                        if ASCII_in == 122:
                            print("Exiting Program")
                            app_log.debug("exiting program")
                            my34970A.write("ROUT:CLOS (@201:220,301:320)")
                            time.sleep(1)
                            break
                    from datetime import datetime
                    now = datetime.now()
                    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
                    print(dt_string)

                    DUTNo_use = DUTNo[x]
                    LANID_use = LANID[x]
                    DAQ_ch = DAQ_ch_import[x]
                   
                    checkDAQ()

                    #close DUT switches one at a time to allow for current measurement 
                    my34970A.write("ROUT:OPEN (@" + str(DAQ_ch) + ")")
                    #time.sleep(0.2)
                    #Measure Current
                    if(int(DAQ_ch) >= 200 and int(DAQ_ch) < 300):
                        my34970A.write('MEAS:CURRENT:DC? AUTO, DEF, (@121)')
                    if(int(DAQ_ch) >= 300 and int(DAQ_ch) < 400):
                        my34970A.write('MEAS:CURRENT:DC? AUTO, DEF, (@122)')
                    current = float(my34970A.read())
                    round(current, 6)
                    print(DAQ_ch)
                    print(current)
                    app_log.debug("DAQ Ch %s", DAQ_ch)
                    app_log.debug("Current %s", current)
                    '''#meas temp
                    my34970A.write("MEAS:TEMP? TC, J, 1, DEF,(@101)")
                    tempj = float(my34970A.read())
                    print("temp = " + tempj + "C")'''
                    #open DUT again
                    my34970A.write("ROUT:CLOS (@" + str(DAQ_ch) + ")")        
                    time.sleep(timebetduts)

                    app_log.debug("append to " + datafilename + ".csv")
                    with open(datafilename + '.csv', 'a+', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([dt_string, LANID_use, DUTNo_use, DAQ_ch, current])
                        file.close()
                #time.sleep(timebetalllans)
                #delay between all DUTs 
                app_log.debug("wait " + str(wait_time) + " seconds between all DUT scans")
                for t in range(wait_time,0,-1):
                    print("Time to next scan: " + str(t) + " seconds")
                    time.sleep(1)
                    if msvcrt.kbhit():
                        ASCII_in = ord(msvcrt.getche())
                        if ASCII_in == 122:
                            break
                app_log.debug("done waiting")
                counter += 1
                print("counter = "+str(counter))
                app_log.debug("counter = %s" + str(counter))
                '''if counter >= 144:
                    #copy data to onedrive every 12 hours
                    app_log.debug("copy data and log to onedrive")
                    print("copying file to OneDrive")
                    now = str(datetime.now())[:19]
                    now = now.replace(":","_")
                    src_dir = "C:\\Users\\TurnerB\\Amazon_data.csv"
                    dest_dir = "C:\\Users\\TurnerB\\OneDrive - Landis+Gyr\\Documents\\18024 Amazon\\Beta 2 ALT\\Current Data Auto\\Amazon_data_"+str(now)+".csv"
                    shutil.copy(src_dir, dest_dir)
                    #copy log to onedrive
                    src_dir_log = "C:\\Users\\TurnerB\\Amazon Current Log.log"
                    dest_dir_log = "C:\\Users\\TurnerB\\OneDrive - Landis+Gyr\\Documents\\18024 Amazon\\Beta 2 ALT\\Current Data Auto\\Amazon Current Log_"+str(now)+".log"
                    shutil.copy(src_dir_log, dest_dir_log)
                    counter=0'''
            my34970A.close()
            app_log.debug("close instrument")
        else:
            print(inputfilename + ".txt no found!!")
            app_log.debug("no " + inputfilename + ".txt file found")
    else:
        print('Creating ' + datafilename + '.csv file')
        app_log.debug("creating csv file")
        with open(datafilename + '.csv', 'w', newline ='') as csvfile:
            filewriter = csv.writer(csvfile)
            filewriter.writerow(["Timestamp", "LAN ID", "DUT #", "DAQ Ch.", "Current"])
        BreakBeforeMake()

def SCPI_Instrument_Setup():
    global Chroma_address
    global DAQ_address
    rm = pyvisa.ResourceManager()
    Resource_list = []
    Resource_list = rm.list_resources()

    if not Resource_list:
        print("nothing connected.  Please connect and try again")
        main()
    else:
        for x in range(len(Resource_list)):
            print("\n\nInstrument Selection:")
            print("|Inst #| Instrument Address|")
            print(" " + str(x) + "       " + Resource_list[x])
            #print(DAQ_list[x])
        Chroma_comp = int(input("\nType *CHROMA* Instrument number to connect (9 to exit):    "))  
        DAQ_comp = int(input("\nType *DAQ* Instrument number to connect (9 to exit):    "))  
        
        #add error check input against list for out of range condition
        if Chroma_comp == 9 or DAQ_comp == 9:
            main()
        if Chroma_comp +1 <= len(Resource_list) and Chroma_comp >= 0:
            Chroma_address = str(Resource_list[Chroma_comp])  
        if DAQ_comp +1 <= len(Resource_list) and DAQ_comp >= 0:
            DAQ_address = str(Resource_list[DAQ_comp])  
        else:
            print("Error!  Input out of range.  Please enter it again.")
            SCPI_Instrument_Setup()
        if Chroma_address in Resource_list:
            myChroma = rm.open_resource(Chroma_address)
            Chroma_status = myChroma.query("*IDN?") 
            print("Chroma Serial: " + Chroma_status) 
        if DAQ_address in Resource_list:
            my34970A = rm.open_resource(DAQ_address)
            DAQ_status = my34970A.query("*IDN?")
            print("DAQ Serial: " + DAQ_status)
        else:
            print("ERROR - Check DAQ Connection")
            app_log.debug("ERROR - Check DAQ Connection.  Something isn't right.")
            SCPI_Instrument_Setup()
def CELL_DISCHARGE():
    #cell discharge
    global Chroma_address
    global DAQ_address
    rm = pyvisa.ResourceManager()
    myChroma = rm.open_resource(Chroma_address)
    my34970A = rm.open_resource(DAQ_address)
    print("cell discharge for 3 minutes") #3min is for test 10 min for live
    #debug
    #time.sleep(3)
    #myChroma = rm.open_resource(Chroma_address)
    #Chroma_status = myChroma.query("*IDN?") 
    #print("Chroma Serial:" + Chroma_status)
    #print("Line - 449") 
    #time.sleep(3)
    #my34970A = rm.open_resource(DAQ_address)
    DAQ_status = my34970A.query("*IDN?")
    print("DAQ Serial:" + DAQ_status)
    myChroma.write('CHAN 1') #discharge
    myChroma.write('MODE CCL')
    myChroma.write('CURR:STAT:L1 ' + str(Discharge_curr)) #CC, static, ch 1 (discharge), 1A
    myChroma.write('LOAD ON')
    
    my34970A.write("ROUT:OPEN (@202,204,206,208,210,212,214,216,218)") #unaffected / set to discharge
    #debug*******************************************************************
    my34970A.write("ROUT:OPEN (@302,304,306,308,310,312,314,316,318)") #unaffected / set to discharge
    #debug*******************************************************************
    my34970A.write("ROUT:CLOS (@201,203,205,207,209,211,213,215,217,219)") #affected / set for in circuit
    #debug*******************************************************************
    my34970A.write("ROUT:CLOS (@301,303,305,307,309,311,313,315,317,319)") #affected / set for in circuit
    #debug*******************************************************************
    for countdown in range(180,0,-1):
        print(str(countdown) + ": Seconds Remaining - initial discharge")
        max_range = Num_samples + 101
        for t in range(101,max_range,1):
            code = 200 + (t);
            print(code)
            #serialcomm.write(str(code).encode())
            my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@' + str(t) + ')')
            voltage = float(my34970A.read())
            print("Voltage for Channel " + str(t) + " = " + str(voltage) + " VDC")
        if msvcrt.kbhit():
            ASCII_in = ord(msvcrt.getche())
            if ASCII_in == 120:
                break
        time.sleep(1)
def EDLC_DOUBLE_CONFIGURE():
    global Chroma_address
    global DAQ_address
    global Sample_curr, Discharge_curr, EDLC_VR
    #Settings()
    rm = pyvisa.ResourceManager()
    myChroma = rm.open_resource(Chroma_address)
    my34970A = rm.open_resource(DAQ_address)
    #init
    myChroma.write('CONF:REM ON') #enable chroma for remote commands
    myChroma.write('*CLS')
    myChroma.write('ABOR')
    my34970A.timeout=5000
    my34970A.write('*CLS')
    my34970A.write('*RST')
    #add modification to scanlist derived from user input
    scanlist = "(@101:120)"
    my34970A.write("CONF:VOLT:DC AUTO, DEF," + scanlist)
    my34970A.write("ROUTE:SCAN " + scanlist)
    my34970A.write("ROUT:CHAN:DELAY:AUTO ON," + scanlist)
    #chroma configure
    myChroma.write('CHAN 1') #discharge
    myChroma.write('MODE CCL')
    myChroma.write('CURR:STAT:L1 ' + str(Discharge_curr)) #CC, static, ch 1 (discharge), 1A
    myChroma.write('LOAD ON')
    myChroma.write('CHAN 3') #charge
    myChroma.write('MODE CCL')
    myChroma.write('CURR:STAT:L1 ' + str(Sample_curr)) #CC, static, ch 3 (charge), A = 0.2A * num samples
    myChroma.write('LOAD ON')    
    myChroma.write('CHAN 5')
    myChroma.write('MODE CV')
    myChroma.write('VOLT:L1 ' + str(EDLC_VR) +'V')  #myChroma.write('VOLT:L1 3V')
    myChroma.write('VOLT:CURR ' + str(Sample_curr)) #debug
    myChroma.write('LOAD ON')
    #34970A configure
    my34970A.write("ROUT:OPEN (@201:220,301:320)") #starting position //open = unaffected, close = affected
    print("setup complete")
    time.sleep(1)
def EDLC_DOUBLE_CC_CHARGE():
    global Chroma_address
    global DAQ_address
    global EDLC_VR, Num_samples
    rm = pyvisa.ResourceManager()
    myChroma = rm.open_resource(Chroma_address)
    my34970A = rm.open_resource(DAQ_address)
    #CC Charge all cells to (0.95 * EDLC_VR e.g. 3V cell = 2.85V)
    EDLC_0p95 = round((EDLC_VR * .95),3)
    print("Charging all cells to " + str(EDLC_0p95) + " V. Press 'x' to cancel.")
    my34970A.write("ROUT:OPEN (@201,203,205,207,209,211,213,215,217,219)") #disconnect cells
    time.sleep(.2)
    #debug***********************************************
    my34970A.write("ROUT:OPEN (@301,303,305,307,309,311,313,315,317,319)") #disconnect cell
    #debug***********************************************
    my34970A.write("ROUT:CLOS (@202,204,206,208,210,212,214,216,218)") #set cells to charge mode
    #debug***********************************************
    my34970A.write("ROUT:CLOS (@302,304,306,308,310,312,314,316,318)") #set cells to charge mode
    #debug***********************************************
    my34970A.write("ROUT:OPEN (@220)") #Connect to CHROMA CC Charge mode on Chan 3 --JN check this line for CC CV mode correctness
    time.sleep(.2)
    my34970A.write("ROUT:CLOS (@201,203,205,207,209,211,213,215,217,219)") #connect all cells
    #debug***********************************************
    my34970A.write("ROUT:CLOS (@301,303,305,307,309,311,313,315,317,319)") #connect all cells
    #debug***********************************************
    CC_charge = True
    counter_volt = 0
    allDUT_Volt = []
    #code = 101
    #serialcomm.write(str(code).encode())
    #ran = False
    while CC_charge == True:
        #debug**********************************************************
        #my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@118)') #was 101
        #debug**********************************************************
        #voltage_charge = float(my34970A.read()) #DEBUG
        
        #measure all cap voltages and make a decision based on any of their voltages
        '''
        if ran == False:    
            for caps in range(101,101+Num_samples,1):
                code = 100 + ( caps - 100 )
                code = 100 + ( caps - 100 )
                print(code)
                serialcomm.write(str(code).encode())
                ran = True
            '''

        for caps in range(101,101+Num_samples,1):
            my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@" + str(caps) +")")
            voltage_charge = float(my34970A.read()) - 0.375
            allDUT_Volt.append(voltage_charge)
            allDUT_Volt.append(voltage_charge)

        #print all cap voltage
        for z in range (len(allDUT_Volt)):
            print("CC chrg DUT " + str(allDUT_Volt[z]) + "Volts")
        #if counter_volt == 10:
        #for index, element in enumerate(allDUT_Volt):
        #    print("DUT", index+1, " = ", element, " V")
        #    counter_volt = 0
        for elem in allDUT_Volt:
            if elem < (EDLC_VR * .95):
                CC_charge = True
                counter_volt += 1
            if elem >= EDLC_VR:
                #disconnect load
                print("DUT ",elem," Voltage >= EDLC Rated Voltage.  Turning Load OFF")
                myChroma.write('CHAN 1')
                myChroma.write('LOAD OFF')
                CC_charge = False
            if elem >= (EDLC_VR * .95) and elem < (EDLC_VR):
                print("CC charge - DUT voltage satisified.  Calling next function")
                CC_charge = False
        '''
        #debug slow print
        if counter_volt == 10:
            print("DUT voltage = " + str(voltage_charge) + " - CC charge")
            counter_volt = 0
        time.sleep(.2) #DEBUG
        if voltage_charge < (EDLC_VR * .95): 
            CC_charge = True
            counter_volt += 1
        if voltage_charge >= EDLC_VR:
            #disconnect DUT
            print("DUT Voltage >= EDLC Rated Voltage.  Turning Load OFF")
            myChroma.write('CHAN 1')
            myChroma.write('LOAD OFF')
            CC_charge = False'''
        if msvcrt.kbhit():
            ASCII_in = ord(msvcrt.getche())
            if ASCII_in == 120:
                CC_charge = False
        #if voltage_charge >= (EDLC_VR * .95) and voltage_charge < EDLC_VR:
        #    CC_charge = False
    '''#CC Charge all cells to (0.95 * EDLC_VR e.g. 3V cell = 2.85V)
    print("Charging all cells to " + str(EDLC_VR * .95) + " . Press 'x' to cancel.")
    # Update for 18 DUTs
    my34970A.write("ROUT:OPEN (@201,203,205,207,209,211,213,215,217)") #disconnect cells in slot 2
    time.sleep(.2)
    #my34970A.write("ROUT:OPEN (@301,303,305,307,309,311,313,315,317,319)") #disconnect cells in slot 3
    time.sleep(.2)
    print("Charging DUT(s) " + str(Num_samples))
    my34970A.write("ROUT:OPEN (@202,204,206,208,210,212,214,216,218)") #set cells in slot 2 to charge mode
    time.sleep(.2)
    #my34970A.write("ROUT:OPEN (@302,304,306,308,310,312,314,316,318,320)") #set cells in slot 3 to charge mode
    my34970A.write("ROUT:OPEN (@220)") #Connect to CHROMA CC Charge mode on Chan 3
    time.sleep(.2)
    my34970A.write("ROUT:CLOS (@201,203,205,207,209,211,213,215,217)") #connect all cells in slot 2
    time.sleep(.2)
    #my34970A.write("ROUT:CLOSE (@301,303,305,307,309,311,313,315,317,319)") #connect all cells in slot 3
    CC_charge = True
    counter_volt = 0
    while CC_charge == True:
        #dut_channel = 101
        #for dut_channel in range(101,120): # Update to run through cells in slot 1
            #my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@' + str(dut_channel) + ')')
            my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@101)') #DEBUG // need to add voltage measurement of other cells taking into account cell health
            voltage_charge = float(my34970A.read()) #DEBUG
            #debug slow print
            if counter_volt == 10:
                #print("DUT channel "+ str(dut_channel) + " voltage = " + str(voltage_charge) + " - CC charge")
                print("DUT voltage = " + str(voltage_charge) + " - CC charge")
                counter_volt = 0
                #dut_channel += 1
            time.sleep(.2) #DEBUG
            if voltage_charge < (EDLC_VR * .95): 
                CC_charge = True
                counter_volt += 1
            if voltage_charge >= EDLC_VR:
                #disconnect DUT
                print("DUT Voltage >= EDLC Rated Voltage.  Turning Load OFF")
                myChroma.write('CHAN 1')
                myChroma.write('LOAD OFF')
                CC_charge = False
            if msvcrt.kbhit():
                ASCII_in = ord(msvcrt.getche())
                if ASCII_in == 120:
                    CC_charge = False
                    break
            if voltage_charge >= (EDLC_VR * .95) and voltage_charge < EDLC_VR:
                CC_charge = False
        '''
def EDLC_DOUBLE_CV_CHARGE():
    global Chroma_address
    global DAQ_address
    global voltage_preESR, Num_samples
    global EDLC_VR
    TARGET_VR = EDLC_VR - 0.1
    rm = pyvisa.ResourceManager()
    myChroma = rm.open_resource(Chroma_address)
    my34970A = rm.open_resource(DAQ_address)
    #set constant voltage charge
    # Update for 18 DUTs
    my34970A.write("ROUT:OPEN (@201,203,205,207,209,211,213,215,217)") #disconnect cells in slot 2
    my34970A.write("ROUT:OPEN (@301,303,305,307,309,311,313,315,317,319)") #disconnect cells in slot 3
    print("Switching to channel 5 with CV")
    my34970A.write("ROUT:CLOS (@220)") #Switch to CHAN 5 for CV mode
    time.sleep(0.2)
    my34970A.write("ROUT:CLOS (@201,203,205,207,209,211,213,215,217)") #connect cells in slot 2
    my34970A.write("ROUT:CLOS (@301,303,305,307,309,311,313,315,317,319)") #connect cells in slot 3
    time.sleep(0.2)
    #hold charge for 30 minutes
    print("hold charge for 30 minutes  x to abort")
    allDUT_Volt = []
    for countdown in range(1800,0,-1):
        print(str(countdown) + ": Seconds Remaining - CV Charge")
        '''max_range = Num_samples + 101
        for z in range(101,max_range,1):
            my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@' + str(z) + ')')
            voltage_preESR = float(my34970A.read())
            print("Voltage for Channel " + str(z) + " = " + str(voltage_preESR) + " VDC\n")'''
        #debug*********************************************
        #my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@118)')
        #voltage_preESR = float(my34970A.read())
        DUT_switch = [201,203,205,207,209,211,213,215,217,301,303,305,307,309,311,313,315,317,319]

        for caps in range(101,101+Num_samples,1):
            code = 100 + ( caps - 100 )
            #print(code)
            #serialcomm.write(str(code).encode())
            my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@" + str(caps) +")")
            voltage_cv = float(my34970A.read())
            #allDUT_Volt.append(voltage_cv)
            allDUT_Volt.insert((100+Num_samples)-caps, voltage_cv)
            #allDUT_Volt[caps - 101] = voltage_cv
            #if allDUT_Volt[caps - 101] >= (EDLC_VR - 0.1):
            if (allDUT_Volt[-1] >= TARGET_VR):
                #disconnect DUT
                print("DUT Voltage >= EDLC Rated Voltage.  Disconnecting DUT")
                print(allDUT_Volt[caps - 101])
                print(allDUT_Volt[-1])
                print("------")
                print("List = :" + str(allDUT_Volt))
                #debug***********************************************
                my34970A.write("ROUT:OPEN (@"+ str(DUT_switch[caps - 101]) +")") #disconnect offending DUT switch
            else:
                print("List = :" + str(allDUT_Volt))
                print('DUT Voltage < EDLC Rated Voltage.  Connecting DUT')
                my34970A.write("ROUT:CLOSE (@"+ str(DUT_switch[caps - 101]) +")") #connect DUT
        #debug*********************************************
        time.sleep(1)
        if msvcrt.kbhit():
            ASCII_in = ord(msvcrt.getche())
            if ASCII_in == 120:
                break
        # Check if voltage exceeds 2.9V
        '''if voltage_preESR >= EDLC_VR - 0.1:
            #disconnect DUT
            print("DUT Voltage >= EDLC Rated Voltage.  Disconnecting DUT")
            #debug***********************************************
            my34970A.write("ROUT:OPEN (@317)") #d/c DUT 1 #was 201 
            #debug***********************************************
        else:
            #debug***********************************************
            print('DUT Voltage < EDLC Rated Voltage.  Connecting DUT')
            my34970A.write("ROUT:CLOSE (@317)") #Connect DUT 1 was 201
            #debug***********************************************'''
def EDLC_MultiEDLC_Discharge():
    global Chroma_address
    global DAQ_address
    global D1_CC_elapsed, D1_volt1, D1_volt3, D1_ESR, voltage_preESR, Discharge_curr, DUT_C, Num_samples

    rm = pyvisa.ResourceManager()
    myChroma = rm.open_resource(Chroma_address)
    my34970A = rm.open_resource(DAQ_address)
    print("Multi DUT Discharge")
    DUT_chr_dchr = [202,204,206,208,210,212,214,216,218,302,304,306,308,310,312,314,316,318,320]
    DUT_200_switch = [201,203,205,207,209,211,213,215,217]
    DUT_300_switch = [301,303,305,307,309,311,313,315,317,319]
    DUT_measure = [101,0,102,0,103,0,104,0,105,0,106,0,107,0,108,0,109,0,110,0,111,0,112,0,113,0,114,0,115,0,116,0,117,0,118,0,119]
    if Num_samples <= 9:
        for cap in range(201,DUT_200_switch[Num_samples-1]+1,2):
            code = 300 + ( cap - 200 )
            print(code)
            print(300 + ( cap - 200 ))
            #serialcomm.write(str(code).encode())
            my34970A.write("ROUT:OPEN (@"+ str(cap) +")") #d/c DUT
            my34970A.write("ROUT:OPEN (@"+ str(cap+1) +")") #dch DUT
            my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
            V_preESR = float(my34970A.read()) 
            my34970A.write("ROUT:CLOS (@"+ str(cap) +")") #con DUT
            my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
            V_posESR = float(my34970A.read()) 
            ESR1 = (V_preESR - V_posESR) / Discharge_curr
            print("ESR1 of DUT " + str(100-DUT_measure[cap-201])+ " = "+ str(round(ESR1,3))+"Ω") #print ESR1
            my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
            Volt1 = float(my34970A.read())
            while Volt1 > (EDLC_VR * 0.8):
                my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
                Volt1 = float(my34970A.read())
                print("DUT "+ str(100-DUT_measure[cap-201])+ " = " +str(round(Volt1,3)) +" V")
                if msvcrt.kbhit():
                    ASCII_in = ord(msvcrt.getche())
                    if ASCII_in == 120:
                        break
            start_time = timer() #when voltage passes 2.4V for 3V cell start timer()
            print("DUT voltage is at 0.8 * rated voltage... start timer")
            my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
            Volt2 = float(my34970A.read()) + 0.3
            while Volt2 > (EDLC_VR * .4):
                my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
                Volt2 = float(my34970A.read())
                print("DUT "+ str(100-DUT_measure[cap-201])+ " = " +str(round(Volt2,3)) +" V")
                if msvcrt.kbhit():
                    ASCII_in = ord(msvcrt.getche())
                    if ASCII_in == 120:
                        break
            end_time = timer()
            my34970A.write("ROUT:OPEN (@"+ str(cap) +")") #d/c DUT
            Time_elapsed = end_time - start_time
            print("Elapsed time = "+ str(Time_elapsed))
            DUT_C = Discharge_curr * Time_elapsed / (Volt1 - Volt2)
            print("DUT Capacitance = " + str(round(DUT_C,3)) + "F") 
            my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
            Volt3 = float(my34970A.read())
            for esr_time in range(0,5,1):
                print("ESR 2 waiting... " + str(esr_time) + " seconds")
                time.sleep
            my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
            Volt4 = float(my34970A.read())
            ESR2 = (Volt4 - Volt3)/Discharge_curr
            print("ESR2 = " + str(ESR2) + " Ω")
            #save values to CSV to be completed
            #discharge cell for handling
            my34970A.write("ROUT:CLOS (@"+ str(cap) +")") #con DUT
            while Volt4 <=0.3:
                my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
                Volt4 = float(my34970A.read())
                print("Discharging.  V = " + str(Volt4))
            print("Discharge complete")
    if Num_samples > 9:
        for cap in range(201,DUT_200_switch[8]+1,2):
            code = 300 + ( cap - 200 )
            print(code)
            print(300 + ( cap - 200 ))
            my34970A.write("ROUT:OPEN (@"+ str(cap) +")") #d/c DUT
            my34970A.write("ROUT:OPEN (@"+ str(cap+1) +")") #dch DUT
            my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
            V_preESR = float(my34970A.read()) 
            my34970A.write("ROUT:CLOS (@"+ str(cap) +")") #con DUT
            my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
            V_posESR = float(my34970A.read()) 
            ESR1 = (V_preESR - V_posESR) / Discharge_curr
            print("ESR1 of DUT " + str(100-DUT_measure[cap-201])+ " = "+ str(round(ESR1,3))+"Ω") #print ESR1
            my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
            Volt1 = float(my34970A.read())
            while Volt1 > (EDLC_VR * 0.8):
                my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
                Volt1 = float(my34970A.read())
                print("DUT "+ str(100-DUT_measure[cap-201])+ " = " +str(round(Volt1,3)) +" V")
                if msvcrt.kbhit():
                    ASCII_in = ord(msvcrt.getche())
                    if ASCII_in == 120:
                        break
            start_time = timer() #when voltage passes 2.4V for 3V cell start timer()
            print("DUT voltage is at 0.8 * rated voltage... start timer")
            my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
            Volt2 = float(my34970A.read()) + 0.3
            while Volt2 > (EDLC_VR * .4):
                my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
                Volt2 = float(my34970A.read())
                print("DUT "+ str(100-DUT_measure[cap-201])+ " = " +str(round(Volt2,3)) +" V")
                if msvcrt.kbhit():
                    ASCII_in = ord(msvcrt.getche())
                    if ASCII_in == 120:
                        break
            end_time = timer()
            my34970A.write("ROUT:OPEN (@"+ str(cap) +")") #d/c DUT
            Time_elapsed = end_time - start_time
            print("Elapsed time = "+ str(Time_elapsed))
            DUT_C = Discharge_curr * Time_elapsed / (Volt1 - Volt2)
            print("DUT Capacitance = " + str(round(DUT_C,3)) + "F") 
            my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
            Volt3 = float(my34970A.read())
            #time.sleep(5) #make this a non-blocking function
            for esr_time in range(0,5,1):
                print("ESR 2 waiting... " + esr_time + " seconds")
                time.sleep(1)
            my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
            Volt4 = float(my34970A.read())
            ESR2 = (Volt4 - Volt3)/Discharge_curr
            print("ESR2 = " + str(ESR2) + " Ω")
            #save values to CSV
            #discharge cell for handling
            my34970A.write("ROUT:CLOS (@"+ str(cap) +")") #con DUT
            while Volt4 <=0.3:
                my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
                Volt4 = float(my34970A.read())
                print("Discharging.  V = " + str(Volt4))
            print("Discharge complete")
        for cap in range(301,DUT_300_switch[Num_samples-1]+1,2):
                my34970A.write("ROUT:OPEN (@"+ str(cap) +")") #d/c DUT
                my34970A.write("ROUT:OPEN (@"+ str(cap+1) +")") #dch DUT
                my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[(cap-301)+18]) +")") #measure DUT
                V_preESR = float(my34970A.read()) 
                my34970A.write("ROUT:CLOS (@"+ str(cap) +")") #con DUT
                my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[(cap-301)+18]) +")") #measure DUT
                V_posESR = float(my34970A.read()) 
                ESR1 = (V_preESR - V_posESR) / Discharge_curr
                print("ESR1 of DUT " + str(100-DUT_measure[(cap-301)+18])+ " = "+ str(round(ESR1,3))+"Ω") #print ESR1
                my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[(cap-301)+18]) +")") #measure DUT
                Volt1 = float(my34970A.read())
                while Volt1 > (EDLC_VR * 0.8):
                    my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[(cap-301)+18]) +")") #measure DUT
                    Volt1 = float(my34970A.read())
                    print("DUT "+ str(100-DUT_measure[(cap-301)+18])+ " = " +str(round(Volt1,3)) +" V")
                    if msvcrt.kbhit():
                        ASCII_in = ord(msvcrt.getche())
                        if ASCII_in == 120:
                            break
                start_time = timer() #when voltage passes 2.4V for 3V cell start timer()
                print("DUT voltage is at 0.8 * rated voltage... start timer")
                my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[(cap-301)+18]) +")") #measure DUT
                Volt2 = float(my34970A.read())
                while Volt2 > (EDLC_VR * .4):
                    my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[(cap-301)+18]) +")") #measure DUT
                    Volt2 = float(my34970A.read())
                    print("DUT "+ str(100-DUT_measure[(cap-301)+18])+ " = " +str(round(Volt2,3)) +" V")
                    if msvcrt.kbhit():
                        ASCII_in = ord(msvcrt.getche())
                        if ASCII_in == 120:
                            break
                end_time = timer()
                my34970A.write("ROUT:OPEN (@"+ str(cap) +")") #d/c DUT
                Time_elapsed = end_time - start_time
                print("Elapsed time = "+ str(Time_elapsed))
                DUT_C = Discharge_curr * Time_elapsed / (Volt1 - Volt2)
                print("DUT Capacitance = " + str(round(DUT_C,3)) + "F") 
                my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[(cap-301)+18]) +")") #measure DUT
                Volt3 = float(my34970A.read())
                #time.sleep(5) #make this a non-blocking function
                for esr_time in range(0,5,1):
                    print("ESR 2 waiting... " + esr_time + " seconds")
                    time.sleep(1)
                my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[(cap-301)+18]) +")") #measure DUT
                Volt4 = float(my34970A.read())
                ESR2 = (Volt4 - Volt3)/Discharge_curr
                print("ESR2 = " + str(ESR2) + " Ω")
                #save values to CSV
                #discharge cell for handling
                my34970A.write("ROUT:CLOS (@"+ str(cap) +")") #con DUT
                while Volt4 <=0.3:
                    my34970A.write("MEAS:VOLTAGE:DC? AUTO, DEF, (@"+ str(DUT_measure[cap-201]) +")") #measure DUT
                    Volt4 = float(my34970A.read())
                    print("Discharging.  V = " + str(Volt4))
                print("Discharge complete")
def EDLC_DOUBLE_DUT1_DISCHARGE():
    global Chroma_address
    global DAQ_address
    global D1_CC_elapsed, D1_volt1, D1_volt3, D1_ESR, voltage_preESR, Discharge_curr, DUT_C

    rm = pyvisa.ResourceManager()
    myChroma = rm.open_resource(Chroma_address)
    my34970A = rm.open_resource(DAQ_address)
    #DUT 1 to discharge, CC Load On
    print("DUT18 CC Discharge")
    #debug***********************************************
    my34970A.write("ROUT:OPEN (@317)") #d/c DUT 1 #was 201
    #debug***********************************************
    time.sleep(0.2)
    #debug***********************************************
    my34970A.write("ROUT:OPEN (@318)") #discharge #was 202
    #debug***********************************************
    #debug***********************************************
    my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@118)') #was 101
    #debug***********************************************
    voltage_preESR = float(my34970A.read()) #debug

    #pre_time = timer()
    
    #debug***********************************************
    my34970A.write("ROUT:CLOS (@317)") #connect DUT 18 was 201
    my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@118)') #was 101
    #debug***********************************************
    D1_volt1 = float(my34970A.read())
    D1_ESR = (voltage_preESR - D1_volt1) / Discharge_curr

    #post_time = timer()
    #total_time = post_time - pre_time #mod 111623
    #print("Total time = " + str(total_time) + " seconds")
    print("D18 ESR = "+ str(round(D1_ESR,3)) +" Ω\n") #mod 111623
    #debug***********************************************
    my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@118)') #was 101
    #debug***********************************************
    D1_volt1 = float(my34970A.read())
    while D1_volt1 > (EDLC_VR * .8):
        #debug***********************************************
        my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@118)') #was 101
        #debug***********************************************
        D1_volt1 = float(my34970A.read())
        print("DUT18 voltage = " + str(D1_volt1)) #DEBUG
        if msvcrt.kbhit():
            ASCII_in = ord(msvcrt.getche())
            if ASCII_in == 120:
                break
    start_time = timer() #when voltage passes 2.4V for 3V cell start timer()
    print("DEBUG: DUT voltage is at 0.8 * rated voltage... start timer")
    #print("start timer = " + str(start_time))

    #debug***********************************************
    my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@118)')
    #debug***********************************************
    D1_volt3 = float(my34970A.read())

    while D1_volt3 > (EDLC_VR * .4):
        #debug***********************************************
        my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@118)') #was 101
        #debug***********************************************
        D1_volt3 = float(my34970A.read())
        print("DUT18 voltage = " + str(D1_volt3)) #DEBUG
       # time.sleep(0.2)
        if msvcrt.kbhit():
            ASCII_in = ord(msvcrt.getche())
            if ASCII_in == 120:
                break
    end_time = timer()
    #debug***********************************************
    my34970A.write("ROUT:OPEN (@317)") #disconnect DUT 1 ADD ESR2 measurement was 201
    #debug***********************************************
    D1_CC_elapsed = end_time - start_time
    #print("End time = " + str(end_time))
    print("Elapsed time = "+ str(D1_CC_elapsed))
    DUT_C = Discharge_curr * D1_CC_elapsed / (D1_volt1 - D1_volt3)
    print("DUT Capacitance = " + str(round(DUT_C,3)) + "F")

def EDLC_DOUBLE_SAFE_DISCHARGE():
    global Chroma_address
    global DAQ_address
    global Num_samples
    rm = pyvisa.ResourceManager()
    myChroma = rm.open_resource(Chroma_address)
    my34970A = rm.open_resource(DAQ_address)
    #safe discharge
    print("safe discharge")
    #debug***********************************************
    my34970A.write("ROUT:CLOS (@201)") #connect DUT18 was 201
    #debug***********************************************
    #debug***********************************************
    my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@101)') #was 101
    #debug***********************************************
    D1_volt4 = float(my34970A.read())
    while D1_volt4 >= 0.4:
        #debug***********************************************
        my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@118)') #was 101
        #debug***********************************************
        D1_volt4 = float(my34970A.read())
        print("DUT18 voltage = " + str(D1_volt4))
        time.sleep(0.2)
        if msvcrt.kbhit():
            ASCII_in = ord(msvcrt.getche())
            if ASCII_in == 120:
                break
    print("Safe discharge complete")
    code=201
    #serialcomm.write(str(code).encode())

def EDLC_ESR2():
    global Chroma_address
    global DAQ_address
    global DUT1_ESR2, Discharge_curr, D1_CC_elapsed, D1_volt1, D1_volt3, D1_ESR, DUT_C
    rm = pyvisa.ResourceManager()
    my34970A = rm.open_resource(DAQ_address)
    #ESR 2 Measurement
    #measure voltage
    #debug***********************************************
    my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@118)') #was 101
    #debug***********************************************
    D1_low = float(my34970A.read())
    #debug***********************************************
    my34970A.write("ROUT:OPEN (@317)") #disconnect DUT8
    #debug***********************************************
    #wait 5 seconds
    time.sleep(5)
    #measure voltage
    #debug***********************************************
    my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@118)') #was 101
    #debug***********************************************
    D1_high = float(my34970A.read())
    #calculate esr
    DUT1_ESR2 = (D1_high - D1_low)/Discharge_curr
    print("ESR2 = " + str(DUT1_ESR2) + " Ω")

    print("DUT18 complete")
    D1_C = Discharge_curr * (D1_CC_elapsed / (D1_volt1 - D1_volt3)) 
    print("D1 C = " + str(D1_C) + " F")
    print("\nD1 ESR = "+ str(D1_ESR) +" Ω\n")

def Hardcode_Settings():
    global Sample_curr, Discharge_curr, Num_samples, Charge_curr, EDLC_VR
    EDLC_VR = 3
    Charge_curr = .25
    Discharge_curr = .2
    Num_samples = 1
    
def EDLC_DOUBLE():
    '''Note:  discharge/charge relay; close = charge, open = discharge.  disconnect relay; open = disconnect, close = connect. 
    Charge mode relay; open = CC, close = CV'''
    global Chroma_address
    global DAQ_address
    global Num_samples
    global Sample_curr
    global Discharge_curr
    global Charge_curr, D1_CC_elapsed, D1_volt1, D1_volt3, D1_ESR

    print("\nEDLC Measurement.  This Function will measure 1x EDLC in position 18 (DUT 18)\n")
    SCPI_Instrument_Setup()
    
    Hardcode_Settings()
    
    Sample_curr = Num_samples * Charge_curr 
    #Num_samples = int(input("Enter the number of samples to test: (hint: start with 1)"  ))
    
    #Discharge_curr = .5 

    EDLC_DOUBLE_CONFIGURE()
    CELL_DISCHARGE()
    EDLC_DOUBLE_CC_CHARGE()
    EDLC_DOUBLE_CV_CHARGE()
    #EDLC_DOUBLE_DUT1_DISCHARGE()
    EDLC_MultiEDLC_Discharge()
    #EDLC_ESR2()
    EDLC_DOUBLE_SAFE_DISCHARGE()
    
    #housekeeping
    rm = pyvisa.ResourceManager()
    myChroma = rm.open_resource(Chroma_address)
    my34970A = rm.open_resource(DAQ_address)
    myChroma.write('CONF:REM OFF')
    myChroma.close()   
    my34970A.close()      
def Housekeeping():
    global Chroma_address
    global DAQ_address
    print("performing housekeeping of SCPI instruments")
    rm = pyvisa.ResourceManager()
    myChroma = rm.open_resource(Chroma_address)
    my34970A = rm.open_resource(DAQ_address)
    myChroma.write('CONF:REM OFF')
    myChroma.close()   
    my34970A.close()
def EDLC_TEST():
    #DEBUG function
    global Chroma_address
    global DAQ_address
    global test_no
    print("Instrument Command Test")
    SCPI_Instrument_Setup()
    rm = pyvisa.ResourceManager()
    myChroma = rm.open_resource(Chroma_address)
    my34970A = rm.open_resource(DAQ_address)

    Chroma_status = myChroma.query("*IDN?")
    print("Chroma Serial:  " + Chroma_status)
    DAQ_status = my34970A.query("*IDN?")
    print("DAQ Serial:  " + DAQ_status)

    #init
    myChroma.write('CONF:REM ON')
    myChroma.write('*CLS')
    myChroma.write('ABOR')
    my34970A.timeout=5000
    my34970A.write('*CLS')
    my34970A.write('*RST')
    scanlist = "(@101:120)"
    my34970A.write("CONF:VOLT:DC AUTO, DEF," + scanlist)
    my34970A.write("ROUTE:SCAN " + scanlist)
    my34970A.write("ROUT:CHAN:DELAY:AUTO ON," + scanlist)

    #test selection
    Answer = 99
    Answer = int(input("Type Selection:  Chroma Test = 0 | DAQ Test = 1 "))
    if Answer == 0:
        #test 1
        test_no = 1
        print("Chroma Test initiated")
        print("Load 1 and 3 set CC 1A/1.2A LOAD ON")
    
        myChroma.write('CHAN 1')
        myChroma.write('MODE CCL')
        myChroma.write('CURR:STAT:L1 1') #CC, static, ch 1 (charge), 1A
        myChroma.write('LOAD ON')
        
        myChroma.write('CHAN 3')
        myChroma.write('MODE CCL')
        myChroma.write('CURR:STAT:L1 1.2') #CC, static, ch 3 (discharge), 1.2A
        myChroma.write('LOAD ON')

        #Chroma_Poll_Status()

        input("Test 1 complete.  Record the result.  Press any key to continue.")
        
        #test2
        test_no = 2
        print("Load 1 to CV 3V and current 1.2A")
        myChroma.write('CHAN 1')
        myChroma.write('MODE CV')
        myChroma.write('VOLT:L1 3V')
        myChroma.write('VOLT:CURR 1.2')
        myChroma.write('LOAD ON')

        #Chroma_Poll_Status()
      
        input("Test 2 complete.  Record the result.  Press any key to continue.")   

        #test3
        test_no = 3
        print("Load 3 (Discharge) Load OFF")
        myChroma.write('CHAN 3')
        myChroma.write('LOAD OFF')

        #Chroma_Poll_Status()

        input("Test 3 complete.  Record the result.  Press any key to continue.")   

        print('delay 5 seconds')
        time.sleep(5)

        myChroma.write('ABOR')
        myChroma.write('*CLS')
        myChroma.write('CONF:REM OFF')
        myChroma.close()

    if Answer == 1:
        Volt_Skip = int(input("DAQ Test Voltage Test.  Press '1' to continue to Voltage Measurement and any other key to skip."))
        if Volt_Skip == 1:
            #test 1 - verify voltage measurement on each channel
            for t in range(101,121,1):
                my34970A.write('MEAS:VOLTAGE:DC? AUTO, DEF, (@' + str(t) + ')')
                voltage = float(my34970A.read())
                print("Voltage for Channel " + str(t) + " = " + str(voltage) + " VDC")
                input("Record result and press any key to continue")
        
        Bank_response = int(input("Select Switch Card Bank - Bank 2 = 2 and Bank 3 = 3    "))
        if Bank_response == 2:
            #test 2 - verify relay operation
            print("DAQ Switch Test")
            #input("Check relay state unaffected")
            my34970A.write("ROUT:OPEN (@201:220)") #set all relays to starting position
            for x in range(201,221,1):
                input("Check relay state of channel " + str(x) + " unaffected and press that NE key when done")
                my34970A.write("ROUT:CLOS (@" + str(x) + ")")
                input("Check relay state of channel " + str(x) + " affected and press that NE key when done")
        if Bank_response == 3:
        #input 2 for the second set
            my34970A.write("ROUT:OPEN (@301:320)") #set all relays to starting position
            for x in range(301,321,1):
                input("Check relay state of channel " + str(x) + " unaffected and press that NE key when done")
                my34970A.write("ROUT:CLOS (@" + str(x) + ")")
                input("Check relay state of channel " + str(x) + " affected and press that NE key when done")
        else:
            print("input out of range. back to EDLC Test function")
            EDLC_TEST()
        my34970A.close()

def Settings():
    global datafilename, logfilename, wait_time, inputfilename, logfilepath, datafilepath, app_log
    global Sample_curr, Discharge_curr, Num_samples, Charge_curr, EDLC_VR

    #defaults
    EDLC_VR = 3
    Charge_curr = .25
    Discharge_curr = .2
    Num_samples = 1


    ans=True
    while ans:
        print("""
        1. change data file name
        2. change log file name
        3. change input file name
        4. change log file path
        5. set EDLC rated voltage
        6. set number of EDLCs to test
        7. set charge current
        8. set discharge current
        9. exit
        """)
        ans=input('Enter Selection:  ')
        if ans == "1":
            datafilename = input('\nEnter the new name of the data without file extension (DEF "ATE"):  ')
        if ans == "2":
            logfilename = input('\nEnter the new name of the log file without file extension (DEF "Log"): ')
        if ans == "3":
            inputfilename = input('\nEnter the new name of the input file without file extension (DEF "LANIDLIST"):  ')
        if ans=="4":
           logfilepath = input('\nEnter the new path to the log file (DEF "C:\\HQA\Software\\"): ')
           logdata()
        if ans == "5":
            #wait_time = int(input('Enter the DUT scan wait time in seconds:  '))
            EDLC_VR = int(input('\nEnter the rated voltage for the supercaps you want to measure.\n<<Note: all EDLCs tested should be the same>>:  '))
        if ans == "6":
            Num_samples = int(input('\nEnter number of EDLCs to test:  '))
            if Num_samples > 19 or Num_samples == 0:
                Num_samples = int(input("Number is out of range. e.g. 0 < n < 20\nPlease enter a number within range:  "))
        if ans == "7":
            Charge_curr = int(input('\nSet Charge current in Amps:  '))
        if ans == "8":
            Discharge_curr = int(input('\nSet Discharge current in Amps:  '))
        if ans == "9":
            print("\nGoodbye!")
            print("data file name = ", datafilename)
            print("log file name = ", logfilename)
            print("DUT wait time(s) = ", wait_time)
            print("Input file name = ", inputfilename)
            print("Logfilepath = ", logfilepath)
            print("EDLC Rated Voltage = ", EDLC_VR)
            print("Number of EDLCs to test = ", Num_samples)
            print("Charge current = " + str(Charge_curr) + "A")
            print("Discharge current = " + str(Discharge_curr) + "A")
            main()
        '''elif ans != "":
            print('invalid selection.  try again.')'''
def main():
   global counter, settings_flag
   global datafilename
   global logfilename
   global wait_time
   global inputfilename

   counter = 0
   #Settings()
   #logging.basicConfig(filename="Amazon Current Log.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
   #from logging.handlers import RotatingFileHandler
   #log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

   #logFile = 'C:\\HQA\\Software\\' + logfilename + '.log'
   #my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)
   #my_handler.setFormatter(log_formatter)
   #my_handler.setLevel(logging.DEBUG)

   #app_log = logging.getLogger('root')
   #app_log.setLevel(logging.DEBUG)
   #app_log.addHandler(my_handler)

   menu = { "S": ("Settings", Settings),
            #"C" : ("Equipment Init", EDLC_TEST),
            "T" : ("EDLC Test (DOUBLE)", EDLC_DOUBLE),
            "E": ("Erase CSV", DestroyFile),
            #"Q": ("Equipment Housekeeping", Housekeeping),
            "X": ("Exit", Exit)}

   ans=True
   while ans:
      print("")
      print("EDLC Tester - Multiple Cell Test")
      #app_log.debug("Current Measurement v.002")
      for key in menu.keys():
         print( "  " + key + ": " + menu[key][0] )

      print("")

      ans = input("Make a selection: ")
      menu.get(ans.upper(),[None,InvalidSelection])[1]() #converts to upper case
   sys.exit(0)

if __name__ == "__main__":
    main()