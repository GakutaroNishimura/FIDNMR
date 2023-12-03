import numpy as np
import pandas as pd
import ROOT

DirPath = "./Data/2023/1102/test01/"
DataPath = DirPath + "10/ftdata2.csv"

# データの読み込み
df = pd.read_csv(DataPath, names=["freq", "amplitude"])

#Fbin = len(df["freq"])
Fmin = float(min(df["freq"]))
Fmax = float(max(df["freq"]))
Amin = float(min(df["amplitude"]))
Amax = float(min(df["amplitude"]))
#print(bin)
#print(min)
#print(max)
#print(df["freq"][1])

# ROOTキャンバスの作成
canvas = ROOT.TCanvas("canvas", "Frequency vs Amplitude", 800, 600)

# ROOTヒストグラムの作成
hist = ROOT.TH2F("hist", "Frequency vs Amplitude", 100, Fmin, Fmax, 1000, Amin, Amax)

# データをヒストグラムに追加
i = 0
for index, row in df.iterrows():
    #hist.Fill(float(row["amplitude"]))
    hist.Fill(float(row["freq"]), float(row["amplitude"]))

# ヒストグラムを描画
hist.Draw()

# キャンバスを表示
canvas.Update()
canvas.Draw()
