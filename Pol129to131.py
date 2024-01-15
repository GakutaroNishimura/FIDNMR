import numpy as np
import pandas as pd
import ROOT
import sys
argvs = sys.argv

DataPath = "./FIDPeakIntegral155.txt"
DataPath129 = "./FIDPeakIntegral129.txt"

df129 = pd.read_table(DataPath129, names=["Int_129", "Int_129E", "T_129", "T_129E"], sep=" ")

T_AQ = 6*10**(-3) #[s]

T_129 = df129.T_129[0]
T_129E = df129.T_129E[0]
Int_129 = df129.Int_129[0]
Int_129E = df129.Int_129E[0]
P_129 = 1.9 #パーセント.
P_129E = 0.1
gamma_129 = 11.86 #[MHz/T]
NatAbun_129 = 26.401 #パーセント.
I_129 = 0.5

gamma_131 = 3.516 #[MHz/T]
NatAbun_131 = 21.232 #パーセント.
I_131 = 1.5

df = pd.read_table(DataPath, names=["Int_131", "Int_131E", "T_131"], sep=" ")

T2_mean = df.T_131[1:].mean()
T2_std = df.T_131[1:].std()
# print(df.T_131[1:].std())


def CalPol(Int_131):
    return P_129*(Int_131/Int_129)*(NatAbun_129/NatAbun_131)*(gamma_129/gamma_131)*(I_129/I_131)*np.exp(T_AQ/T2_mean - T_AQ/T_129)

def CalPolE(Int_131, Int_131E):
    IntDivE = np.sqrt((Int_131E/Int_129)**2 + (Int_131*Int_129E/Int_129**2)**2) #Error of Int_131/Int_129.
    ExpDiv = np.exp(T_AQ/T2_mean - T_AQ/T_129)
    T2E = np.sqrt((T_AQ*T2_std*ExpDiv/T2_mean**2)**2 + (T_AQ*T_129E*ExpDiv/T_129E**2)**2) #Error of T_AQ correction.
    return np.sqrt((P_129E*ExpDiv*Int_131E/Int_129)**2 + (IntDivE*P_129*ExpDiv)**2 + (T2E*P_129*Int_131E/Int_129)**2)*(NatAbun_129/NatAbun_131)*(gamma_129/gamma_131)*(I_129/I_131)

for i in range(len(df.T_131)):
    Int_131, Int_131E = df.Int_131[i], df.Int_131E[i]
    # print(Int_131, Int_131E)
    P_131 = CalPol(Int_131)
    P_131E = CalPolE(Int_131, Int_131E)

    f=open(argvs[1],"a")
    f.write("%f %f\n" %(P_131, P_131E))
    f.close()