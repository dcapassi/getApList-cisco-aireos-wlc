# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 11:49:28 2019
This module provides  tools to work with IP format strings
"""

def checkRangeError(ip):
    ip = int (ip)
    if ip < 0:
        errorFormat(ip)
    if ip > 255:
        errorFormat(ip)
    return 0

def errorFormat(ip):
    raise NameError("Format invalid "+str(ip))
    return -1

def ipBinFormat(ip):
    '''
    This Function receives a IP Format value e.g 192.168.1.1
    And converts it to Binary Example 11000000101010000000000100000001
    '''    
    ipSplittedDec = ip.split('.')
        
    ipBin1_Oct = format(int(ipSplittedDec[0]),'08b')
    ipBin2_Oct = format(int(ipSplittedDec[1]),'08b')
    ipBin3_Oct = format(int(ipSplittedDec[2]),'08b')
    ipBin4_Oct = format(int(ipSplittedDec[3]),'08b')
    
    #Checking Errors
    #Throws an error if the format is invalid
    if(len(ipSplittedDec))!=4:
            errorFormat(ipSplittedDec)
            
    checkRangeError(int(ipBin1_Oct,2))
    checkRangeError(int(ipBin2_Oct,2))
    checkRangeError(int(ipBin3_Oct,2))
    checkRangeError(int(ipBin4_Oct,2))
    
    #Executing the Sum
    ipBin = ipBin1_Oct + ipBin2_Oct + ipBin3_Oct + ipBin4_Oct
    return ipBin

def decToBin(dec):
    '''
    This function converts a decimal number to a 8 bit Binary
    ex:
        decToBin(10) -> 00001010
    '''
    return format(int(dec),'08b')    

def binToDec(ip):
    return int(ip,2)
    
def binIpToDecIp(ipBin):
    '''
    This function converts a sequence of 32 bits to decimal
        ipBin = 11000000101010000000000100001010
        192.168.1.10
        binIpToDecIp(ipBin)
    '''
    padding = 32 - len(ipBin)
    ipBinPadded = ''
    for x in range(padding):
        if padding > 0:
            ipBinPadded = ipBinPadded + '0'
        padding = padding - 1
        
    ipBin = ipBinPadded + ipBin
    count = 0
    ipDec1_Oct = ipDec2_Oct = ipDec3_Oct = ipDec4_Oct = ''
    for x in ipBin:
        if count < 8:
            ipDec1_Oct = ipDec1_Oct + str(x)
        if count >= 8 and count < 16:
            ipDec2_Oct = ipDec2_Oct + str(x)
        if count >= 16 and count < 24:
            ipDec3_Oct = ipDec3_Oct + str(x)     
        if count >= 24 and count < 32:
            ipDec4_Oct = ipDec4_Oct + str(x)    
        count = count + 1
           
    ipDec1_Oct = (int(ipDec1_Oct,2))
    ipDec2_Oct = (int(ipDec2_Oct,2))
    ipDec3_Oct = (int(ipDec3_Oct,2))
    ipDec4_Oct = (int(ipDec4_Oct,2))
    
    strIpDec = str(ipDec1_Oct) + '.' + str(ipDec2_Oct) + '.' + str(ipDec3_Oct)\
    + '.' + str(ipDec4_Oct)
    return strIpDec

def sumIpAddress(ip,addend):
    '''
    This function sums an IP eg. 172.16.1.1 to a decimal number.
    ip = 172.16.0.1
    addend = 500
    sumIpAddress(ip,addend)
    172.16.1.245
    '''
    ipBinTotal = format(int(ipBinFormat(ip),2) + int(decToBin(addend),2),'08b')
    
    return binIpToDecIp(ipBinTotal)

def maskGetBin(mask):
    '''
    This function returns the mask in binary format
    '''
    maskBin = ''
    if mask[0] == '/':
        mask = int(mask[1:])
    else:
        mask = int(mask)
    
    for x in range(32):
        if mask > 0:
            maskBin = maskBin + '1'
        else:
            maskBin = maskBin + '0' 
        mask = mask - int(1)
    return maskBin

def maskGetIpFormat(mask):
    '''
    Returns the mask in binary format
    '''
    return binIpToDecIp(maskGetBin(mask))

def getSubnet(ip,mask):
    '''
    Receives the IP, Mask and returns the subnet
    '''
    subnet = ""
    ip = ipBinFormat(ip)
    mask = maskGetBin(mask)
    count = 0
    for x in range(32):
        subnet = subnet + str((int(ip[count]) and int(mask[count])))
        count = count + 1
    return (binIpToDecIp(subnet))

def getIpAndMask(ipWithMaskSlashNotation):
    '''
    Receives the IP, Mask and returns the subnet
    '''
    ipMask = []
    ipWithMaskSplitted = ipWithMaskSlashNotation.split("/")
    
    ip = str(ipWithMaskSplitted[0])
    mask = "/"+str(ipWithMaskSplitted[1])
    ipMask.append(ip)
    ipMask.append(mask)
    return (ipMask)

def maskIpNet(ip,mask):
    '''
    Receives an IP and Mask and concatenate them
    Outputs
    ip[0] = Ip + Mask eg. "192.168.107.1/24"
    ip[1] = Subnet eg. "192.168.107.0"
    ip[2] = Subnet + mask eg. "192.168.107.0/24"
    ip[3] = Ip eg. "192.168.107.1"
    '''
    
    ipMask = []

    ipMask.append(ip+mask)
    ipMask.append(getSubnet(ip,mask))
    ipMask.append(getSubnet(ip,mask)+mask)
    ipMask.append(ip)

    return (ipMask)
