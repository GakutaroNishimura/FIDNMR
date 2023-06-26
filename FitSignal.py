import numpy as np
import pandas as pd
import ROOT

path = "./data/scope_260.csv"
df = pd.read_csv(path, names=["time", "RFsignal", "PickUpsignal", "sync2"], skiprows=2, skipfooter=1, engine="python")

x_min = 2000
x_max = 19900
gr = ROOT.TGraph(len(df.time[x_min:x_max]), np.array(df.time[x_min:x_max]), np.array(df.PickUpsignal[x_min:x_max]))
gr_fit = ROOT.TF1("f", "[0]*expo(-[1]*x)*sin(2*pi*[2]*x+[3])", df.time[x_min], df.time[x_max])
#gr_fit.SetParameters(-6.61436292e-03,  6.50124722e+01,  1.81216540e+04,  1.41380037e+00)
gr_fit.SetParameters(0.01415861885725226, 13.324007257585418, 18117.27312027492, 0.)
gr_fit.SetNpx(10000)
gr.Fit(gr_fit, "QR")
par = [gr_fit.GetParameter(k) for k in range(gr_fit.GetNpar())]
gr.Draw("APL")
gr.SetMarkerStyle(7)
gr.SetMarkerSize(10)
ROOT.gStyle.SetOptFit(1)
c1 = ROOT.gROOT.FindObject("c1")
c1.Draw("same")

