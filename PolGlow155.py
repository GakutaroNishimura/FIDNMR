import ROOT
import numpy as np
import pandas as pd

time = [0.0, 2., 4., 6., 8., 11., 13., 18., 28.]
df155 = pd.read_table("./FIDAbsPol155.txt", names=["amp", "ampE", "T2"], sep=" ")

gr100 = ROOT.TGraphErrors(len(time), np.array(time), np.array(df155.amp), np.array([0.0 for i in range(len(time))]), np.array(df155.ampE))
# gr100.SetMarkerStyle(22)
# gr100.SetMarkerSize(1.4)
gr100.SetMarkerStyle(20)
gr100.SetMarkerSize(1.0)
# gr100.SetMarkerColor(ROOT.kBlack)
# gr100.SetLineColor(ROOT.kBlack)
gr_fit100 = ROOT.TF1("f", "[0]*(1-exp(-x/[1]))", time[0], time[-1])
# gr_fit100.SetLineColor(ROOT.kBlack)
# gr_fit100.SetLineStyle(1)
gr_fit100.SetTitle("100")
# gr_fit100.SetParameters(5.0, 8.) #for Integral
gr_fit100.SetParameters(0.04, 3.) #for Absolute polarization
gr100.Fit(gr_fit100, "QR")
par100 = [gr_fit100.GetParameter(k) for k in range(gr_fit100.GetNpar())]
par100E = [gr_fit100.GetParError(k) for k in range(gr_fit100.GetNpar())]
print(par100)
print(par100E)
gr100.Draw("AP")
gr100.SetTitle("")
gr100.GetXaxis().SetTitle("time [s]")
gr100.GetYaxis().SetTitle("polarization %")
gr100.GetXaxis().SetLabelSize(0.06)
gr100.GetYaxis().SetLabelSize(0.06)
gr100.GetXaxis().SetTitleSize(0.07)
gr100.GetYaxis().SetTitleSize(0.07)
gr100.GetXaxis().SetTitleOffset(0.85)
gr100.GetYaxis().SetTitleOffset(0.9)
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetLeftMargin(0.15)
ROOT.gPad.SetRightMargin(0.05)
c1 = ROOT.gROOT.FindObject("c1")
c1.Draw("same")