import glob
import time
import os
from os.path import exists


currentSpeed = 0
manualFanControl = False
logFile = '/tmp/fan-manager.log'
pollInterval = 5                    # in seconds
maunalCutOff = 60                   # Max Temp before manual control is disabled 
daily_list = []                     # length =  86400 / pollinterval
recent_list = []                    # length =  recent_list_time / pollinterval
recent_list_time = 900              # in seconds

## Temp : fanspeed % in hexadecimal 
tempMap = {
    '21': '01',
    '22': '02',
    '23': '03',
    '24': '04',
    '25': '05',
    '26': '06',
    '27': '07',
    '28': '08',
    '29': '09',
    '30': '0a',
    '31': '0b',
    '32': '0c',
    '33': '0d',
    '34': '0e',
    '35': '0f',
    '36': '10',
    '37': '11',
    '38': '12',
    '39': '13',
    '40': '14',
    '41': '15',
    '42': '16',
    '43': '17',
    '44': '18',
    '45': '19',
    '46': '1a',
    '47': '1b',
    '48': '1c',
    '49': '1d',
    '50': '1e',
    '51': '1f',
    '52': '20',
    '53': '21',
    '54': '22',
    '55': '23',
    '56': '24',
    '57': '25',
    '58': '26',
    '59': '27',
    '60': '28',
}

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


def main():
    if (not exists(logFile)):
        fp = open(logFile, 'x')
        fp.close()
    log = open(logFile, 'a')
    log.write("Starting Fan Manager\n")
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
