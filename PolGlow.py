import ROOT
import numpy as np


time = [2., 7., 12., 17., 27., 37., 57.]
#time = [7., 12., 17., 27., 37., 57.] #110
#amplitude = [0.437551, 0.473369, 0.633478, 0.722147, 0.694416, 0.591403, 0.658201] #100
#amplitude = [0.491034, 0.620165, 0.793393, 0.622123, 0.710504, 0.65927] #110
#amplitude = [0.43229, 0.689053, 1.01882, 0.947034, 0.990453, 0.868595, 0.84074] #120
#amplitude = [0.359947, 0.718809, 0.828886, 0.664256, 0.925595, 0.862325, 0.987762] #130
#amplitude = [0.505634, 0.848728, 0.724358, 0.945877, 1.00124, 1.07725, 0.972557] #140
amplitude = [0.722924, 1.12504, 1.24068, 1.31561, 1.37747, 1.18928, 1.2161] #150


gr = ROOT.TGraph(len(time), np.array(time), np.array(amplitude))
gr_fit = ROOT.TF1("f", "[2]+[0]*(1-exp(-x/[1]))", time[0], time[-1])
gr_fit.SetParameters(0.5, 8., 0.26)
gr.Fit(gr_fit, "QR")
par = [gr_fit.GetParameter(k) for k in range(gr_fit.GetNpar())]
print(par)
#gr.GetYaxis().SetRangeUser(0., 0.8)
gr.Draw("AP")
gr.SetMarkerStyle(7)
gr.SetMarkerSize(10)
gr.SetTitle("150")
ROOT.gStyle.SetOptFit(1)
c1 = ROOT.gROOT.FindObject("c1")
c1.Draw("same")