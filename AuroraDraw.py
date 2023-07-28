import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ROOT

DirPath = "./Data/2023/0719/test10/"
DataPath = "./Data/2023/0719/test10/30/ftdata2.csv"

df = pd.read_csv(DataPath, names=["freq", "amplitude"])

gr = ROOT.TGraph(len(df.freq), np.array(df.freq), np.array(df.amplitude))
gr.Draw("APL")
c1 = ROOT.gROOT.FindObject("c1")
c1.Draw("same")

