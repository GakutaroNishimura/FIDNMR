import ROOT
import numpy as np

p_129 = np.array([50.0*0.264 , 1.0, 3.0*760*0.264])
p_Xe = np.array([50.0, 26.0, 3.0*760])
p_tot = np.array([305.0, 236.0, 3.0*760])
T_2 = np.array([15.0, 21.0, 0.1892])

gr = ROOT.TGraph(len(p_Xe), p_Xe, T_2)
#gr = ROOT.TGraph(len(p_Xe), p_tot, T_2)

#gr_fit = ROOT.TF1("f", "[0]/x + [1]", 1.0, 610.0)
gr_fit = ROOT.TF1("f", "[0]/x + [1]", 27.0, 2400) #p_Xe
gr_fit.SetParameters(549.0, 0.0)
#gr_fit = ROOT.TF1("f", "[0]/x + [1]", 230.0, 2300.0) #p_tot
#gr_fit.SetParameters(5000.0, 0.0)

gr_fit.SetNpx(10000)
gr.Fit(gr_fit, "QR")
gr.Draw("AP")
gr.GetXaxis().SetTitle("Xe partial pressure [torr]")
#gr.GetXaxis().SetTitle("cell total pressure [torr]")
gr.GetYaxis().SetTitle("T2 [s]")
gr.SetMarkerStyle(8)
gr.SetMarkerSize(1)
ROOT.gStyle.SetOptFit(1)
c1 = ROOT.gROOT.FindObject("c1")
c1.Draw("same")