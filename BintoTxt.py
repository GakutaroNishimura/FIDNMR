import Config as conf
import Lockin
import numpy as np
import os
import sys

argvs = sys.argv  
argc = len(argvs) 

for j in range(1, 12):

    file_list = os.listdir(conf.DataPath + "%i/" %j)
    data_list = []
    print(conf.DataPath)

    for i in range(len(file_list)):
        #if ".bin" == os.path.splitext(file_list[i])[1]:
        if ".1d" == os.path.splitext(file_list[i])[1]:
            data_list.append(os.path.join(conf.DataPath + "%i/" %j, file_list[i]))

    print(len(data_list))

    for i in range(len(data_list)):
        BinaryFileName = data_list[i]
        V, Time = Lockin.Lockin(BinaryFileName)
        #V = np.array([V[i] + 0.05*np.exp(-100*Time[i]) for i in range(len(V))])
        #print("read %d th data" %i)
        if i == 0:
            #plt.plot(Time, V, ".")
            #plt.show()
            V_mean = np.array([0.0 for i in range(len(V))])
        V_mean += V

    V_mean = V_mean/len(data_list)

    with open(conf.DataPath  + "%i/" %j + argvs[1], "w") as f:
        for i in range(len(Time)):
            f.write("%f %f\n" %(Time[i], V_mean[i]))