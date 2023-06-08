#======================================================================
#  Calculation of neutron spin rotation
#  ver.1.0:     2019            T.Okudaira  (AFPNMR_FS/Lockin.py)
#  ver.2.0:     2022            S.Takahashi (AFPNMRGUI/Lockin_forGUI.py)
#  ver.3.0:     2022            S.Takahashi (AFPNMRGUI_ver3/Lockin_forGUI.py)
#  ver.4.0:     2023/03/28      S.Takada    (AFPNMR/Lockin.py)
#======================================================================

import struct
import ROOT
from array import array
import math
import numpy as np
import pandas as pd
import datetime
import os
import DrawGraph
import Config as conf
import FileInfo

def Lockin(path_w):
    V, VSubx, VSuby, VSub, VSubsq, VRef = [], [], [], [], [], []
    VLockinx, VLockiny, VLockin, TimeLockin = [], [], [], []
    XYScale = []  # [TOrigin, TReference, TIncrement, VOrigin, VReference, VIncrement]
    Time = []
    #dfreq = (conf.FreqRange[1]-conf.FreqRange[0]) / conf.ModulationTime      #    ModulationFreq -> 1/conf.ModulationTime
    NPoint = 0
    NPointLockin = 0
    VLockintemp = 0
    VLockintempx = 0
    VLockintempy = 0
    i = 0
    with open(path_w, mode='rb') as f:
        while True:
            if (i < 6):
                Nbyte = 4
            else:
                Nbyte = 1
            d = f.read(Nbyte)
            if len(d) == 0:
                break
            if (Nbyte == 4):
                d8 = struct.unpack('f', d)
                XYScale.append(d8[0])
            if (Nbyte == 1):
                d8 = struct.unpack('B', d)
                if (1):
                    VSigtmp = (d8[0]-XYScale[4])*XYScale[5]+XYScale[3]
                    V.append(VSigtmp)
                    Time.append((NPoint-XYScale[1])*XYScale[2]+XYScale[0])
                    # VRef.append(math.sin(2*math.pi*(dfreq*Time[NPoint]*0.5+ifreq)*Time[NPoint]-1/2*math.pi))
                    # VLockintempx=VLockintempx+V[NPoint]*math.sin(2*math.pi*(dfreq*Time[NPoint]*0.5+ifreq)*Time[NPoint]+Phase)

                    """
                    VLockintempx = VLockintempx + \
                        V[NPoint]*math.sin(2*math.pi*(dfreq*Time[NPoint]
                                                      * 0.5+conf.FreqRange[0])*Time[NPoint]+conf.Phase)

                    
                    VLockintempx = VLockintempx + \
                        V[NPoint]*math.cos(2*math.pi*
                                           (dfreq*Time[NPoint]*0.5 + conf.FreqRange[0])*Time[NPoint]
                                           + conf.Phase)
                    
                    
                    # VLockintempy=VLockintempy+V[NPoint]*math.cos(2*math.pi*(dfreq*Time[NPoint]*0.5+ifreq)*Time[NPoint]+Phase)

                    VLockintempy = VLockintempy + \
                        V[NPoint]*math.cos(2*math.pi*(dfreq*Time[NPoint]
                                                      * 0.5+conf.FreqRange[0])*Time[NPoint]+conf.Phase)                    
                    
                    VLockintempy = VLockintempy + \
                        V[NPoint]*math.sin(2*math.pi*
                                           (dfreq*Time[NPoint]*0.5 + conf.FreqRange[0])*Time[NPoint]
                                           + conf.Phase)
                    
                    
                    #                    VLockintemp = VLockintemp + \
                        #                        (VLockintempx**2+VLockintempy**2)**0.5
                    VLockintemp = VLockintemp + math.sqrt(pow(VLockintempx,2) + pow(VLockintempy,2))
                    # VLockintempsq=VLockintemp+V[NPoint]**2

                    #                    print(i, VLockintempx, VLockintempy)
                    
                    if (NPoint % conf.NMean == 0 and NPoint != 0):
                        VLockinx.append(VLockintempx / conf.NMean)
                        VLockiny.append(VLockintempy / conf.NMean)
                        VLockin.append(math.sqrt(pow(VLockintempx/conf.NMean, 2) + pow(VLockintempy/conf.NMean, 2)))
                        # VLockinsq.append(((VLockintempsq/NMean)**2)**0.5)
                        # TimeLockin.append(Time[NPoint])
                        TimeLockin.append(Time[NPoint]*dfreq + conf.FreqRange[0])
                        NPointLockin = NPointLockin+1
                        VLockintempx = 0
                        VLockintempy = 0
                        VLockintemp  = 0
                    """
                    NPoint = NPoint+1
            i = i+1
    """   
    print("NPoint of Graph %f, time resolution %f, N wave for average %f" %
          (len(lockin1[0]["VLockinx"]), lockin1[2][2], lockin1[2][2]*lockin1[3]/50e3))
    
    df = pd.DataFrame(dict(VLockinx=VLockinx, VLockiny=VLockiny,
                           VLockin=VLockin, TimeLockin=TimeLockin))
    """
    return V, Time

def MakeLockinGraphs(LockinDataFrame1, LockinDataFrame2):
    # Axis names
    AxisTitle = [";Freqensy [Hz]", ";Voltage [V]"]

    # Graph names
    Title=["x"           + AxisTitle[0] + AxisTitle[1],
           "y"           + AxisTitle[0] + AxisTitle[1],
           "x^2+y^2"     + AxisTitle[0] + AxisTitle[1],
           "substruct x" + AxisTitle[0] + AxisTitle[1],
           "substruct y" + AxisTitle[0] + AxisTitle[1],
           "((substruct x)^2+(substruct y)^2)^0.5" + AxisTitle[0] + AxisTitle[1]]
    #           "substruct (x^2+y^2)^0.5" + AxisTitle[0] + AxisTitle[1]]
    
    # Subtruction
    SubtractionDataFrame           = LockinDataFrame1.copy()
    SubtractionDataFrame["VSubtx"] = LockinDataFrame1["VLockinx"] - LockinDataFrame2["VLockinx"]
    SubtractionDataFrame["VSubty"] = LockinDataFrame1["VLockiny"] - LockinDataFrame2["VLockiny"]
    SubtractionDataFrame["VSubt"]  = pow(pow(SubtractionDataFrame["VSubtx"], 2) + pow(SubtractionDataFrame["VSubty"], 2), 0.5)
    
    # Make Graphs
    Graph1X = DrawGraph.MakeGraph(LockinDataFrame1, "TimeLockin", "VLockinx", "XError", "YError")
    Graph2X = DrawGraph.MakeGraph(LockinDataFrame2, "TimeLockin", "VLockinx", "XError", "YError")
    Graph1Y = DrawGraph.MakeGraph(LockinDataFrame1, "TimeLockin", "VLockiny", "XError", "YError")
    Graph2Y = DrawGraph.MakeGraph(LockinDataFrame2, "TimeLockin", "VLockiny", "XError", "YError")
    Graph1  = DrawGraph.MakeGraph(LockinDataFrame1, "TimeLockin", "VLockin", "XError", "YError")
    Graph2  = DrawGraph.MakeGraph(LockinDataFrame2, "TimeLockin", "VLockin", "XError", "YError")
    
    GraphSubtX = DrawGraph.MakeGraph(SubtractionDataFrame, "TimeLockin", "VSubtx", "XError", "YError")
    GraphSubtY = DrawGraph.MakeGraph(SubtractionDataFrame, "TimeLockin", "VSubty", "XError", "YError")
    GraphSubt  = DrawGraph.MakeGraph(SubtractionDataFrame, "TimeLockin", "VSubt", "XError", "YError")
    
    # Set Graph Styles
    # line color
    Graph1X.SetLineColor(1)
    Graph2X.SetLineColor(2)
    Graph1Y.SetLineColor(1)
    Graph2Y.SetLineColor(2)
    Graph1.SetLineColor(1)
    Graph2.SetLineColor(2)
    GraphSubtX.SetLineColor(1)
    GraphSubtY.SetLineColor(1)
    GraphSubt.SetLineColor(1)
    # marker color
    Graph1X.SetMarkerColor(1)
    Graph2X.SetMarkerColor(2)
    Graph1Y.SetMarkerColor(1)
    Graph2Y.SetMarkerColor(2)
    Graph1.SetMarkerColor(1)
    Graph2.SetMarkerColor(2)
    GraphSubtX.SetMarkerColor(1)
    GraphSubtY.SetMarkerColor(1)
    GraphSubt.SetMarkerColor(1)
    # graph name
    Graph1X.SetTitle(Title[0])
    Graph2X.SetTitle(Title[0])
    Graph1Y.SetTitle(Title[1])
    Graph2Y.SetTitle(Title[1])
    Graph1.SetTitle(Title[2])
    Graph2.SetTitle(Title[2])
    GraphSubtX.SetTitle(Title[3])
    GraphSubtY.SetTitle(Title[4])
    GraphSubt.SetTitle(Title[5])
    
    return Graph1X, Graph2X, Graph1Y, Graph2Y, Graph1, Graph2, GraphSubtX, GraphSubtY, GraphSubt


def FitLockinPeak(Graph, XYName):
    # Define fitting function
    fBreit = ROOT.TF1("fBreit",
                      conf.FunctionBreitWigner,
                      conf.FitRange[0], conf.FitRange[1])
    fBG    = ROOT.TF1("fBG",
                      conf.FunctionBackground,
                      conf.FitRange[0], conf.FitRange[1])
    fBreitBG = ROOT.TF1("fBreitBG",
                        "fBreit + fBG",
                        conf.FitRange[0], conf.FitRange[1])
    
    # Set parameters
    for iPara in range(7):
        fBreitBG.SetParLimits(iPara, conf.ParameterLimitBritWignerBG[iPara][0], conf.ParameterLimitBritWignerBG[iPara][1])
        if XYName == "X":
            fBreitBG.SetParameters(iPara, conf.InitialValueBritWignerBGX[iPara])
        elif XYName == "Y":
            fBreitBG.SetParameters(iPara, conf.InitialValueBritWignerBGY[iPara])
        
    # Fit
    for i in range(5):
        Graph.Fit(fBreitBG, "Q", "", conf.FitRange[0], conf.FitRange[1])
        if(i==4):
            Graph.Fit(fBreitBG, "", "", conf.FitRange[0], conf.FitRange[1])

    # Fix parameters
    for iPara in range(3):
        fBreit.FixParameter(iPara, fBreitBG.GetParameter(iPara))
    
    PeakValue      = fBreit.Eval(fBreitBG.GetParameter(2))
    #    PeakValueError = fBreit.Eval(fBreitBG.GetParError(2))
    PeakValueError = fBreitBG.GetParError(0)/fBreitBG.GetParameter(0) * PeakValue
    
    return PeakValue, PeakValueError

def DataOutputToPeakValueFile(PeakValue, PeakValueError, BinaryFileName):
    # time
    NowTime = datetime.datetime.now()
    if conf.OptOnlyLockin:
        src_stats = os.stat(BinaryFileName)
        src_birthtimestamp = src_stats.st_birthtime
        NowTime = datetime.datetime.fromtimestamp(src_birthtimestamp)
        
    # Calculate elapsed time
    ElapsedTime = datetime.datetime.now()
    if os.path.exists(conf.FileNamePeakValue):
        df = pd.read_csv(conf.FileNamePeakValue,
                         names=("Time", "Elapsed", "PeakValue", "PeakValueError"), header=0)
        ElapsedTime = NowTime - datetime.datetime.strptime(df["Time"][0], '%Y-%m-%d %H:%M:%S.%f')  # timedelta since experiment start
    else:
        ElapsedTime = NowTime - conf.const.StartTime                                           # timedelta since program start
        if conf.OptOnlyLockin:
            ElapsedTime = NowTime - NowTime
        else:
            ElapsedTime = NowTime - conf.const.StartTime                                           # timedelta since program start            

    # Data output
    #    DataDictionary = dict(Time=[NowTime], Elapsed=[ElapsedTime.seconds/60.], PeakValue=PeakValue, PeakValueError=PeakValueError)  # ElapsedTime -> [min]
    DataDictionary = dict(Time=[NowTime], Elapsed=[round(ElapsedTime.total_seconds()/60.,1)], PeakValue=round(PeakValue,4), PeakValueError=round(PeakValueError,4))  # ElapsedTime -> [min]
    df = pd.DataFrame(data=DataDictionary)
    header = FileInfo.addHeader(conf.FileNamePeakValue)
    df.to_csv(conf.FileNamePeakValue, mode="a", header=header, index=False)
    
def fft(BinaryFileName, V, Time):
    Ndata = len(V)
    sampling_rate = 1 / (Time[1] - Time[0])  # 時刻の間隔からサンプリング周波数を求める
    V -= np.mean(V)
    frequency_spectrum = np.fft.fft(V)
    frequencies = np.fft.fftfreq(Ndata, d=1/sampling_rate)
    return Ndata, frequency_spectrum, frequencies

def main(BinaryFileName1, BinaryFileName2):
    # Lockin for data 1
    LockinDataFrame1 = Lockin(BinaryFileName1)
    # Lockin for data 2
    LockinDataFrame2 = Lockin(BinaryFileName2)

    # Add Error column to DataFrame
    Npoint = len(LockinDataFrame1)
    LockinDataFrame1["XError"] = [0 for ip in range(Npoint)]
    LockinDataFrame1["YError"] = [0.00005 for ip in range(Npoint)] # Error of Y-axis is fixed to 0.0005
    LockinDataFrame2["XError"] = [0 for ip in range(Npoint)]
    LockinDataFrame2["YError"] = [0.00005 for ip in range(Npoint)] # Error of Y-axis is fixed to 0.0005    
    
    # Make Graphs
    Graph1X, Graph2X, Graph1Y, Graph2Y, Graph1, Graph2, GraphSubtX, GraphSubtY, GraphSubt = MakeLockinGraphs(LockinDataFrame1, LockinDataFrame2)
    
    # Plot Graphs
    c = ROOT.TCanvas("c", "c", 1400, 800)
    c.Divide(3,2)
    DrawGraph.GraphDesign()
    c.cd(1)
    Graph1X.Draw("aple")
    Graph2X.Draw("plesame")
    c.cd(2)
    Graph1Y.Draw("aple")
    Graph2Y.Draw("pelsame")
    c.cd(3)
    Graph1.Draw("aple")
    Graph2.Draw("plesame")
    c.cd(4)
    GraphSubtX.Draw("aple")
    c.cd(5)
    GraphSubtY.Draw("aple")
    c.cd(6)
    GraphSubt.Draw("aple")

    # Get Peak Value
    PeakValueX, PeakValueErrorX = FitLockinPeak(GraphSubtX, "X")
    PeakValueY, PeakValueErrorY = FitLockinPeak(GraphSubtY, "Y")
    print("PeakValueX: {0}+/-{1}, PeakValueY: {1}+/-{2}".format(PeakValueX, PeakValueErrorX, PeakValueY, PeakValueErrorY))
    
    # Save PDF of figure
    PDFFileName = BinaryFileName2 + ".pdf"
    c.Update()    
    c.SaveAs(PDFFileName)

    # Output Peak data to CSV file
    DataOutputToPeakValueFile(abs(PeakValueX), abs(PeakValueErrorX), BinaryFileName1)
    
    
if __name__ == '__main__':
    main()
