import glob
import time
import os
from os.path import exists

currentLogFile = ""
currentSpeed = 0
manualFanControl = False
logFile = '/tmp/fan-manager.log'
pollInterval = 5                    # in seconds
maunalCutOff = 60                   # Max Temp before manual control is disabled 
daily_list = []                     # length =  86400 / pollinterval
recent_list = []                    # length =  recent_list_time / pollinterval
recent_list_time = 900              # in seconds

## Temp : fanspeed % in hexadecimal 
tempMap = {}

def FanControlSwitch(enable):
    global manualFanControl
    if(enable):
        if(manualFanControl == False):
            cmd = "ipmitool raw 0x30 0x30 0x01 0x00"
            manualFanControl = True
            os.system(cmd)
    else:
        cmd = "ipmitool raw 0x30 0x30 0x01 0x01"
        os.system(cmd)
        manualFanControl = False

def get_cpu_temp():
    cpu_temps = []
    for x in glob.glob("/sys/class/thermal/thermal_zone[0-9]/temp"): 
        tempFile = open(x)
        cpu_temps.append(int(tempFile.read().strip('\n')))
        tempFile.close()

    averageTemp = 0
    for i in cpu_temps:
        averageTemp += i

    temp = int((int(averageTemp)/1000)/len(cpu_temps))

    if (len(daily_list) >= (86400/pollInterval)):
        daily_list.pop()
    daily_list.insert(0, temp)

    if (len(recent_list) >= (recent_list_time/pollInterval)):
        recent_list.pop()
    recent_list.insert(0, temp)


    return temp

def setFanSpeed(temp, speed):
    global currentSpeed
    currentSpeed = speed
    FanControlSwitch(True)
    cmd = f"ipmitool raw 0x30 0x30 0x02 0xff 0x{speed}"
    os.system(cmd)

def loadTempMap(filePath = './default.tm'):
    global tempMap
    if exists(filePath):
        with open(filePath, 'r') as f:
            line = f.readline()
            while line:
                tempMap.update({line.split(',')[0]: line.split(',')[1].strip('\n')})
                line = f.readline()

def main():
    ## Setup Logging
    if (not exists(logFile)):
        fp = open(logFile, 'x')
        fp.close()
    log = open(logFile, 'a')
    log.write("Starting Fan Manager\n")

    loadTempMap()

    ## Set Fan control to manual
    FanControlSwitch(True)
    exit = False
    while (not exit):
        time.sleep(pollInterval)
        t = get_cpu_temp()
        if(t > 60):
            log.write("Temp too high! Disabling Manual Fan Control\n")
            FanControlSwitch(False)
        else:
            FanControlSwitch(True)
            if ( tempMap[str(t)] != currentSpeed ):
                log.write(f"Temp :{t} - Setting Fan Speed {int(tempMap[str(t)],16)}%")
                setFanSpeed(t, tempMap[str(t)])
            else:
                log.write(f"Temp :{t} - Fan Speed {int(tempMap[str(t)],16)}% not changed")
        average_24 = round(sum(daily_list) / len(daily_list),2)
        average_recent = round(sum(recent_list) / len(recent_list),2)
        log.write(f" - 24 hr Average: {average_24} - Recent Average: {average_recent}\n")
                

        log.flush()  


if __name__ == "__main__":
    main()
