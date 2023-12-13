import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ROOT
import sys
import Config as conf

argvs = sys.argv

DataPath = conf.DataPath + "ftdata2.csv"

voltage = 1.0

# DirPath = "./Data/2023/0728/test01/"
# DataPath = DirPath + "10/ftdata2.csv"

df = pd.read_csv(DataPath, names=["freq", "amplitude"])

f_0 = 18390.0
f_dev = 50
f_min = f_0-f_dev
f_max = f_0+f_dev

f_0BG = 18400.0
f_devBG = 400.0
f_minBG = f_0BG-f_devBG
f_maxBG = f_0BG+f_devBG

# f_0 = 18920.0
# f_min = f_0-150.0
# f_max = f_0+150.0

# f_0 = 18920.0
# f_min = f_0-400.0
# f_max = f_0+400.0

def FitFunc(DirPath, df):
    c = ROOT.TCanvas("c", "title", 900, 600)
    #c2 = ROOT.TCanvas("c", "title", 900, 600)
    c.Divide(1,2)
    c.cd(1)

    #c.cd()
    freqBG = []
    ampBG = []
    j = 0
    for i in df.freq:
        if i > f_minBG and i < f_min:
            freqBG.append(i)
            iamp = df.amplitude[j]
            ampBG.append(iamp)
        if i > f_max and i < f_maxBG:
            freqBG.append(i)
            iamp = df.amplitude[j]
            ampBG.append(iamp)
        j += 1


    freq = []
    amp = []
    j = 0
    for i in df.freq:
        if i > f_minBG and i < f_maxBG:
            iamp = df.amplitude[j]
            amp.append(iamp)
        j += 1
    amp_max = max(amp)
    amp = []

    grBG = ROOT.TGraph(len(freqBG), np.array(freqBG), np.array(ampBG))
    grBGplot = ROOT.TGraph(len(df.freq), np.array(df.freq), np.array(df.amplitude))
    gr_fitBG = ROOT.TF1("f", "pol2", f_minBG, f_maxBG)
    gr_fitBG.SetParameters(-160.0, 0.015, -4.5e-7)
    gr_fitBG.SetNpx(10000)
    grBG.Fit(gr_fitBG, "QRS")
    parBG = [gr_fitBG.GetParameter(k) for k in range(gr_fitBG.GetNpar())]
    print(parBG)
    grBG.SetMarkerStyle(7)
    grBG.SetMarkerSize(10)
    grBGplot.SetMarkerStyle(7)
    grBGplot.SetMarkerSize(10)
    grBG.SetTitle("fitting back ground")
    grBG.GetXaxis().SetTitle("frequency [Hz]")
    grBG.GetYaxis().SetTitle("amplitude [#muV/Hz]")
    grBG.GetXaxis().SetLabelSize(0.06)
    grBG.GetYaxis().SetLabelSize(0.06)
    grBG.GetXaxis().SetTitleSize(0.07)
    grBG.GetYaxis().SetTitleSize(0.07)
    grBG.GetXaxis().SetTitleOffset(0.85)
    grBG.GetYaxis().SetTitleOffset(0.6)

    grBG.Draw("AP")
    grBGplot.Draw("PL")
    grBG.GetYaxis().SetRangeUser(0.0, amp_max*1.5)
    ROOT.gPad.SetTopMargin(0.1)
    ROOT.gPad.SetBottomMargin(0.15)
    ROOT.gPad.SetLeftMargin(0.1)
    ROOT.gPad.SetRightMargin(0.05)
    c.Update()


    c.cd(2)

    freq = []
    amp = []
    j = 0
    for i in df.freq:
        if i > f_minBG and i < f_maxBG:
            freq.append(i)
            iamp = df.amplitude[j] - (parBG[0] + parBG[1]*i + parBG[2]*i**2)
            if iamp < 0:
                amp.append(0.0)
            else:
                amp.append(iamp)
        j += 1
            

    #gr = ROOT.TGraph(len(df.freq), np.array(df.freq), np.array(df.amplitude))
    gr = ROOT.TGraph(len(freq), np.array(freq), np.array(amp))
    #gr_fit = ROOT.TF1("f", "[2]*[0]/(pow((x-[1]), 2) + [0]*[0]) + [3]", f_min, f_max)
    #gr_BGfit = ROOT.TF1("f", "pol2", f_min, f_max)
    # gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-18397.0), 2) + [0]*[0])", f_min, f_max)
    # gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-18391.0), 2) + [0]*[0])", f_min, f_max)
    # gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-18383.0), 2) + [0]*[0])", f_min, f_max)
    gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-[2]), 2) + [0]*[0])", f_min, f_max)


    gr_fit.SetParameters(4.0, 12.8, 18391.)
    # gr_fit.SetParameters(4.0, 12.8)
    # gr_fit.SetParameters(0.7426, 2.195)
    #gr_fit.SetParameters(4.0, 18404., 12.8, 0.14)
    #gr_fit.SetParameters(13.13, 18920., 500.0, 1.5)
    # gr_fit.SetParameters(15.0, 18920., 500.0)

    # gr_BGfit.SetParameters(-160.0, 0.015, -4.5)

    gr_fit.SetNpx(10000)
    gr.Fit(gr_fit, "QR")
    par = [gr_fit.GetParameter(k) for k in range(gr_fit.GetNpar())]
    print(par)

    integral = gr_fit.Integral(f_min, f_max)
    fwhm = 2*par[0]
    T2 = 1/(np.pi*fwhm)
    print("FWHM is %f" %fwhm)
    print("T2 is %f" %T2)
    print("function integral is %f" %integral)
    ROOT.gPad.SetTopMargin(0.1)
    ROOT.gPad.SetBottomMargin(0.15)
    ROOT.gPad.SetLeftMargin(0.1)
    ROOT.gPad.SetRightMargin(0.05)
    ROOT.gStyle.SetStatX(0.9)
    ROOT.gStyle.SetStatY(0.8)
    ROOT.gStyle.SetStatW(0.14)
    ROOT.gStyle.SetStatH(0.2)
    gr.SetTitle("fitting peak after BG subtraction")
    gr.GetXaxis().SetTitle("frequency [Hz]")
    gr.GetYaxis().SetTitle("amplitude [#muV/Hz]")
    gr.GetXaxis().SetLabelSize(0.06)
    gr.GetYaxis().SetLabelSize(0.06)
    gr.GetXaxis().SetTitleSize(0.07)
    gr.GetYaxis().SetTitleSize(0.07)
    gr.GetXaxis().SetTitleOffset(0.85)
    gr.GetYaxis().SetTitleOffset(0.6)

    gr.Draw("APL")
    # gr.GetXaxis().SetRangeUser(f_min, f_max)
    gr.GetYaxis().SetRangeUser(0.0, par[1]/par[0]*1.5)
    ROOT.gStyle.SetOptFit(1)
    gr.SetMarkerStyle(7)
    gr.SetMarkerSize(10)

    #c1 = ROOT.gROOT.FindObject("c1")
    c.Update()
    c.Draw("same")
    # c2.Draw("same")
    c.SaveAs(DirPath + "PeakFit.pdf")
    #c.Close()

    f=open(argvs[1],"a")
    # f.write("%f %f %f %f %f\n" %(voltage, integral, par[0], par[1], par[2]))
    f.write("%f %f\n" %(integral, T2))
    f.close()