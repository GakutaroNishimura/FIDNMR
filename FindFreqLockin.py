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

#AnalyzeDir = conf.DataPath + "/LockinValue_cos_sin/"
#AnalyzeDir = conf.DataPath + "/LockinValue_cos/"
AnalyzeDir = conf.DataPath + "/LockinValue_cos_fitF0/"

os.makedirs(AnalyzeDir, exist_ok=True)

Bin_or_Float = conf.Bin_or_Float
FreqDeltaNaverage = 1000
FinalNaverage = 1000
StartF, EndF, dFreq = 18500, 19500, 0.01
dDelta = 1000
Nstart, Nend = 0, 150000
x_min = 0
x_max = 150000

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
    #for ifreq in range(StartF, EndF, dFreq):
    for ifreq in np.arange(StartF, EndF, dFreq):
        LockinValue = 0
        LockinValue0 = 0
        LockinValue90 = 0
        for i in range(Naverage):
            t0 = Time[0]
            #LockinValue += V_mean[i]*math.cos(2*math.pi*f0*Time[i]+math.pi)
            #LockinValue += V_mean[i]*math.cos(2*math.pi*f0*Time[i])
            LockinValue0 += V_mean[i]*math.cos(2*math.pi*ifreq*Time[i])
            #LockinValue90 += V_mean[i]*math.cos(2*math.pi*ifreq*Time[i]+math.pi/2)
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
        LockinValue0 = 0
        LockinValue90 = 0
        for i in range(Naverage):
            t0 = Time[0]
            LockinValue0 += V_mean[i]*math.cos(2*math.pi*F0*Time[i]+idelta)
            #LockinValue90 += V_mean[i]*math.cos(2*math.pi*F0*Time[i]+idelta+math.pi/2)

        #LockinValue = math.sqrt(LockinValue0**2 + LockinValue90**2)
        t1 = Time[i]
        DeltaList.append(idelta)
        #LockinList.append(LockinValue/(t1-t0))
        LockinList.append(LockinValue0/(t1-t0))
                    
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
            #LockinValue90 += V_mean[i]*math.cos(2*math.pi*F0*Time[i]+Delta0+math.pi/2)
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

"""
def FitSignal(x_min, x_max, Time, V_mean):
    #c1 = ROOT.TCanvas("c1", "c1", 600, 600)
    #c1.Divide(1, 2)
    #c1.cd(1)
    #gr = ROOT.TGraph(len(df.time[x_min:x_max]), np.array(df.time[x_min:x_max]), np.array(df.PickUpsignal[x_min:x_max]))
    gr = ROOT.TGraph(len(Time[x_min:x_max]), Time[x_min:x_max], V_mean[x_min:x_max])
    gr_fit = ROOT.TF1("f", "[0]*expo(-[1]*x)*sin(2*pi*[2]*x+[3]) + [4]", Time[x_min], Time[x_max])
    #gr_fit.SetParameters(-6.61436292e-03,  6.50124722e+01,  1.81216540e+04,  1.41380037e+00)
    #gr_fit.SetParameters(0.01415861885725226, 13.324007257585418, 18117.27312027492, 0.) # "./data/scope_260.csv"
    gr_fit.SetParameters(0.04341888572810267, 5.383077353509305, 18900.682613541823, -35.1607898488646, 0.0020867903362365692) # 129Xe_069A_19kHz/run6
    gr_fit.SetNpx(10000)
    gr.Fit(gr_fit, "QR")
    par = [gr_fit.GetParameter(k) for k in range(gr_fit.GetNpar())]
    print(par)
    #gr.Draw("APL")
    #gr.SetMarkerStyle(7)
    #gr.SetMarkerSize(10)
    #ROOT.gStyle.SetOptFit(1)
    #c1 = ROOT.gROOT.FindObject("c1")
    #c1.Draw("same")
    #c1.Update()

    return par[2]
"""
    

def main():
    Time, V_mean = GetDataList(Bin_or_Float)
    c1 = ROOT.TCanvas("c1", "c1", 600, 600)
    #c1.Divide(1, 2)
    #c1.cd(1)
    #c1.cd(1)
    grSignal = ROOT.TGraph(len(Time[x_min:x_max]), Time[x_min:x_max], V_mean[x_min:x_max])
    gr_fit = ROOT.TF1("f", "[0]*expo(-[1]*x)*sin(2*pi*[2]*x+[3]) + [4]", Time[x_min], Time[x_max])
    gr_fit.SetParameters(0.04341888572810267, 5.383077353509305, 18900.682613541823, -35.1607898488646, 0.0020867903362365692) # 129Xe_069A_19kHz/run6
    gr_fit.SetNpx(10000)
    grSignal.Fit(gr_fit, "QR")
    par = [gr_fit.GetParameter(k) for k in range(gr_fit.GetNpar())]
    grSignal.Draw("APL")
    grSignal.SetMarkerStyle(7)
    grSignal.SetMarkerSize(10)
    ROOT.gStyle.SetOptFit(1)
    c1.Draw()
    #c1.Update()

    F0 = par[2]
    #F0 = FitSignal(x_min, x_max, Time, V_mean)
    #F0, FreqList, FreqLockinList = FindFreqLockin(StartF, EndF, dFreq, FreqDeltaNaverage, Time, V_mean)
    Delta0, DeltaList, DeltaLockinList = FindDeltaLockin(F0, dDelta, FreqDeltaNaverage, Time, V_mean)
    aveTime, LockinList = FinalLockin(F0, Delta0, Nstart, Nend, FinalNaverage, Time, V_mean)

    c2 = ROOT.TCanvas("c2", "c2", 600, 600)
    #c1.cd(2)
    #c2.cd()
    #c1.SetLeftMargin(0.15)
    #c1.SetRightMargin(0.05)
    #ROOT.gStyle.SetTitleOffset(2.0, "Y")
    grLockin = ROOT.TGraph(len(aveTime), np.array(aveTime), np.array(LockinList))
    #gr_fit = ROOT.TF1("f", "[0]*expo(-[1]*x)", aveTime[0], aveTime[10])
    #gr_fit.SetParameters(60000., 25.)
    #gr.Fit(gr_fit, "QR")
    #par = [gr_fit.GetParameter(k) for k in range(gr_fit.GetNpar())]
    grLockin.Draw("APL")
    grLockin.SetMarkerStyle(7)
    grLockin.SetMarkerSize(10)
    #gr.SetTitle("average = %d"%FinalNaverage)
    grLockin.SetTitle("average = %d"%FreqDeltaNaverage)
    grLockin.GetXaxis().SetTitle("time [s]")
    grLockin.GetYaxis().SetTitle("LockinValue [V/s]")
    grLockin.GetYaxis().SetMaxDigits(4)
    #gr_fit.Draw("same")
    #c1 = ROOT.gROOT.FindObject("c1")
    #c1.Draw("same")
    #c1.Update()
    c2.Draw()
    #c2.Update()
    #time.sleep(1000)
    c2.SaveAs(AnalyzeDir + "LockinValue_%i.pdf" %FreqDeltaNaverage)
    c2.SaveAs(AnalyzeDir + "LockinValue_%i.png" %FreqDeltaNaverage)

    if argc == 2:
        with open(AnalyzeDir + argvs[1], "a") as f:
            f.write("FreqDeltaNaverage = %i\n" %(FreqDeltaNaverage))
            f.write("FinalNaverage = %i\n" %(FinalNaverage))
            f.write("StartF = %i, EndF = %i, dFreq = %i\n" %(StartF, EndF, dFreq))
            f.write("dDelta = %i\n" %(dDelta))
            f.write("Nstart = %i, Nend = %i\n" %(Nstart, Nend))
            f.write("F0 = %f, Delta0 = %f\n" %(F0, Delta0))
            f.write("----------------------------------------------------\n")


if __name__ == "__main__":
    main()

