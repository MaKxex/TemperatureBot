import os, sys

try:
    import wmi
except Exception as e:
    print(e)
    os.system('pip install wmi')
    sys.exit("Restart the Prototype.")

def checktemp():
    avg, coren = 0, 0
    w = wmi.WMI(namespace= "OpenHardwareMonitor") 
    temperature_infos = w.Sensor() 
    for sensor in temperature_infos: 
        if sensor.SensorType==u'Temperature':
            if sensor.Name.startswith("CPU Core"):
                avg += sensor.value
                coren += 1
    avg = avg // coren
    return avg