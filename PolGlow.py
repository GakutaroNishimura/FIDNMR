import ROOT
import numpy as np
import pandas as pd

time = [0.0, 2., 7., 12., 17., 27., 37., 57.]
#time = [7., 12., 17., 27., 37., 57.] #110
#amplitude = [0.437551, 0.473369, 0.633478, 0.722147, 0.694416, 0.591403, 0.658201] #100
#amplitude = [0.491034, 0.620165, 0.793393, 0.622123, 0.710504, 0.65927] #110
#amplitude = [0.43229, 0.689053, 1.01882, 0.947034, 0.990453, 0.868595, 0.84074] #120
#amplitude = [0.359947, 0.718809, 0.828886, 0.664256, 0.925595, 0.862325, 0.987762] #130
#amplitude = [0.505634, 0.848728, 0.724358, 0.945877, 1.00124, 1.07725, 0.972557] #140
# amplitude = [0.722924, 1.12504, 1.24068, 1.31561, 1.37747, 1.18928, 1.2161] #150

df100 = pd.read_table("./FIDPeakIntegral100.txt", names=["amp", "T2"], sep=" ")
df110 = pd.read_table("./FIDPeakIntegral110.txt", names=["amp", "T2"], sep=" ")
df120 = pd.read_table("./FIDPeakIntegral120.txt", names=["amp", "T2"], sep=" ")
df130 = pd.read_table("./FIDPeakIntegral130.txt", names=["amp", "T2"], sep=" ")
df140 = pd.read_table("./FIDPeakIntegral140.txt", names=["amp", "T2"], sep=" ")
df150 = pd.read_table("./FIDPeakIntegral150.txt", names=["amp", "T2"], sep=" ")

c = ROOT.TCanvas("c", "title", 900, 600)
legend = ROOT.TLegend(0.81,0.9,1.0,0.55)

# gr = ROOT.TGraph(len(time), np.array(time), np.array(amplitude))
gr100 = ROOT.TGraph(len(time), np.array(time), np.array(df100.amp))
gr100.SetMarkerStyle(22)
gr100.SetMarkerSize(1.4)
gr100.SetMarkerColor(ROOT.kBlack)
gr100.SetLineColor(ROOT.kBlack)
gr_fit100 = ROOT.TF1("f", "[0]*(1-exp(-x/[1]))", time[0], time[-1])
gr_fit100.SetLineColor(ROOT.kBlack)
gr_fit100.SetLineStyle(1)
gr_fit100.SetTitle("100")
gr_fit100.SetParameters(5.0, 8.)
gr100.Fit(gr_fit100, "QR")
par100 = [gr_fit100.GetParameter(k) for k in range(gr_fit100.GetNpar())]
print(par100)

gr110 = ROOT.TGraph(len(time), np.array(time), np.array(df110.amp))
gr110.SetMarkerStyle(25)
gr110.SetMarkerSize(1.0)
gr110.SetMarkerColor(ROOT.kBlue)
gr110.SetLineColor(ROOT.kBlue)
gr_fit110 = ROOT.TF1("f", "[0]*(1-exp(-x/[1]))", time[0], time[-1])
gr_fit110.SetLineColor(ROOT.kBlue)
gr_fit110.SetLineStyle(2)
gr_fit110.SetTitle("110")
gr_fit110.SetParameters(5.0, 8.)
gr110.Fit(gr_fit110, "QR")
par110 = [gr_fit110.GetParameter(k) for k in range(gr_fit110.GetNpar())]
print(par110)

gr120 = ROOT.TGraph(len(time), np.array(time), np.array(df120.amp))
gr120.SetMarkerStyle(20)
gr120.SetMarkerSize(1.0)
gr120.SetMarkerColor(ROOT.kRed)
gr120.SetLineColor(ROOT.kRed)
gr_fit120 = ROOT.TF1("f", "[0]*(1-exp(-x/[1]))", time[0], time[-1])
gr_fit120.SetLineColor(ROOT.kRed)
gr_fit120.SetLineStyle(7)
gr_fit120.SetTitle("120")
gr_fit120.SetParameters(5.0, 8.)
gr120.Fit(gr_fit120, "QR")
par120 = [gr_fit120.GetParameter(k) for k in range(gr_fit120.GetNpar())]
print(par120)

gr130 = ROOT.TGraph(len(time), np.array(time), np.array(df130.amp))
gr130.SetMarkerStyle(3)
gr130.SetMarkerSize(1.8)
gr130.SetMarkerColor(ROOT.kGreen)
gr130.SetLineColor(ROOT.kGreen)
gr_fit130 = ROOT.TF1("f", "[0]*(1-exp(-x/[1]))", time[0], time[-1])
gr_fit130.SetLineColor(ROOT.kGreen)
gr_fit130.SetLineStyle(9)
gr_fit130.SetTitle("130")
gr_fit130.SetParameters(5.0, 8.)
gr130.Fit(gr_fit130, "QR")
par130 = [gr_fit130.GetParameter(k) for k in range(gr_fit130.GetNpar())]
print(par130)

gr140 = ROOT.TGraph(len(time), np.array(time), np.array(df140.amp))
gr140.SetMarkerStyle(28)
gr140.SetMarkerSize(1.4)
gr140.SetMarkerColor(ROOT.kMagenta)
gr140.SetLineColor(ROOT.kMagenta)
gr_fit140 = ROOT.TF1("f", "[0]*(1-exp(-x/[1]))", time[0], time[-1])
gr_fit140.SetLineColor(ROOT.kMagenta)
gr_fit140.SetLineStyle(10)
gr_fit140.SetTitle("140")
gr_fit140.SetParameters(5.0, 8.)
gr140.Fit(gr_fit140, "QR")
par140 = [gr_fit140.GetParameter(k) for k in range(gr_fit140.GetNpar())]
print(par140)

gr150 = ROOT.TGraph(len(time), np.array(time), np.array(df150.amp))
gr150.SetMarkerStyle(39)
gr150.SetMarkerSize(2.0)
gr150.SetMarkerColor(ROOT.kCyan)
gr150.SetLineColor(ROOT.kCyan)
gr_fit150 = ROOT.TF1("f", "[0]*(1-exp(-x/[1]))", time[0], time[-1])
gr_fit150.SetLineColor(ROOT.kCyan)
gr_fit150.SetParameters(15.0, 8.)
gr_fit150.SetLineColor(ROOT.kCyan)
gr_fit150.SetLineStyle(6)
gr_fit150.SetTitle("150")
gr150.Fit(gr_fit150, "QR")
par150 = [gr_fit150.GetParameter(k) for k in range(gr_fit150.GetNpar())]
print(par150)

#par = [gr_fit100.GetParameter(k) for k in range(gr_fit100.GetNpar())]
#print(par)
#gr.GetYaxis().SetRangeUser(0., 0.8)
gr150.SetTitle("")

gr150.Draw("AP")
gr140.Draw("P")
gr130.Draw("P")
gr120.Draw("P")
gr110.Draw("P")
gr100.Draw("P")

gr150.GetXaxis().SetTitle("time [s]")
gr150.GetYaxis().SetTitle("amplitude [#muV]")

gr150.GetXaxis().SetLabelSize(0.06)
gr150.GetYaxis().SetLabelSize(0.06)
gr150.GetXaxis().SetTitleSize(0.07)
gr150.GetYaxis().SetTitleSize(0.07)
gr150.GetXaxis().SetTitleOffset(0.85)
gr150.GetYaxis().SetTitleOffset(0.6)

ROOT.gPad.SetTopMargin(0.05)
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetLeftMargin(0.1)
ROOT.gPad.SetRightMargin(0.2)

legend.AddEntry(gr_fit150, "150 #circ C", "lep")
legend.AddEntry(gr_fit140, "140 #circ C", "lep")
legend.AddEntry(gr_fit130, "130 #circ C", "lep")
legend.AddEntry(gr_fit120, "120 #circ C", "lep")
legend.AddEntry(gr_fit110, "110 #circ C", "lep")
legend.AddEntry(gr_fit100, "100 #circ C", "lep")
legend.Draw()
# gr.SetMarkerStyle(7)
# gr.SetMarkerSize(10)
# gr.SetTitle("150")
# ROOT.gStyle.SetOptFit(1)
# c1 = ROOT.gROOT.FindObject("c1")
c.Draw("same")