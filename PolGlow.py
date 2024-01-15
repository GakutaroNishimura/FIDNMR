import ROOT
import numpy as np
import pandas as pd

time = [0.0, 2., 7., 12., 17., 27., 37., 57.]
time110 = [0.0, 7., 12., 17., 27., 37., 57.]
#time = [7., 12., 17., 27., 37., 57.] #110
#amplitude = [0.437551, 0.473369, 0.633478, 0.722147, 0.694416, 0.591403, 0.658201] #100
#amplitude = [0.491034, 0.620165, 0.793393, 0.622123, 0.710504, 0.65927] #110
#amplitude = [0.43229, 0.689053, 1.01882, 0.947034, 0.990453, 0.868595, 0.84074] #120
#amplitude = [0.359947, 0.718809, 0.828886, 0.664256, 0.925595, 0.862325, 0.987762] #130
#amplitude = [0.505634, 0.848728, 0.724358, 0.945877, 1.00124, 1.07725, 0.972557] #140
# amplitude = [0.722924, 1.12504, 1.24068, 1.31561, 1.37747, 1.18928, 1.2161] #150

# df100 = pd.read_table("./FIDPeakIntegral100.txt", names=["amp", "T2"], sep=" ")
# df110 = pd.read_table("./FIDPeakIntegral110.txt", names=["amp", "T2"], sep=" ")
# df120 = pd.read_table("./FIDPeakIntegral120.txt", names=["amp", "T2"], sep=" ")
# df130 = pd.read_table("./FIDPeakIntegral130.txt", names=["amp", "T2"], sep=" ")
# df140 = pd.read_table("./FIDPeakIntegral140.txt", names=["amp", "T2"], sep=" ")
# df150 = pd.read_table("./FIDPeakIntegral150.txt", names=["amp", "T2"], sep=" ")

# df110 = pd.read_table("./FIDPeakIntegral110.txt", names=["amp", "ampE", "T2"], sep=" ")
# df120 = pd.read_table("./FIDPeakIntegral120.txt", names=["amp", "ampE", "T2"], sep=" ")
# df130 = pd.read_table("./FIDPeakIntegral130.txt", names=["amp", "ampE", "T2"], sep=" ")
# df140 = pd.read_table("./FIDPeakIntegral140.txt", names=["amp", "ampE", "T2"], sep=" ")
# df150 = pd.read_table("./FIDPeakIntegral150.txt", names=["amp", "ampE", "T2"], sep=" ")

# df100 = pd.read_table("./FIDPeakIntegral100_AbsPol.txt", names=["amp", "T2"], sep=" ")
# df110 = pd.read_table("./FIDPeakIntegral110_AbsPol.txt", names=["amp", "T2"], sep=" ")
# df120 = pd.read_table("./FIDPeakIntegral120_AbsPol.txt", names=["amp", "T2"], sep=" ")
# df130 = pd.read_table("./FIDPeakIntegral130_AbsPol.txt", names=["amp", "T2"], sep=" ")
# df140 = pd.read_table("./FIDPeakIntegral140_AbsPol.txt", names=["amp", "T2"], sep=" ")
# df150 = pd.read_table("./FIDPeakIntegral150_AbsPol.txt", names=["amp", "T2"], sep=" ")

df120 = pd.read_table("./FIDAbsPol120.txt", names=["amp", "ampE"], sep=" ")
df130 = pd.read_table("./FIDAbsPol130.txt", names=["amp", "ampE"], sep=" ")
df140 = pd.read_table("./FIDAbsPol140.txt", names=["amp", "ampE"], sep=" ")
df150 = pd.read_table("./FIDAbsPol150.txt", names=["amp", "ampE"], sep=" ")

# c = ROOT.TCanvas("c", "title", 900, 600)
c = ROOT.TCanvas("c", "title", 900, 600)
#legend = ROOT.TLegend(0.81,0.9,1.0,0.55)

c.Divide(2, 2)

# c.cd(1)
# # gr = ROOT.TGraph(len(time), np.array(time), np.array(amplitude))
# gr100 = ROOT.TGraph(len(time), np.array(time), np.array(df100.amp))
# # gr100.SetMarkerStyle(22)
# # gr100.SetMarkerSize(1.4)
# gr100.SetMarkerStyle(20)
# gr100.SetMarkerSize(1.0)
# # gr100.SetMarkerColor(ROOT.kBlack)
# # gr100.SetLineColor(ROOT.kBlack)
# gr_fit100 = ROOT.TF1("f", "[0]*(1-exp(-x/[1]))", time[0], time[-1])
# # gr_fit100.SetLineColor(ROOT.kBlack)
# # gr_fit100.SetLineStyle(1)
# gr_fit100.SetTitle("100")
# # gr_fit100.SetParameters(5.0, 8.) #for Integral
# gr_fit100.SetParameters(0.02, 6.) #for Absolute polarization
# gr100.Fit(gr_fit100, "QR")
# par100 = [gr_fit100.GetParameter(k) for k in range(gr_fit100.GetNpar())]
# gr100.Draw("AP")
# ROOT.gPad.SetBottomMargin(0.15)
# ROOT.gPad.SetLeftMargin(0.2)
# ROOT.gPad.SetRightMargin(0.05)
# c.Update()
# print(par100)

# c.cd(1)
# # gr110 = ROOT.TGraph(len(time110), np.array(time110), np.array(df110.amp))
# gr110 = ROOT.TGraphErrors(len(time110), np.array(time110), np.array(df110.amp), np.array([0.0 for i in range(len(time110))]), np.array(df110.ampE))
# # gr110.SetMarkerStyle(25)
# # gr110.SetMarkerSize(1.0)
# gr110.SetMarkerStyle(20)
# gr110.SetMarkerSize(1.0)
# # gr110.SetMarkerColor(ROOT.kBlue)
# # gr110.SetLineColor(ROOT.kBlue)
# gr_fit110 = ROOT.TF1("f", "[0]*(1-exp(-x/[1]))", time110[0], time110[-1])
# # gr_fit110.SetLineColor(ROOT.kBlue)
# # gr_fit110.SetLineStyle(2)
# gr_fit110.SetTitle("110")
# gr_fit110.SetParameters(5.0, 8.) #for Integral
# # gr_fit110.SetParameters(0.02, 6.) #for Absolute polarization
# gr110.Fit(gr_fit110, "QR")
# par110 = [gr_fit110.GetParameter(k) for k in range(gr_fit110.GetNpar())]
# gr110.Draw("AP")
# ROOT.gPad.SetBottomMargin(0.15)
# ROOT.gPad.SetLeftMargin(0.2)
# ROOT.gPad.SetRightMargin(0.05)
# c.Update()
# print(par110)

c.cd(1)
# gr120 = ROOT.TGraph(len(time), np.array(time), np.array(df120.amp))
gr120 = ROOT.TGraphErrors(len(time), np.array(time), np.array(df120.amp), np.array([0.0 for i in range(len(time))]), np.array(df120.ampE))
gr120.SetMarkerStyle(20)
gr120.SetMarkerSize(1.0)
# gr120.SetMarkerColor(ROOT.kRed)
# gr120.SetLineColor(ROOT.kRed)
gr_fit120 = ROOT.TF1("f", "[0]*(1-exp(-x/[1]))", time[0], time[-1])
# gr_fit120.SetLineColor(ROOT.kRed)
# gr_fit120.SetLineStyle(7)
gr_fit120.SetTitle("120")
# gr_fit120.SetParameters(5.0, 8.) #for Integral
gr_fit120.SetParameters(0.02, 6.) #for Absolute polarization
gr120.Fit(gr_fit120, "QR")
par120 = [gr_fit120.GetParameter(k) for k in range(gr_fit120.GetNpar())]
parE120 = [gr_fit120.GetParError(k) for k in range(gr_fit120.GetNpar())]
gr120.Draw("AP")
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetLeftMargin(0.2)
ROOT.gPad.SetRightMargin(0.05)
c.Update()
print(par120)
print(parE120)

c.cd(2)
# gr130 = ROOT.TGraph(len(time), np.array(time), np.array(df130.amp))
gr130 = ROOT.TGraphErrors(len(time), np.array(time), np.array(df130.amp), np.array([0.0 for i in range(len(time))]), np.array(df130.ampE))
# gr130.SetMarkerStyle(3)
# gr130.SetMarkerSize(1.8)
gr130.SetMarkerStyle(20)
gr130.SetMarkerSize(1.0)
# gr130.SetMarkerColor(ROOT.kGreen)
# gr130.SetLineColor(ROOT.kGreen)
gr_fit130 = ROOT.TF1("f", "[0]*(1-exp(-x/[1]))", time[0], time[-1])
# gr_fit130.SetLineColor(ROOT.kGreen)
# gr_fit130.SetLineStyle(9)
gr_fit130.SetTitle("130")
# gr_fit130.SetParameters(5.0, 8.) #for Integral
gr_fit130.SetParameters(0.02, 6.) #for Absolute polarization
gr130.Fit(gr_fit130, "QR")
par130 = [gr_fit130.GetParameter(k) for k in range(gr_fit130.GetNpar())]
parE130 = [gr_fit130.GetParError(k) for k in range(gr_fit130.GetNpar())]
gr130.Draw("AP")
gr130.GetYaxis().SetRangeUser(0.0, 0.035)
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetLeftMargin(0.2)
ROOT.gPad.SetRightMargin(0.05)
c.Update()
print(par130)
print(parE130)

c.cd(3)
# gr140 = ROOT.TGraph(len(time), np.array(time), np.array(df140.amp))
gr140 = ROOT.TGraphErrors(len(time), np.array(time), np.array(df140.amp), np.array([0.0 for i in range(len(time))]), np.array(df140.ampE))
# gr140.SetMarkerStyle(28)
# gr140.SetMarkerSize(1.4)
gr140.SetMarkerStyle(20)
gr140.SetMarkerSize(1.0)
# gr140.SetMarkerColor(ROOT.kMagenta)
# gr140.SetLineColor(ROOT.kMagenta)
gr_fit140 = ROOT.TF1("f", "[0]*(1-exp(-x/[1]))", time[0], time[-1])
# gr_fit140.SetLineColor(ROOT.kMagenta)
# gr_fit140.SetLineStyle(10)
gr_fit140.SetTitle("140")
# gr_fit140.SetParameters(18.0, 5.) #for Integral
gr_fit140.SetParameters(0.02, 6.) #for Absolute polarization
gr140.Fit(gr_fit140, "QR")
par140 = [gr_fit140.GetParameter(k) for k in range(gr_fit140.GetNpar())]
parE140 = [gr_fit140.GetParError(k) for k in range(gr_fit140.GetNpar())]
gr140.Draw("AP")
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetLeftMargin(0.2)
ROOT.gPad.SetRightMargin(0.05)
c.Update()
print(par140)
print(parE140)

c.cd(4)
# gr150 = ROOT.TGraph(len(time), np.array(time), np.array(df150.amp))
gr150 = ROOT.TGraphErrors(len(time), np.array(time), np.array(df150.amp), np.array([0.0 for i in range(len(time))]), np.array(df150.ampE))
# gr150.SetMarkerStyle(39)
# gr150.SetMarkerSize(2.0)
gr150.SetMarkerStyle(20)
gr150.SetMarkerSize(1.0)
# gr150.SetMarkerColor(ROOT.kCyan)
# gr150.SetLineColor(ROOT.kCyan)
gr_fit150 = ROOT.TF1("f", "[0]*(1-exp(-x/[1]))", time[0], time[-1])
# gr_fit150.SetLineColor(ROOT.kCyan)
# gr_fit150.SetLineStyle(6)
gr_fit150.SetTitle("150")
# gr_fit150.SetParameters(15.0, 8.) #for Integral
gr_fit150.SetParameters(0.02, 6.) #for Absolute polarization
gr150.Fit(gr_fit150, "QR")
par150 = [gr_fit150.GetParameter(k) for k in range(gr_fit150.GetNpar())]
parE150 = [gr_fit150.GetParError(k) for k in range(gr_fit150.GetNpar())]
gr150.Draw("AP")
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetLeftMargin(0.2)
ROOT.gPad.SetRightMargin(0.05)
c.Update()
print(par150)
print(parE150)

#par = [gr_fit100.GetParameter(k) for k in range(gr_fit100.GetNpar())]
#print(par)
#gr.GetYaxis().SetRangeUser(0., 0.8)
# gr100.SetTitle("100 #circC")
# gr110.SetTitle("110 #circC")
gr120.SetTitle("120 #circC")
gr130.SetTitle("130 #circC")
gr140.SetTitle("140 #circC")
gr150.SetTitle("150 #circC")

# gr150.Draw("AP")
# gr140.Draw("P")
# gr130.Draw("P")
# gr120.Draw("P")
# gr110.Draw("P")
# gr100.Draw("P")

# gr100.GetXaxis().SetTitle("time [s]")
# gr110.GetYaxis().SetRangeUser(0.0, max(par110)*1.5)

# gr110.GetXaxis().SetTitle("time [s]")
# gr110.GetYaxis().SetTitle("amplitude [#muV]")

# gr120.GetXaxis().SetTitle("time [s]")
# gr120.GetYaxis().SetTitle("amplitude [#muV]")

# gr130.GetXaxis().SetTitle("time [s]")
# gr130.GetYaxis().SetTitle("amplitude [#muV]")

# gr140.GetXaxis().SetTitle("time [s]")
# gr140.GetYaxis().SetTitle("amplitude [#muV]")

# gr150.GetXaxis().SetTitle("time [s]")
# gr150.GetYaxis().SetTitle("amplitude [#muV]")

# gr100.GetXaxis().SetTitle("time [s]")
# gr100.GetYaxis().SetTitle("polarization %")

# gr110.GetXaxis().SetTitle("time [s]")
# gr110.GetYaxis().SetTitle("polarization %")

gr120.GetXaxis().SetTitle("time [s]")
gr120.GetYaxis().SetTitle("polarization %")

gr130.GetXaxis().SetTitle("time [s]")
gr130.GetYaxis().SetTitle("polarization %")

gr140.GetXaxis().SetTitle("time [s]")
gr140.GetYaxis().SetTitle("polarization %")

gr150.GetXaxis().SetTitle("time [s]")
gr150.GetYaxis().SetTitle("polarization %")

# gr100.GetXaxis().SetLabelSize(0.06)
# gr100.GetYaxis().SetLabelSize(0.06)
# gr100.GetXaxis().SetTitleSize(0.07)
# gr100.GetYaxis().SetTitleSize(0.07)
# gr100.GetXaxis().SetTitleOffset(0.85)
# gr100.GetYaxis().SetTitleOffset(1.1)

# gr110.GetXaxis().SetLabelSize(0.06)
# gr110.GetYaxis().SetLabelSize(0.06)
# gr110.GetXaxis().SetTitleSize(0.07)
# gr110.GetYaxis().SetTitleSize(0.07)
# gr110.GetXaxis().SetTitleOffset(0.85)
# gr110.GetYaxis().SetTitleOffset(1.1)

gr120.GetXaxis().SetLabelSize(0.06)
gr120.GetYaxis().SetLabelSize(0.06)
gr120.GetXaxis().SetTitleSize(0.07)
gr120.GetYaxis().SetTitleSize(0.07)
gr120.GetXaxis().SetTitleOffset(0.85)
gr120.GetYaxis().SetTitleOffset(1.1)

gr130.GetXaxis().SetLabelSize(0.06)
gr130.GetYaxis().SetLabelSize(0.06)
gr130.GetXaxis().SetTitleSize(0.07)
gr130.GetYaxis().SetTitleSize(0.07)
gr130.GetXaxis().SetTitleOffset(0.85)
gr130.GetYaxis().SetTitleOffset(1.1)

gr140.GetXaxis().SetLabelSize(0.06)
gr140.GetYaxis().SetLabelSize(0.06)
gr140.GetXaxis().SetTitleSize(0.07)
gr140.GetYaxis().SetTitleSize(0.07)
gr140.GetXaxis().SetTitleOffset(0.85)
gr140.GetYaxis().SetTitleOffset(1.1)

gr150.GetXaxis().SetLabelSize(0.06)
gr150.GetYaxis().SetLabelSize(0.06)
gr150.GetXaxis().SetTitleSize(0.07)
gr150.GetYaxis().SetTitleSize(0.07)
gr150.GetXaxis().SetTitleOffset(0.85)
gr150.GetYaxis().SetTitleOffset(1.1)

# ROOT.gPad.SetTopMargin(0.05)
# ROOT.gPad.SetBottomMargin(0.15)
# ROOT.gPad.SetLeftMargin(0.2)
# ROOT.gPad.SetRightMargin(0.05)

# legend.AddEntry(gr_fit150, "150 #circ C", "lep")
# legend.AddEntry(gr_fit140, "140 #circ C", "lep")
# legend.AddEntry(gr_fit130, "130 #circ C", "lep")
# legend.AddEntry(gr_fit120, "120 #circ C", "lep")
# legend.AddEntry(gr_fit110, "110 #circ C", "lep")
# legend.AddEntry(gr_fit100, "100 #circ C", "lep")
# legend.Draw()
# gr.SetMarkerStyle(7)
# gr.SetMarkerSize(10)
# gr.SetTitle("150")
# ROOT.gStyle.SetOptFit(1)
# c1 = ROOT.gROOT.FindObject("c1")
c.Draw("same")