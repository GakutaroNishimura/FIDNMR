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

f_0 = 18400.0
f_min = f_0-60.0*2
f_max = f_0+60.0*2

# f_0 = 18500.0
# f_dev = 500.0
# f_min = f_0-f_dev
# f_max = f_0+f_dev

# f_0 = 18920.0
# f_min = f_0-150.0
# f_max = f_0+150.0

# f_0 = 18920.0
# f_min = f_0-400.0
# f_max = f_0+400.0

freq = []
amp = []

j = 0

for i in df.freq:
    if i > 18000 and i < 19000:
        freq.append(i)
        iamp = df.amplitude[j] - (-160.23544456164237 + 0.017317993774758424*i - 4.67413966835862e-07*i**2)
        if iamp < 0:
            amp.append(0.0)
        else:
            amp.append(iamp)
    j += 1
        

#gr = ROOT.TGraph(len(df.freq), np.array(df.freq), np.array(df.amplitude))
gr = ROOT.TGraph(len(freq), np.array(freq), np.array(amp))
#gr_fit = ROOT.TF1("f", "[2]*[0]/(pow((x-[1]), 2) + [0]*[0]) + [3]", f_min, f_max)
#gr_BGfit = ROOT.TF1("f", "pol2", f_min, f_max)
gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-18389.0), 2) + [0]*[0])", f_min, f_max)

#gr_fit.SetParameters(4.0, 18404., 12.8)
gr_fit.SetParameters(0.7426, 2.195)
#gr_fit.SetParameters(4.0, 18404., 12.8, 0.14)
#gr_fit.SetParameters(13.13, 18920., 500.0, 1.5)
# gr_fit.SetParameters(15.0, 18920., 500.0)

# gr_BGfit.SetParameters(-160.0, 0.015, -4.5)

gr_fit.SetNpx(10000)
gr.Fit(gr_fit, "QR")
par = [gr_fit.GetParameter(k) for k in range(gr_fit.GetNpar())]

# gr.Fit(gr_BGfit, "QR")
# par = [gr_BGfit.GetParameter(k) for k in range(gr_BGfit.GetNpar())]
print(par)

# integral = gr_fit.Integral(f_min, f_max)
# fwhm = 2*par[0]
# T2 = 1/(np.pi*fwhm)
# print("FWHM is %f" %fwhm)
# print("T2 is %f" %T2)
# print("function integral is %f" %integral)

gr.Draw("APL")
gr.GetXaxis().SetRangeUser(f_min, f_max)
#gr.GetYaxis().SetRangeUser(0.0, 3.5)
ROOT.gStyle.SetOptFit(1)
gr.SetMarkerStyle(7)
gr.SetMarkerSize(10)
c1 = ROOT.gROOT.FindObject("c1")
c1.Draw("same")
# c1.SaveAs(DirPath + "PeakFit.pdf")

# f=open(argvs[1],"a")
# f.write("%f %f %f %f %f\n" %(voltage, integral, par[0], par[1], par[2]))
# f.close()