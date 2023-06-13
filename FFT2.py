import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import time as tm

f_file = 276
l_file = 277
V_pp = 150
y_max = 5
min_freq = 18000
max_freq = 20000

Srow = 10
Sfooter = 20

file_path = [] #データのpathをしまうlist.""で囲まれた文字列のリストになる.
for i in range(f_file, l_file+1):
    path = glob.glob("./data/scope_%d.csv"% i)
    file_path.append(path[0])
    
dir_path = "./peak/%d-%d/"%(f_file, l_file)
#dir_path = "./peak/%d-%d/"%(f_file, l_file)

os.makedirs(dir_path, exist_ok=True)

freq_list = []

# CSVファイルからデータを読み込む
for i in range(int(len(file_path)/2)):
    data1 = pd.read_csv(file_path[2*i], names=["time", "RFsignal", "PickUpsignal", "sync2"], skiprows=Srow, skipfooter=Sfooter, engine="python")
    data2 = pd.read_csv(file_path[2*i+1], names=["time", "RFsignal", "PickUpsignal", "sync2"], skiprows=Srow, skipfooter=Sfooter, engine="python")    
    # 時刻と電圧データの列を取得
    time1 = data1["time"].values
    voltage1 = data1["PickUpsignal"].values

    time2 = data2["time"].values
    voltage2 = data2["PickUpsignal"].values
    
    #time = data["time"].values[400:1200]
    #voltage = data["PickUpsignal"].values[400:1200]
    
    #time = data["time"].values[200:1900]
    #voltage = data["PickUpsignal"].values[200:1900]
    
    #time1 = data1["time"].values[1000:19900]
    #voltage1 = data1["PickUpsignal"].values[1000:19900]

    #time2 = data2["time"].values[1000:19900]
    #voltage2 = data2["PickUpsignal"].values[1000:19900]

    time1 = data1["time"].values[2000:19900]
    voltage1 = data1["PickUpsignal"].values[2000:19900]

    time2 = data2["time"].values[2000:19900]
    voltage2 = data2["PickUpsignal"].values[2000:19900]
    
    Npoints = len(time1)
    frequency_spectrum1_mean = np.array([0.0 for i in range(Npoints)])
    frequency_spectrum2_mean = np.array([0.0 for i in range(Npoints)])

    # サンプリング周波数の計算
    sampling_rate = 1 / (time1[1] - time1[0])  # 時刻の間隔からサンプリング周波数を求める

    # 電圧データの平均値を除去
    voltage1 -= np.mean(voltage1)
    voltage2 -= np.mean(voltage2)

    # フーリエ変換を実行
    frequency_spectrum1 = np.fft.fft(voltage1)
    frequencies1 = np.fft.fftfreq(len(voltage1), d=1/sampling_rate)
    frequency_spectrum1_mean += np.abs(frequency_spectrum1)
        
    frequency_spectrum2 = np.fft.fft(voltage2)
    frequencies2 = np.fft.fftfreq(len(voltage2), d=1/sampling_rate)
    frequency_spectrum2_mean += np.abs(frequency_spectrum2)
    #matrix = np.ndarray(frequencies, frequency_spectrum)
    #print(matrix[:10])
    
frequency_spectrum1_mean = frequency_spectrum1_mean/int(len(file_path)/2)
frequency_spectrum2_mean = frequency_spectrum2_mean/int(len(file_path)/2)   


#"""
    # フーリエ変換結果のプロット
fig, ax = plt.subplots(nrows=2)
#ax[0].plot(frequencies, np.abs(frequency_spectrum), ".")
ax[0].plot(frequencies1, np.abs(frequency_spectrum1), ".", label="RF Vpp = " + str(150) + "[V]")
#ax[0].set_xlim(17000, 19000)
ax[0].set_xlim(0, 19000)
#ax[0].set_ylim(0, 20)
ax[0].grid()
ax[0].legend()
ax[1].plot(time1, voltage1, ".")

#plt.savefig(dir_path + str(i) + ".png")
plt.show()
tm.sleep(1000)
plt.close()

freq_list.append(np.max(np.abs(frequency_spectrum1)))
   
plt.plot(np.linspace(1, len(file_path), len(file_path)), freq_list, ".")
plt.grid()
plt.xlabel("nubmer of measurement")
plt.ylabel("amplitude")
plt.savefig(dir_path + "amplitude.png")

#"""

"""

plt.plot(frequencies, np.abs(frequency_spectrum))
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude')
plt.title('Fourier Transformation')
plt.grid(True)
plt.show()

plt.plot(time, voltage)
plt.xlabel('time [s]')
plt.ylabel('voltage')
plt.grid(True)
plt.show()
"""


indices = np.where((frequencies1 >= min_freq) & (frequencies1 <= max_freq))
amplitude = frequency_spectrum1_mean[indices]
max_amp = np.max(amplitude)


fig, ax = plt.subplots(nrows=2)
ax[0].plot(frequencies1, frequency_spectrum1_mean, ".", label="max amplitude = {:.1f}".format(max_amp) + "\n RF $V_{\mathrm{p-p}}$ = %d" %V_pp)
ax[0].set_xlim(min_freq, max_freq)
ax[0].set_ylim(0.0, y_max)
ax[0].grid()
ax[0].legend()
ax[1].plot(frequencies2, frequency_spectrum2_mean, ".")
ax[1].set_xlim(min_freq, max_freq)
ax[1].set_ylim(0.0, y_max)
ax[1].grid()
plt.show()
#plt.savefig(dir_path + "amp_compare.pdf")

