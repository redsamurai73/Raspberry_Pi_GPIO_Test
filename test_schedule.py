import RPi.GPIO as GPIO
from datetime import date
from datetime import datetime
from datetime import time
from array import array
from re import findall
from subprocess import check_output
from time import sleep

pin = 15;
tempON = 50;
threshold = 5;

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT,initial = 0);
filetime = open('time');
schedule = filetime.readlines();
n = len(schedule);
print(n);
filetime.close();
Pinstate_time = False;
Pinstate_temp = False;
time_array = [];

class Time:

    def __init__(self, timeON, timeOFF):
        self.timeON = timeON;
        self.timeOFF = timeOFF;

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode()
    temp = float(findall('\d+\.\d+', temp)[0])
    return(temp)

currenttime = (datetime.now());
currenttime = datetime(currenttime.year, currenttime.month, currenttime.day, currenttime.hour, currenttime.minute, currenttime.second);
for i in range(0, n, 2):
    print(i);
    z = '%H:%M\n' if i != n - 2 else '%H:%M';
    settimeON = datetime.strptime(schedule[i], '%H:%M\n');
    settimeON = datetime(currenttime.year, currenttime.month, currenttime.day, settimeON.hour, settimeON.minute);
    print(settimeON);
    settimeOFF = datetime.strptime(schedule[i+1], z);
    settimeOFF = datetime(currenttime.year, currenttime.month, currenttime.day, settimeOFF.hour, settimeOFF.minute);
    print(settimeOFF);
    
    settime = Time(settimeON, settimeOFF);
    time_array.append(settime);

while True:
    currenttime = (datetime.now()); #Time measurement
    temp = get_temp(); #Temperature measurement
    for i in range(len(time_array)):
        if currenttime.hour == time_array[i].timeON.hour and currenttime.minute == time_array[i].timeON.minute and not Pinstate_time:
            print("Pin ON");
            Pinstate_time = True; 
        if currenttime.hour == time_array[i].timeOFF.hour and currenttime.minute == time_array[i].timeOFF.minute and Pinstate_time:
            print("Pin OFF");
            Pinstate_time = False;
        if temp > tempON and not Pinstate_temp or temp < tempON - threshold and Pinstate_temp:
            Pinstate_temp = not Pinstate_temp;
        GPIO.output(pin, Pinstate_temp or Pinstate_time);
    
    print(str(temp) + " " + str(Pinstate_temp));
    sleep(2);