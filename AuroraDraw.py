import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ROOT

DirPath = "./Data/2023/0728/test01/"
DataPath = DirPath + "10/ftdata2.csv"

df = pd.read_csv(DataPath, names=["freq", "amplitude"])

gr = ROOT.TGraph(len(df.freq), np.array(df.freq), np.array(df.amplitude))
gr.Draw("APL")
gr.SetMarkerStyle(7)
gr.SetMarkerSize(10)
c1 = ROOT.gROOT.FindObject("c1")
c1.Draw("same")

