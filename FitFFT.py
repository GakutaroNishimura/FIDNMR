import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import ROOT
import os
import sys
import time

argvs = sys.argv  
argc = len(argvs) 

Time = [2., 7., 12., 17., 27., 37., 57.]
PeakInt = []

NStart = 11
NStop = NStart+7

for i in range(NStart, NStop):

    DirPath = "./Data/2023/0727/test" + str(36) + "/"
    DataPath = DirPath + "10/ftdata2.csv"
    SavePath = "./Data/2023/0727/test120/"
    os.makedirs(SavePath, exist_ok=True)
    df = pd.read_csv(DataPath, names=["freq", "amplitude"])

    gr_raw = ROOT.TGraph(len(df.freq), np.array(df.freq), np.array(df.amplitude))
    #gr_fitBG = ROOT.TF1("f1", "pol2", 17986., 19170.)
    gr_fitBG = ROOT.TF1("f1", "[0]+[1]*x+[2]*x*x+[3]/((x-[4])*(x-[4])+[5]*[5])", 17926., 19170.)
    func = ROOT.TF1("func", "[0]/((x-[1])*(x-[1])+[2]*[2])", 17926., 19170.)
    """
    PeakIndex = 2510
    exclude_indices = [PeakIndex-1, PeakIndex, PeakIndex+1]

    # フィッティングを実行（除外したいデータ点はRejectPointで除外）
    for i in range(len(df.freq)):
        if i in exclude_indices:
            continue
            #gr_fitBG.RejectPoint(i)
        else:
            gr_raw.SetPoint(i, df.freq[i], df.amplitude[i])
    """

    c1 = ROOT.TCanvas("c1", "c1", 600, 600)
    gr_raw = ROOT.TGraph(len(df.freq), np.array(df.freq), np.array(df.amplitude))
    gr_fitBG.SetParameters(-11., 0.0012, -3.4e-8, 17.6, 18381.3, 3.09)
    gr_fitBG.SetNpx(10000)
    gr_raw.Fit(gr_fitBG, "QR")
    par = [gr_fitBG.GetParameter(k) for k in range(gr_fitBG.GetNpar())]
    gr_raw.Draw("APL")
    gr_raw.SetMarkerStyle(20)
    gr_raw.SetMarkerSize(0.7)
    gr_raw.GetXaxis().SetTitle("frequency [Hz]")
    gr_raw.GetYaxis().SetTitle("amplitude [V/Hz]")
    gr_raw.GetXaxis().SetRangeUser(18320., 18440.)
    #gr.GetYaxis().SetRangeUser(0., 2.1)
    #c1 = ROOT.gROOT.FindObject("c1")
    ROOT.gStyle.SetOptFit(1)
    c1.Draw("same")
    time.sleep(1000)
    c1.SaveAs(SavePath + "%d.pdf" %i)

    func.SetParameters(par[3], par[4], par[5])
    integral = func.Integral(17926., 19170.)
    print("Integral:", integral)
    PeakInt.append(integral)
    
    if argc == 2:
        with open(SavePath + argvs[1], "a") as f:
            f.write("%f\n" %(integral))

    """
    gr_BGsub = ROOT.TGraph()
    for i in range(len(df.freq)):
        if df.freq[i]<18000.0 or df.freq[i]>19000.0:
            continue
        else:
            freq = df.freq[i]
            amp = df.amplitude[i]-(par[0]+par[1]*freq+par[2]*freq**2)
            if amp<0: amp = 0.0
            gr_BGsub.SetPoint(i, freq, amp)

    c2 = ROOT.TCanvas("c2", "c2", 600, 600)
    gr_BGsub.Draw("APL")
    gr_BGsub.SetMarkerStyle(7)
    gr_BGsub.SetMarkerSize(10)
    gr_BGsub.GetXaxis().SetRangeUser(18000., 19000.)
    #c2 = ROOT.gROOT.FindObject("c1")
    #c2.Draw("same")


    gr_fitPeak = gr_BGsub
    c3 = ROOT.TCanvas("c3", "c3", 600, 600)
    gr_fit = ROOT.TF1("f", "[0]/(pow((x-[1]), 2)+pow([2], 2))", 18302.0, 18513.0)
    gr_fit.SetParameters(12.0, 18397.9, 2.0)
    #gr_fit = ROOT.TF1("f", "gaus", 18302.0, 18513.0)
    #gr_fit.SetParameters(1.0, 18397.9, 5.0)
    gr_fit.SetNpx(10000)
    gr_fitPeak.Fit(gr_fit, "Q")
    par = [gr_fit.GetParameter(k) for k in range(gr_fit.GetNpar())]
    gr_fitPeak.Draw("APL")
    gr_fitPeak.SetMarkerStyle(21)
    gr_fitPeak.SetMarkerSize(1.0)
    gr_fitPeak.GetXaxis().SetRangeUser(18300., 18500.)
    gr_fitPeak.GetYaxis().SetRangeUser(0., 3.5)
    #c1 = ROOT.gROOT.FindObject("c1")
    c3.Draw("same")
    """


c2 = ROOT.TCanvas("c2", "c2", 600, 600)
gr_PolGlow = ROOT.TGraph(len(Time), np.array(Time), np.array(PeakInt))
gr_FitPolGlow = ROOT.TF1("f", "[0]+[1]*(1-exp(-x/[2]))", 0., 60.)
gr_FitPolGlow.SetParameters(10., 10., 15.)
gr_PolGlow.Fit(gr_FitPolGlow, "QR")
gr_PolGlow.SetMarkerStyle(20)
gr_PolGlow.SetMarkerSize(0.7)
gr_PolGlow.Draw("AP")
gr_PolGlow.GetXaxis().SetTitle("time [s]")
gr_PolGlow.GetYaxis().SetTitle("peak integral [V/Hz]")
ROOT.gStyle.SetOptFit(1)
stats = gr_PolGlow.GetListOfFunctions().FindObject("stats")
stats.SetX1NDC(0.65)  # X座標を調整
stats.SetY1NDC(0.3)   # Y座標を調整
stats.SetX2NDC(0.95)  # X座標を調整
stats.SetY2NDC(0.5)   # Y座標を調整
c2.Draw("same")
c2.SaveAs(SavePath + "PolGlow.pdf")



