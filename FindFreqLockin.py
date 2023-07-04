import Config as conf
import Lockin
import FileInfo
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import ROOT
import time
import pandas as pd
import sys

argvs = sys.argv  
argc = len(argvs) 


Bin_or_Float = conf.Bin_or_Float
FreqDeltaNaverage = 30000
FinalNaverage = 1000
StartF, EndF, dFreq = 18000, 20000, 1
dDelta = 1000
Nstart, Nend = 0, 150000

def FindFreqDeltaLockin(StartF, EndF, Naverage, Time, V_mean):
    FreqList = []
    deltaList = []
    LockinList = []
    
    deltaRange = np.linspace(0., 2*math.pi, 10)
    #deltaRange = np.linspace(0.9*math.pi, 1.1*math.pi, 50)
    for f0 in range(StartF, EndF, 10):
        for delta in deltaRange:
            LockinValue = 0
            for i in range(Naverage):
                LockinValue += V_mean[i]*math.cos(2*math.pi*f0*Time[i]+delta)
                if i == Naverage-1:
                    FreqList.append(f0)
                    deltaList.append(delta)
                    LockinList.append(LockinValue)
                    
    return FreqList, deltaList, LockinList


def FindFreqLockin(StartF, EndF, dFreq, Naverage, Time, V_mean):
    FreqList = []
    LockinList = []
    for ifreq in range(StartF, EndF, dFreq):
        LockinValue = 0
        LockinValue0 = 0
        LockinValue90 = 0
        for i in range(Naverage):
            t0 = Time[0]
            #LockinValue += V_mean[i]*math.cos(2*math.pi*f0*Time[i]+math.pi)
            #LockinValue += V_mean[i]*math.cos(2*math.pi*f0*Time[i])
            LockinValue0 += V_mean[i]*math.cos(2*math.pi*ifreq*Time[i])
            #LockinValue90 += V_mean[i]*math.cos(2*math.pi*f0*Time[i]+math.pi/2)
        t1 = Time[i]
        #LockinValue = math.sqrt(LockinValue0**2 + LockinValue90**2)
        FreqList.append(ifreq)
        #LockinList.append(LockinValue/(t1-t0))
        LockinList.append(LockinValue0/(t1-t0))

    df = pd.DataFrame({"freq": FreqList, "Lockin": LockinList})
    df_s = df.sort_values(by = "Lockin", ascending=False)
    df_r = df_s.reset_index(drop=True)
    F0 = df_r.freq[0]
                    
    return F0, FreqList, LockinList


def FindDeltaLockin(F0, dDelta, Naverage, Time, V_mean):
    FreqList = []
    DeltaList = []
    LockinList = []
    
    deltaRange = np.linspace(0., 2*math.pi, dDelta)
    for idelta in deltaRange:
        LockinValue = 0
        for i in range(Naverage):
            t0 = Time[0]
            LockinValue += V_mean[i]*math.cos(2*math.pi*F0*Time[i]+idelta)
            #LockinValue += V_mean[i]*math.cos(2*math.pi*f0*Time[i])

        t1 = Time[i]
        DeltaList.append(idelta)
        LockinList.append(LockinValue/(t1-t0))
                    
    df = pd.DataFrame({"Delta": DeltaList, "Lockin": LockinList})
    df_s = df.sort_values(by = "Lockin", ascending=False)
    df_r = df_s.reset_index(drop=True)
    Delta0 = df_r.Delta[0]

    return Delta0, DeltaList, LockinList


def FinalLockin(F0, Delta0, Nstart, Nend, Naverage, Time, V_mean):
    aveTime = []
    LockinList = []
    #start_time = time.time()
    for  j in range(int((Nend-Nstart)/Naverage)):
        LockinValue = 0
        LockinValue0 = 0
        LockinValue90 = 0
        for i in range(j*Naverage, (j+1)*Naverage):
            t0 = Time[j*Naverage]
            t1 = Time[(j+1)*Naverage-1]
            t_ave = (t0+t1)/2
            LockinValue0 += V_mean[i]*math.cos(2*math.pi*F0*Time[i]+Delta0)
            #LockinValue90 += V_mean[i]*math.cos(2*math.pi*f0*Time[i]+Delta+math.pi/2)
        #LockinValue = math.sqrt(LockinValue0**2 + LockinValue90**2)
        aveTime.append(t_ave)
        #LockinList.append(LockinValue/(t1-t0))
        LockinList.append(LockinValue0/(t1-t0))
    #end_time = time.time()
    #execution_time = end_time - start_time
    #print("Execution time normal:", execution_time, "seconds")
    return aveTime, LockinList


def GetDataList(Bin_or_Float):
    if Bin_or_Float == "Float":
        print(conf.DataName)
        df = pd.read_table(conf.DataName, sep=" ", names = ["time", "signal"])
        Time = np.array(df.time, dtype="d")
        V_mean = np.array(df.signal, dtype="d")

    else:
        #StartNo = FileInfo.GetMaxFileNumber() + 1
        #StopNo  = conf.NumOfDataAcquisition
        file_list = os.listdir(conf.DataPath)
        data_list = []
        print(conf.DataPath)

        for i in range(len(file_list)):
            if ".bin" == os.path.splitext(file_list[i])[1]:
                data_list.append(os.path.join(conf.DataPath, file_list[i]))

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

    return Time, V_mean


def main():
    Time, V_mean = GetDataList(Bin_or_Float)

    F0, FreqList, FreqLockinList = FindFreqLockin(StartF, EndF, dFreq, FreqDeltaNaverage, Time, V_mean)
    Delta0, DeltaList, DeltaLockinList = FindDeltaLockin(F0, dDelta, FreqDeltaNaverage, Time, V_mean)
    aveTime, LockinList = FinalLockin(F0, Delta0, Nstart, Nend, FinalNaverage, Time, V_mean)

    c1 = ROOT.TCanvas("c1", "c1", 600, 600)
    #c1.SetLeftMargin(0.15)
    #c1.SetRightMargin(0.05)
    #ROOT.gStyle.SetTitleOffset(2.0, "Y")
    gr = ROOT.TGraph(len(aveTime), np.array(aveTime), np.array(LockinList))
    #gr_fit = ROOT.TF1("f", "[0]*expo(-[1]*x)", aveTime[0], aveTime[10])
    #gr_fit.SetParameters(60000., 25.)
    #gr.Fit(gr_fit, "QR")
    #par = [gr_fit.GetParameter(k) for k in range(gr_fit.GetNpar())]
    gr.Draw("APL")
    gr.SetMarkerStyle(7)
    gr.SetMarkerSize(10)
    #gr.SetTitle("average = %d"%FinalNaverage)
    gr.SetTitle("average = %d"%FreqDeltaNaverage)
    gr.GetXaxis().SetTitle("time [s]")
    gr.GetYaxis().SetTitle("LockinValue [V/s]")
    gr.GetYaxis().SetMaxDigits(4)
    #gr_fit.Draw("same")
    #c1 = ROOT.gROOT.FindObject("c1")
    c1.Draw()
    c1.Update()
    c1.SaveAs(conf.DataPath + "LockinValue.pdf")
    c1.SaveAs(conf.DataPath + "LockinValue.png")

    if argc == 2:
        with open(conf.DataPath + argvs[1], "w") as f:
            f.write("FreqDeltaNaverage = %i\n" %(FreqDeltaNaverage))
            f.write("FinalNaverage = %i\n" %(FinalNaverage))
            f.write("StartF = %i, EndF = %i, dFreq = %i\n" %(StartF, EndF, dFreq))
            f.write("dDelta = %i\n" %(dDelta))
            f.write("Nstart = %i, Nend = %i\n" %(Nstart, Nend))
            f.write("F0 = %f, Delta0 = %f\n" %(F0, Delta0))


if __name__ == "__main__":
    main()

