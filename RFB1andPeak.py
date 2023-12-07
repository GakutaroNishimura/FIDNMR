import pandas as pd
import numpy as np
import ROOT

#df = pd.read_table("./PeakRFVoltage.txt", names=["voltage", "integral", "par0", "par1", "par2"], sep=" ")

voltage = [1.0, 3.0, 2.0, 0.8, 0.5, 1.2]
peak = [41.2412, 14.0849, 11.3675, 40.4567, 11.6887, 40.4863]

#gr = ROOT.TGraph(len(df.voltage), np.array(df.voltage), np.array(df.integral))
gr = ROOT.TGraph(len(voltage), np.array(voltage), np.array(peak))
#gr_fit = ROOT.TF1("f", "abs([1]*sin([0]*x + [2]))", 0.5, 3.0)
#gr_fit.SetParameters(842.0, 2.3, 800.0, -1.5)
#gr_fit.SetParameters(25.0, 2.3, 15.0, -1.5)
#gr_fit.SetParameters(2.3, 15.0, -1.5)
#gr.Fit(gr_fit, "QR")
gr.SetTitle("")
gr.GetXaxis().SetTitle("transmit level [V]")
gr.GetYaxis().SetTitle("peak height [a.u.]")
gr.GetXaxis().SetLabelSize(0.06)
gr.GetYaxis().SetLabelSize(0.06)
gr.GetXaxis().SetTitleSize(0.07)
gr.GetYaxis().SetTitleSize(0.07)
gr.GetXaxis().SetTitleOffset(0.85)
gr.GetYaxis().SetTitleOffset(0.7)
gr.Draw("AP")
#gr.GetYaxis().SetRangeUser(-100.0, 2000.0)
gr.GetYaxis().SetRangeUser(-2.0, 50.0)
gr.SetMarkerStyle(7)
gr.SetMarkerSize(10)
ROOT.gStyle.SetOptFit(1)
ROOT.gPad.SetTopMargin(0.1)
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetLeftMargin(0.1)
ROOT.gPad.SetRightMargin(0.05)
c1 = ROOT.gROOT.FindObject("c1")
c1.Draw("same")