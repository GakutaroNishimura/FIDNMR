import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ROOT
import sys
import Config as conf

argvs = sys.argv

PeakPath = conf.DataPath + "ftdata2.csv"
SignalPath = conf.DataPath + "data.csv"

# DirPath = "./Data/2023/0728/test01/"
# DataPath = DirPath + "10/ftdata2.csv"

df_Peak = pd.read_csv(PeakPath, names=["freq", "amplitude"])
df_Signal = pd.read_csv(SignalPath, names=["time", "voltage"])

f_0 = 18400.0
f_min = f_0-400.0
f_max = f_0+400.0

# f_0 = 18920.0
# f_min = f_0-150.0
# f_max = f_0+150.0

# f_0 = 18920.0
# f_min = f_0-400.0
# f_max = f_0+400.0

c = ROOT.TCanvas("c", "title", 900, 600)
c.Divide(1,2)

c.cd(1)

gr_signal = ROOT.TGraph(len(df_Signal.time), np.array(df_Signal.time), np.array(df_Signal.voltage))
gr_signal.SetTitle("FID signal")
gr_signal.GetXaxis().SetTitle("time [s]")
gr_signal.GetYaxis().SetTitle("voltage [#muV]")
gr_signal.GetXaxis().SetLabelSize(0.06)
gr_signal.GetYaxis().SetLabelSize(0.06)
gr_signal.GetXaxis().SetTitleSize(0.07)
gr_signal.GetYaxis().SetTitleSize(0.07)
gr_signal.GetXaxis().SetTitleOffset(0.85)
gr_signal.GetYaxis().SetTitleOffset(0.6)
gr_signal.Draw("APL")
gr_signal.GetXaxis().SetRangeUser(0.0, 0.14)
#gr_signal.GetYaxis().SetRangeUser(0.0, 3.5)
#ROOT.gStyle.SetOptFit(1)
gr_signal.SetMarkerStyle(7)
gr_signal.SetMarkerSize(10)
ROOT.gPad.SetTopMargin(0.1)
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetLeftMargin(0.1)
ROOT.gPad.SetRightMargin(0.05)
c.Update()

c.cd(2)
gr_peak = ROOT.TGraph(len(df_Peak.freq), np.array(df_Peak.freq), np.array(df_Peak.amplitude))
gr_peak.SetTitle("magnitude spectrum")
gr_peak.GetXaxis().SetTitle("frequency [Hz]")
gr_peak.GetYaxis().SetTitle("amplitude [#muV/Hz]")
gr_peak.GetXaxis().SetLabelSize(0.06)
gr_peak.GetYaxis().SetLabelSize(0.06)
gr_peak.GetXaxis().SetTitleSize(0.07)
gr_peak.GetYaxis().SetTitleSize(0.07)
gr_peak.GetXaxis().SetTitleOffset(0.85)
gr_peak.GetYaxis().SetTitleOffset(0.6)
gr_peak.Draw("APL")
gr_peak.GetXaxis().SetRangeUser(f_min, f_max)
#gr_peak.GetYaxis().SetRangeUser(0.0, 3.5)
#ROOT.gStyle.SetOptFit(1)
gr_peak.SetMarkerStyle(7)
gr_peak.SetMarkerSize(10)
ROOT.gPad.SetTopMargin(0.1)
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetLeftMargin(0.1)
ROOT.gPad.SetRightMargin(0.05)
c.Draw("same")
#c.SaveAs(DirPath + "AuroraDraw.pdf")