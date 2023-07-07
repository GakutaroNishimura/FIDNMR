import ROOT
import numpy as np

# データ生成
np.random.seed(0)
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x) + np.random.normal(0, 0.2, 100)

# ROOTのグラフ描画用のデータ形式に変換
graph1 = ROOT.TGraph(len(x), x, y1)
graph2 = ROOT.TGraph(len(x), x, y2)

# グラフスタイルの設定
graph1.SetLineColor(ROOT.kBlue)
graph1.SetLineWidth(2)
graph2.SetLineColor(ROOT.kRed)
graph2.SetLineWidth(2)

# グラフ1の描画用キャンバス作成
canvas1 = ROOT.TCanvas("canvas1", "Graph 1", 800, 600)
graph1.Draw("AL")  # "AL"は線を描画する指定
canvas1.Draw()

# グラフ2の描画用キャンバス作成
canvas2 = ROOT.TCanvas("canvas2", "Graph 2", 800, 600)
graph2.Draw("AL")  # "AL"は線を描画する指定
canvas2.Draw()