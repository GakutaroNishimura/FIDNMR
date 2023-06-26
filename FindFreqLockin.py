import Config as conf
import Lockin
import FileInfo
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import ROOT
import time

def FindFreqDeltaLockin(StartF, EndF, Naverage, Time, V_mean):
    FreqList = []
    deltaList = []
    LockinList = []
    LockinValue = 0
    deltaRange = np.linspace(0., 2*math.pi, 50)
    for f0 in range(StartF, EndF, 200):
        for delta in deltaRange:
            for i in range(Naverage):
                LockinValue += V_mean[i]*math.cos(2*math.pi*f0*Time[i]+delta)
                if i == Naverage-1:
                    FreqList.append(f0)
                    deltaList.append(delta)
                    LockinList.append(LockinValue)
                    
    return FreqList, deltaList, LockinList

def FindFreqLockin(StartF, EndF, Naverage, Time, V_mean):
    FreqList = []
    LockinList = []
    LockinValue = 0
    for f0 in range(StartF, EndF, 10):
        for i in range(Naverage):
            LockinValue += V_mean[i]*math.cos(2*math.pi*f0*Time[i]+math.pi)
            #LockinValue += V_mean[i]*math.cos(2*math.pi*f0*Time[i])
            if i == Naverage-1:
                FreqList.append(f0)
                LockinList.append(LockinValue)
                    
    return FreqList, LockinList

StartNo = FileInfo.GetMaxFileNumber() + 1
StopNo  = conf.NumOfDataAcquisition

file_list = os.listdir(conf.DataPath)
data_list = []

for i in range(len(file_list)):
    if ".bin" == os.path.splitext(file_list[i])[1]:
        data_list.append(os.path.join(conf.DataPath, file_list[i]))

for i in range(len(data_list)):
    BinaryFileName = data_list[i]
    V, Time = Lockin.Lockin(BinaryFileName)
    print("read %d th data" %i)
    if i == 0:
        #plt.plot(Time, V, ".")
        #plt.show()
        V_mean = np.array([0.0 for i in range(len(V))])
    V_mean += V

FreqList, deltaList, LockinList = FindFreqDeltaLockin(17000, 21000, 1000, Time, V_mean)

#FreqList, LockinList = FindFreqLockin(17000, 20000, 1000, Time, V_mean)

#"""
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(FreqList, deltaList, LockinList)
plt.show()
#"""

"""
fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(FreqList, LockinList)
plt.show()
"""
