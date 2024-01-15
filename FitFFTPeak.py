import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ROOT
import sys
import Config as conf
import FitFFTPeakFunc as func
import time

argvs = sys.argv

StartNum = 2
EndNum = StartNum + 7

f=open(argvs[1],"a")
# f.write("%f %f %f %f %f\n" %(voltage, integral, par[0], par[1], par[2]))
f.write("%f %f %f\n" %(0.0, 0.0, 0.0))
f.close()

for i in range(StartNum, EndNum + 1):
    # DirPath = "./Data/2023/0726/test%d/" %i
    # DirPath = "./Data/2023/0727/test0%d/" %i
    # DirPath = "./Data/2023/0727/test%d/" %i
    DirPath = "./Data/2023/0728/test0%d/" %i
    # DirPath = "."
    DataPath = DirPath + "/10/ftdata2.csv" 
    # DataPath = conf.DataPath + "/ftdata2.csv"
    df = pd.read_csv(DataPath, names=["freq", "amplitude"])

    # func.FitFunc(DirPath, df)
    func.FitPeak(DirPath, df)

#time.sleep(1000)