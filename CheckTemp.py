import os, sys

try:
    import wmi
except Exception as e:
    print(e)
    os.system('pip install wmi')
    sys.exit("Restart the Prototype.")

w = wmi.WMI(namespace= "OpenHardwareMonitor")

def checktemp():
    avg, coren, gpuTemp = 0, 0, 0

    temperature_infos = w.Sensor() 
    for sensor in temperature_infos: 
        if sensor.SensorType==u'Temperature':
            if sensor.Name.startswith("CPU Core"):
                avg += sensor.value
                coren += 1
            if sensor.Name == u"GPU Core":
                gpuTemp = sensor.value
    cpuTemp = avg // coren
    return cpuTemp, gpuTemp


def checkusage():
    cpu = 0
    ram = 0
    gpu = 0
    
    usage_info = w.Sensor()
    for sensor in usage_info:
        if sensor.SensorType == u"Load":
            if sensor.name =="CPU Total":
                cpu = sensor.value
            if sensor.name == u"Memory":
                ram = sensor.value
            if sensor.name == u"GPU Video Engine":
                gpu = sensor.value
    return cpu, ram, gpu

    


if __name__ == "__main__":
    checkusage()