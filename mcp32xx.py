#!/usr/bin/env python3
import spidev, time

#Setup spidev to talk to MCP3204/8
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 15600   #MCP32xx suggests 10Khz minimum
spi.mode = 0b01
spi.bits_per_word = 8

#Function to read data from the MCP3208
#Original function was written by Jeremy Blythe, and can be found at: https://github.com/jerbly/Pi
#I changed the xfer bytes construction to work with the 12bit MCP3204/MCP3208 (MCP32xx).
#Current version only works with single-ended samples; differential is not constructed.

def readMCP(channel):
    #if ((channel > 3) or (channel < 0)):   #MCP3204
    if ((channel > 7) or (channel < 0)):   #MCP3208
        return -1

    #Construct the xfer bytes. MCP32xx pads Byte1 with 5 zeroes before the start bit
    #SNG/DIFF & D2 bits trail the start bit, and D1 & D0 bits are the first two bits of Byte2
    #All bits after D0 are "Don't Care" bits.

    byt1 = 6 if channel < 4 else 7   #Only for MCP3208; MCP3204 lists bit D2 as "Don't Care"
    
    byt2 = {0: '0', 1: '64', 2: '128', 3: '192', 4: '0', 5: '64', 6: '128', 7: '192'} #couldn't figure out
    #how to bit shift for the second byte. using the dict has caused no speed degradation for me.

    #Take 10 samples to get an average, and send the smoothed out. Smoothing is optional.
    #To remove smoothing, simply comment/delete all lines marked with #*

    smooth = []  #*
    for i in range(10):  #*
        r = spi.xfer2([byt1, int(byt2[channel]), 0])
        #The MCP32xx responds with samples starting at the 5th bit in Byte2, so we & and shift
        #accordingly.
        adcout = ((r[1]&5) << 8) + r[2]
        smooth.append(adcout) #*
        time.sleep(0.001) #*

    tadaa = sum(smooth) / len(smooth) #*

    return tadaa  #return adcout
