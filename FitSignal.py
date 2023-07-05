import numpy as np
import pandas as pd
import ROOT
import Config as conf

#path = "./data/scope_260.csv"
#df = pd.read_csv(path, names=["time", "RFsignal", "PickUpsignal", "sync2"], skiprows=2, skipfooter=1, engine="python")
df = pd.read_table(conf.DataName, sep=" ", names = ["time", "signal"])
Time = np.array(df.time, dtype="d")
V_mean = np.array(df.signal, dtype="d")

# "./data/scope_260.csv"
#x_min = 2000
#x_max = 19900

# 129Xe_069A_19kHz/run6
x_min = 0
x_max = 150000

#gr = ROOT.TGraph(len(df.time[x_min:x_max]), np.array(df.time[x_min:x_max]), np.array(df.PickUpsignal[x_min:x_max]))
gr = ROOT.TGraph(len(df.time[x_min:x_max]), np.array(df.time[x_min:x_max]), np.array(df.signal[x_min:x_max]))
gr_fit = ROOT.TF1("f", "[0]*expo(-[1]*x)*sin(2*pi*[2]*x+[3]) + [4]", df.time[x_min], df.time[x_max])
#gr_fit.SetParameters(-6.61436292e-03,  6.50124722e+01,  1.81216540e+04,  1.41380037e+00)
#gr_fit.SetParameters(0.01415861885725226, 13.324007257585418, 18117.27312027492, 0.) # "./data/scope_260.csv"
gr_fit.SetParameters(0.04341888572810267, 5.383077353509305, 18900.682613541823, -35.1607898488646, 0.0020867903362365692) # 129Xe_069A_19kHz/run6
gr_fit.SetNpx(10000)
gr.Fit(gr_fit, "QR")
par = [gr_fit.GetParameter(k) for k in range(gr_fit.GetNpar())]
print(par)
gr.Draw("APL")
gr.SetMarkerStyle(7)
gr.SetMarkerSize(10)
ROOT.gStyle.SetOptFit(1)
c1 = ROOT.gROOT.FindObject("c1")
c1.Draw("same")

