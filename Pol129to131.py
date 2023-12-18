import numpy as np
import pandas as pd
import ROOT
import sys
argvs = sys.argv

DataPath = "./FIDPeakIntegral155.txt"
DataPath129 = "./FIDPeakIntegral129.txt"

df129 = pd.read_table(DataPath129, names=["Int_129", "T_129"], sep=" ")

T_AQ = 6*10**(-3) #[s]

T_129 = df129.T_129[0]
Int_129 = df129.Int_129[0]
P_129 = 1.9 #パーセント.
gamma_129 = 11.86 #[MHz/T]
NatAbun_129 = 26.401 #パーセント.
I_129 = 0.5

gamma_131 = 3.516 #[MHz/T]
NatAbun_131 = 21.232 #パーセント.
I_131 = 1.5

df = pd.read_table(DataPath, names=["Int_131", "T_131"], sep=" ")

T2_mean = df.T_131[1:-1].mean()

def CalPol(Int_131, T2_mean):
    return P_129*(Int_131/Int_129)*(NatAbun_129/NatAbun_131)*(gamma_129/gamma_131)*(I_129/I_131)*np.exp(T_AQ/T2_mean - T_AQ/T_129)

for Int_131 in df.Int_131:
    P_131 = CalPol(Int_131, T2_mean)

    f=open(argvs[1],"a")
    f.write("%f\n" %(P_131))
    f.close()