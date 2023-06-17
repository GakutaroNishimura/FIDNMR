import Config as conf
import Lockin
import FileInfo
import matplotlib.pyplot as plt
import numpy as np
import os


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
        plt.plot(Time, V, ".")
        plt.show()
        V_mean = np.array([0.0 for i in range(len(V))])
    V_mean += V
    

V_mean = V_mean/len(data_list)

plt.plot(Time, V_mean)
plt.show()

Ndata, freq_spectrum_mean, frequencies = Lockin.fft(V_mean, Time)

plt.plot(frequencies, np.abs(freq_spectrum_mean), ".")
plt.xlim(15000, 22000)
plt.ylim(0, 5)
plt.grid()
plt.show()
print(len(frequencies))
#plt.savefig(conf.DataPath + "fft.pdf")