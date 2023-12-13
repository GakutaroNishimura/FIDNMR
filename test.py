import ROOT

# データの作成
# ここでは単純な例として、ランダムなデータを生成しています。
# 実際のデータに合わせて、適切なデータを読み込んでください。
data = [1.5, 1.6, 1.7, 1.8, 1.9, 5.2, 5.5, 6.0, 6.5, 6.8]

# ヒストグラムの作成
hist = ROOT.TH1F("hist", "Data Histogram", 10, 0, 10)

for value in data:
    hist.Fill(value)

# 各範囲に対してフィッティングを行う
fit_range_1 = (1, 2)
fit_range_2 = (5, 7)

# フィッティング関数の定義
# ここでは単純な例として、ガウス関数を使用しています。
# 実際のデータに合わせて適切な関数を選択してください。
fit_func = ROOT.TF1("fit_func", "gaus", 0, 10)

# 範囲1のフィッティング
hist.Fit("fit_func", "R", "", fit_range_1[0], fit_range_1[1])

# フィッティング結果の取得
fit_result_1 = hist.GetFunction("fit_func").Clone("fit_result_1")

# 範囲2のフィッティング
hist.Fit("fit_func", "R", "", fit_range_2[0], fit_range_2[1])

# フィッティング結果の取得
fit_result_2 = hist.GetFunction("fit_func").Clone("fit_result_2")

# フィッティング結果の組み合わせ
# ここでは、各範囲のフィッティング結果を足し合わせています。
# 適切な組み合わせ方法は、実際のデータや目的によります。
final_fit_result = fit_result_1 + fit_result_2

# キャンバスの作成と表示
canvas = ROOT.TCanvas("canvas", "Fit Result", 800, 600)
hist.Draw()
final_fit_result.Draw("same")
canvas.Update()
canvas.Draw()

# 結果を保存する場合
canvas.SaveAs("fit_result.png")

# プログラムの実行を続ける
ROOT.gApplication.Run()
