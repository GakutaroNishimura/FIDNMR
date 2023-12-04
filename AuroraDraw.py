import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ROOT

DirPath = "./Data/2023/0720/test21/"
DataPath = DirPath + "1/ftdata2.csv"

# DirPath = "./Data/2023/0728/test01/"
# DataPath = DirPath + "10/ftdata2.csv"

df = pd.read_csv(DataPath, names=["freq", "amplitude"])

# f_0 = 18400.0
# f_min = f_0-60.0*2
# f_max = f_0+60.0*2

f_0 = 18920.0
f_min = f_0-150.0
f_max = f_0+150.0

gr = ROOT.TGraph(len(df.freq), np.array(df.freq), np.array(df.amplitude))
gr_fit = ROOT.TF1("f", "[2]*[0]/(pow((x-[1]), 2) + [0]*[0]) + [3]", f_min, f_max)
#gr_fit.SetParameters(4.0, 18404., 12.8, 0.14)
gr_fit.SetParameters(13.13, 18920., 500.0, 1.5)
gr_fit.SetNpx(10000)
gr.Fit(gr_fit, "QR")
par = [gr_fit.GetParameter(k) for k in range(gr_fit.GetNpar())]
print(par)

fwhm = 2*par[0]
T2 = 1/(np.pi*fwhm)
print("FWHM is %f" %fwhm)
print("T2 is %f" %T2)

gr.Draw("APL")
gr.GetXaxis().SetRangeUser(f_min, f_max)
gr.GetYaxis().SetRangeUser(0.0, 3.5)
ROOT.gStyle.SetOptFit(1)
gr.SetMarkerStyle(7)
gr.SetMarkerSize(10)
c1 = ROOT.gROOT.FindObject("c1")
c1.Draw("same")

