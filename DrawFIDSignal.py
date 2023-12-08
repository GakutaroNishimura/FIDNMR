import numpy as np
import matplotlib.pyplot as plt
import ROOT

x = np.linspace(0.0, 1.0, 10000)
y = []

def func(x):
    return np.exp(-x/0.3)*np.sin(500*x)

for ix in x:
    y.append(func(x))

gr = ROOT.TGraph(len(x), np.array(x), np.array(y))
#gr.SetNpx(10000)
gr.SetTitle("")
# gr.GetXaxis().SetTitle("time [a.u.]")
# gr.GetYaxis().SetTitle("amplitude [a.u.]")
# gr.GetXaxis().SetLabelSize(0.05)
# gr.GetYaxis().SetLabelSize(0.05)
gr.GetXaxis().SetTitleSize(0.07)
gr.GetYaxis().SetTitleSize(0.07)
gr.GetXaxis().SetTitleOffset(0.85)
gr.GetYaxis().SetTitleOffset(0.6)
gr.Draw("AC")
c1 = ROOT.gROOT.FindObject("c1")
ROOT.gPad.SetTopMargin(0.1)
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetLeftMargin(0.1)
ROOT.gPad.SetRightMargin(0.05)
c1.Draw("same")