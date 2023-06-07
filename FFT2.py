import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import time as tm

#f_file = 223
#l_file = 243
#f_file = 244
#l_file = 245
f_file = 246
l_file = 247
f_file = 248
l_file = 249
f_file = 250
l_file = 251
f_file = 252
l_file = 253
f_file = 254
l_file = 255
f_file = 256
l_file = 257
f_file = 258
l_file = 259
f_file = 260
l_file = 261
f_file = 262
l_file = 263
#f_file = 264
#l_file = 265
#f_file = 266
#l_file = 267
#f_file = 268
#l_file = 269
f_file = 270
l_file = 271
f_file = 272
l_file = 273
#f_file = 274
#l_file = 275
#f_file = 276
#l_file = 277
f_file = 278
l_file = 297
file_path = [] #データのpathをしまうlist.""で囲まれた文字列のリストになる.
for i in range(f_file, l_file+1):
    path = glob.glob("./data/scope_%d.csv"% i)
    file_path.append(path[0])
    
dir_path = "./peak/%d-%d/"%(f_file, l_file)
#dir_path = "./peak/%d-%d/"%(f_file, l_file)

os.makedirs(dir_path, exist_ok=True)

freq_list = []

frequency_spectrum1_mean = np.array([0.0 for i in range(982)])
frequency_spectrum2_mean = np.array([0.0 for i in range(982)])

# CSVファイルからデータを読み込む
for i in range(int(len(file_path)/2)):
    data1 = pd.read_csv(file_path[2*i], names=["time", "RFsignal", "PickUpsignal", "sync2"], skiprows=10, skipfooter=10, engine="python")
    data2 = pd.read_csv(file_path[2*i+1], names=["time", "RFsignal", "PickUpsignal", "sync2"], skiprows=10, skipfooter=10, engine="python")    
    # 時刻と電圧データの列を取得
    time1 = data1["time"].values
    voltage1 = data1["PickUpsignal"].values

    time2 = data2["time"].values
    voltage2 = data2["PickUpsignal"].values
    
    #time = data["time"].values[400:1200]
    #voltage = data["PickUpsignal"].values[400:1200]
    
    #time = data["time"].values[200:1900]
    #voltage = data["PickUpsignal"].values[200:1900]
    
    #time = data["time"].values[1000:19900]
    #voltage = data["PickUpsignal"].values[1000:19900]

    #time = data["time"].values[2000:19900]
    #voltage = data["PickUpsignal"].values[2000:19900]
    
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

"""
    # フーリエ変換結果のプロット
    fig, ax = plt.subplots(nrows=2)
    #ax[0].plot(frequencies, np.abs(frequency_spectrum), ".")
    ax[0].plot(frequencies, np.abs(frequency_spectrum), ".", label="RF Vpp = " + str(150) + "[V]")
    ax[0].set_xlim(15000, 25000)
    ax[0].set_ylim(0, 5)
    ax[0].grid()
    ax[0].legend()
    ax[1].plot(time, voltage, ".")
    
    plt.savefig(dir_path + str(i) + ".png")
    #plt.show()
    #tm.sleep(1000)
    plt.close()

    freq_list.append(np.max(np.abs(frequency_spectrum)))
    
plt.plot(np.linspace(1, len(file_path), len(file_path)), freq_list, ".")
plt.grid()
plt.xlabel("nubmer of measurement")
plt.ylabel("amplitude")
plt.savefig(dir_path + "amplitude.png")

"""

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

fig, ax = plt.subplots(nrows=2)
ax[0].plot(frequencies1, frequency_spectrum1_mean, ".")
ax[0].set_xlim(13000, 25000)
ax[0].set_ylim(0.0, 0.3)
ax[0].grid()
ax[1].plot(frequencies2, frequency_spectrum2_mean, ".")
ax[1].set_xlim(13000, 25000)
ax[1].set_ylim(0.0, 0.3)
ax[1].grid()
plt.show()