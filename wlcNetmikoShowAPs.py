"""
    This function creates a parsed file of the cisco WLC Aps
    tested Aireos version: 8.3.112.0
    tested on Windows 10 python 3.7
    
    How it works:
        The script reads a file with the list of WLC Ip and hostname
        FileName: wlcList.csv
        Format: 
            wlcName,IpAddress
            wlc-01,192.168.1.1
            wlc-02,192.168.1.2
            wlc-ha,192.168.1.3
            
        Connects to the WLC using SSH;
        Excecutes the commands:
            Config paging disabled;
            show ap summary;
        From the show ap summary output a temporary file is created;
        The script reads the file and parse it creating a DataFrame;
        The scripts outputs a parsed file;
    
    Limitations:
        - Only works for a single country code
        - Creates a temporary file during the parsing process
        
    Author: Diego Capassi Moreira
    Contact: diego.capassi.moreira@gmail.com
    
    Reference: https://netpacket.net/2018/02/scripting-the-wlc/
"""

import time, paramiko, csv, re, os, datetime
import wlcParameters as wlcParameters
import pandas as pd

#countryCode
apCountry = 'BR'

#Getting the username and password from the wlcParameters module
password = wlcParameters.password
username = wlcParameters.username

#Buffersize may be higher depending on the size of the AP list
buffersize = 65535

#Wait time may be tweeked depeding on the latency to reach the WLC.
waitTime = 2

def getApListParsedFile(username, password, hostname,ip):    
    #Establishing SSH connection
    wlc_session = paramiko.SSHClient()
    wlc_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    wlc_session.connect(ip, port='22', username='null', password='null')
    wlc_ssh_class = wlc_session.invoke_shell()
    time.sleep(waitTime)
    wlc_ssh_class.send(username+'\n')
    time.sleep(waitTime)
    wlc_ssh_class.send(password+'\n')
    time.sleep(waitTime)
     #Disabling the paging to avoid asking for confirmation
    wlc_ssh_class.send('config paging disable'+'\n')
    time.sleep(waitTime)
    #Executing the show ap summary command
    wlc_ssh_class.send('show ap summary'+'\n')
    time.sleep(waitTime)
    output = wlc_ssh_class.recv(buffersize).decode('utf-8', 'backslashreplace')
    wlc_session.close()
    #print (output)
    
    #Creating a temporary file to help the parsing process
    #Needs to be improved in future versions
    filePathName = "Temp_outputNotParsed"+".txt"
    file = open(filePathName,'w')
    file.write(output)
    file.close()
    
    file2 = open("Temp_outputNotParsed.txt","r") 
    lines = file2.readlines()
    file2.close()
    os.remove("Temp_outputNotParsed.txt")
    lineList = []

    count = 0
    for line in lines:
            if line != "\n":
                ##Parsing the TABS
                if count >= 32:
                    parsedLine = re.sub(' +',' ', line)
                    lineList.append(parsedLine)
                else:
                    lineList.append(line)
            count = count + 1
            
    #Removing the header, dashline and last line        
    del lineList[0:9]
    del lineList[0]
    del lineList[-1]
        
    ##Parsing the Data
    col_names = ['apName','apSlot','apModel','apMac','apLocation','apCountry','apIp','apAssociations']
    my_df = pd.DataFrame(columns = col_names)
    
    for lines in lineList:
        lineSplitted = lines.split()
        apName = lineSplitted[0]
        apSlot = lineSplitted[1]
        apModel = lineSplitted[2]
        apMacAddress = lineSplitted[3]
        apLocation = lineSplitted[4]
        ##Parsing Ap Group
        count = 4
        while lineSplitted[count+1] != apCountry:
            apLocation = apLocation + " " + lineSplitted[count+1] 
            count = count + 1
        apCountryCode = lineSplitted[count+1]
        apIp = lineSplitted[count+2]
        apAssociations = int((lineSplitted[count+3]))
        my_df.loc[len(my_df)] = [apName,apSlot,apModel,apMacAddress,apLocation,apCountryCode,apIp,apAssociations]
        
    
    #Getting the day, month year to add to the parsed file name
    today = datetime.datetime.today()
    day = str(today.day)
    month = str(today.month)
    year = str(today.year)
    hour = str(today.hour)
    minutes = str(today.minute)
    parsedTime = (month+"-"+day+"-"+year+"_"+hour+"_"+minutes)
        
    ##Writing Parsed File
    filePathName = hostname+"_"+parsedTime+"_Parsed_Data"+".csv"
    export_csv = my_df.to_csv (hostname+"_"+parsedTime+"_Parsed_Data"+".csv", index = None, header=True) #Don't forget to add '.csv' at the end of the path
        
wlc_df = pd.read_csv('wlcList.csv')
count = 0;

#Loop to use the getApList function iterating over the wlcName file
while len(wlc_df['wlcName']) > count:
    wlcHostname = wlc_df['wlcName'][count]
    wlcIP = wlc_df['IpAddress'][count]
    getApListParsedFile(username, password, wlcHostname, wlcIP)
    count = count + 1
    
    
    
    




    
