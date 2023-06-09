import Config as conf
import Lockin
import FileInfo
import matplotlib.pyplot as plt
import numpy as np
import os


StartNo = FileInfo.GetMaxFileNumber() + 1
StopNo  = 30

file_list = os.listdir(conf.DataPath)
data_list = []

for i in range(len(file_list)):
    if ".bin" == os.path.splitext(file_list[i])[1]:
        data_list.append(os.path.join(conf.DataPath, file_list[i]))


for i in range(len(data_list)):
    BinaryFileName = data_list[i]
    V, Time = Lockin.Lockin(BinaryFileName)
    Ndata, frequency_spectrum, frequencies = Lockin.fft(BinaryFileName, V, Time)
    print("%d th data analyzed" %i)
    if i == 0:
        freq_spectrum_mean = np.array([0.0 for i in range(Ndata)])
    freq_spectrum_mean += np.abs(frequency_spectrum)

freq_spectrum_mean = freq_spectrum_mean/(StopNo-1)
#print("data analyzed")
plt.plot(frequencies, freq_spectrum_mean, ".")
plt.xlim(10000, 30000)
#plt.xlim(25000, 30000)
plt.ylim(0, 20)
plt.grid()
plt.show()
#plt.savefig(conf.DataPath + "fft.pdf")