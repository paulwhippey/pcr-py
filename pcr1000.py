# 
# Quick and dirty Python script to control an Icom PCR-1000 receiver
#
#Based on the work that GM4JJJ published here: http://www.gm4jjj.co.uk/PCR1000.html
# Many, many thanks for publishing this info.
# This would be impossible without it!
#

import serial
import sys
import time

# Variables
sleepTime = 0.1

# Set to your USB serial port. Do a ls -l /dev/tty.usb* to find your port first
serialPort = "/dev/tty.usbserial-2110"

# Setup serial connection to radio. Initial boot up at 9600 Baud.
ser = serial.Serial(serialPort,9600)
ser.flushInput()

# Queries
isAlive = "H1?"
firmwareVersion = "G4?"
region = "GE?"
hasDsp = "GD?"

# Setup frequency input variables
ghz = sys.argv[1]
mhz = sys.argv[2]
khz = sys.argv[3]
hz = sys.argv[4]
mode = sys.argv[5]
fil = sys.argv[6]

# Print desired frequency etc
print ("Tuning to: " + ghz + "," + mhz + "," + khz + "." + hz + " GHz. Mode: " + mode + " Filter: " + fil)

# Construct desired frequency, mode, filter settings
# Frequency, mode and filter syntax: K0 G MMM KKK HHH mm ff 00
# K0 padding, G = GHz, MMM = MHz, KKK = kHz, HHH = Hz, mm = mode, ff = filter, 00 = padding
# Frequency is in GHz
# ----------------  GMMMKKKHHH
desiredFrequency = ghz + mhz + khz + hz # 0 GHz 088 MHz 900 kHz 000 Hz
# 0 088 900 000 06 04

# Mode is one of:
# 00 = LSB
# 01 = USB
# 02 = AM
# 03 = CW
# 04 = Not used or Unknown
# 05 = NFM
# 06 = WFM
desiredMode = mode

# Filter is one of:
# 00 = 3 Khz (actually 2.8 Khz) (CW USB LSB AM)
# 01 = 6 Khz (CW USB LSB AM NFM)
# 02 = 15 Khz (AM NFM)
# 03 = 50 Khz (AM NFM WFM)
# 04 = 230 Khz (WFM)
desiredFilter = fil

# Commands

# Setup frequency, mode and filter command
setFrequency = "K0" + desiredFrequency + desiredMode + desiredFilter + "00\r\n"

# Other commands
powerOn = "H101\r\n"
powerOff = "H100\r\n"
baud38400 = "G105\r\n"
updateOff = "G300\r\n"
updateOn = "G301\r\n"
setVolume = "J4077\r\n"

# Initial settings
initFrequency = "K00857937500050200\r\n"
initSquelch = "J4100\r\n"
initToneSquelch = "J5100\r\n"
initVsc = "J5000\r\n"
initIfShift = "J4380\r\n"
initAGC = "J4500\r\n"
initNB = "J4600\r\n"
initAtt = "J4700\r\n"
initMisc = "J4A80\r\n"
initTrackFilter = "LD82000\r\n"
initDSP = "J8001J8101J8200J8301\r\n"
initVolume = "J4000\r\n"
initBandScope = "ME0000120050100012500\r\n"
initSigUpdate = "G301\r\n"

#### Initialise radio ####
print("Initialising radio...")

# H101 Turn Radio ON
ser.write(str.encode(powerOn))
time.sleep(0.1)

# J4100 Set Squelch
ser.write(str.encode(initSquelch))
time.sleep(sleepTime)

# J5100 See Tone Squelch
ser.write(str.encode(initToneSquelch))
time.sleep(sleepTime)

# J5000 Set VSC off
ser.write(str.encode(initVsc))
time.sleep(sleepTime)

# J4380 Set IF Shift to mid range
ser.write(str.encode(initIfShift))
time.sleep(sleepTime)

# J4500 Set AGC OFF
ser.write(str.encode(initAGC))
time.sleep(sleepTime)

# J4600 Set Noise Blanker OFF
ser.write(str.encode(initNB))
time.sleep(sleepTime)

# J4700 Set Attenuator OFF
ser.write(str.encode(initAtt))
time.sleep(sleepTime)

# J4000 Set Volume
ser.write(str.encode(initVolume))
time.sleep(sleepTime)

#### Initialise radio ends ####
print("Radio initialised.")

# Set frequency, mode and filter
print("Setting desired frequency: " + desiredFrequency + " mode: " + desiredMode + " and filter: " + desiredFilter + " ...")
ser.write(str.encode(setFrequency))
time.sleep(sleepTime)
print("Desired frequency, mode and filter is set.")

# Set volume level
print("Setting desired volume...")
ser.write(str.encode(setVolume))
print("Desired volume is set.")

# Keep sending radio on command or radio will turn off!
print("Running radio keep alive loop. Press CTRL-C to exit...")

try:
    while True:
        ser.write(str.encode(powerOn))
        time.sleep(10)
except KeyboardInterrupt:
    pass

# Turn off radio
print("Turning off radio...")
ser.write(str.encode(powerOff))
time.sleep(0.1)
print("Radio turned off.")

# Close serial port
print ("Closing port...")
ser.close()
print ("Port closed.")
