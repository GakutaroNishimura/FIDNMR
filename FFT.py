import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

f_file = 223
l_file = 243
file_path = [] #データのpathをしまうlist.""で囲まれた文字列のリストになる.
for i in range(f_file, l_file+1):
    path = glob.glob("./WaveData/scope_%d.csv"% i)
    file_path.append(path[0])
    
dir_path = "./peak/%d-%d/"%(f_file, l_file)
#dir_path = "./peak/%d-%d/"%(f_file, l_file)

os.makedirs(dir_path, exist_ok=True)



# Load the CSV data into a pandas DataFrame
data = pd.read_csv('./data/scope_10.csv', names=["time", "RFsignal", "PickUpsignal", "sync2"], skiprows=2, skipfooter=1, engine="python")

# Extract the column of data for the Fourier transformation
time_series = data.PickUpsignal

# Calculate the Fourier transformation
fourier_transform = np.fft.fft(time_series)

# Calculate the frequencies corresponding to the Fourier coefficients
n = len(time_series)
timestep = 1  # Assumes uniform timestep, change if necessary
frequencies = np.fft.fftfreq(n, d=timestep)

# Plot the Fourier transformation results
plt.plot(frequencies, np.abs(fourier_transform))
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.title('Fourier Transformation')
plt.grid(True)
plt.show()
