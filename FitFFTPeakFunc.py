import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ROOT
import sys
import Config as conf

argvs = sys.argv

DataPath = conf.DataPath + "ftdata2.csv"

voltage = 1.0
temp = 120

# DirPath = "./Data/2023/0728/test01/"
# DataPath = DirPath + "10/ftdata2.csv"

df = pd.read_csv(DataPath, names=["freq", "amplitude"])

#131Xe 100℃から150℃.
# f_0 = 18390.0
# f_dev = 50
# f_min = f_0-f_dev
# f_max = f_0+f_dev
# f_minBG = 18100.0
# f_maxBG = 19100.0

#131Xe 155℃のやつ.0728.
f_0 = 18400.0
f_dev = 70
f_min = f_0-f_dev
f_max = f_0+f_dev
f_minBG = 18100.0
f_maxBG = 19100.0

#129Xe 0721/test07
# f_0 = 18935.0 
# f_dev = 50
# f_min = f_0-f_dev
# f_max = f_0+f_dev
# f_minBG = f_0-400.0
# f_maxBG = f_0+400.0


def FitFunc(DirPath, df):
    c = ROOT.TCanvas("c", "title", 900, 600)
    #c2 = ROOT.TCanvas("c", "title", 900, 600)
    c.Divide(1,2)
    c.cd(1)

    #c.cd()
    freqBG = []
    ampBG = []
    j = 0
    for i in df.freq:
        if i > f_minBG and i < f_min:
            freqBG.append(i)
            iamp = df.amplitude[j]
            ampBG.append(iamp)
        if i > f_max and i < f_maxBG:
            freqBG.append(i)
            iamp = df.amplitude[j]
            ampBG.append(iamp)
        j += 1


    freq = []
    amp = []
    j = 0
    for i in df.freq:
        if i > f_minBG and i < f_maxBG:
            iamp = df.amplitude[j]
            amp.append(iamp)
        j += 1
    amp_max = max(amp)
    amp = []

    grBG = ROOT.TGraph(len(freqBG), np.array(freqBG), np.array(ampBG))
    grBGplot = ROOT.TGraph(len(df.freq), np.array(df.freq), np.array(df.amplitude))
    gr_fitBG = ROOT.TF1("f", "pol2", f_minBG, f_maxBG)
    gr_fitBG.SetParameters(-160.0, 0.015, -4.5e-7)
    gr_fitBG.SetNpx(10000)
    grBG.Fit(gr_fitBG, "QRS")
    parBG = [gr_fitBG.GetParameter(k) for k in range(gr_fitBG.GetNpar())]
    print(parBG)
    grBG.SetMarkerStyle(7)
    grBG.SetMarkerSize(10)
    grBGplot.SetMarkerStyle(7)
    grBGplot.SetMarkerSize(10)
    grBG.SetTitle("fitting back ground")
    grBG.GetXaxis().SetTitle("frequency [Hz]")
    grBG.GetYaxis().SetTitle("amplitude [#muV/Hz]")
    grBG.GetXaxis().SetLabelSize(0.06)
    grBG.GetYaxis().SetLabelSize(0.06)
    grBG.GetXaxis().SetTitleSize(0.07)
    grBG.GetYaxis().SetTitleSize(0.07)
    grBG.GetXaxis().SetTitleOffset(0.85)
    grBG.GetYaxis().SetTitleOffset(0.6)

    grBG.Draw("AP")
    grBGplot.Draw("PL")
    grBG.GetXaxis().SetRangeUser(f_minBG, f_maxBG)
    grBG.GetYaxis().SetRangeUser(0.0, amp_max*1.5)
    ROOT.gPad.SetTopMargin(0.1)
    ROOT.gPad.SetBottomMargin(0.15)
    ROOT.gPad.SetLeftMargin(0.1)
    ROOT.gPad.SetRightMargin(0.05)
    c.Update()


    c.cd(2)

    freq = []
    amp = []
    j = 0
    for i in df.freq:
        if i > f_minBG and i < f_maxBG:
            freq.append(i)
            iamp = df.amplitude[j] - (parBG[0] + parBG[1]*i + parBG[2]*i**2)
            if iamp < 0:
                amp.append(0.0)
            else:
                amp.append(iamp)
        j += 1
            

    #gr = ROOT.TGraph(len(df.freq), np.array(df.freq), np.array(df.amplitude))
    gr = ROOT.TGraph(len(freq), np.array(freq), np.array(amp))
    # gr_fit = ROOT.TF1("f", "[2]*[0]/(pow((x-[1]), 2) + [0]*[0]) + [3]", f_min, f_max)
    #gr_BGfit = ROOT.TF1("f", "pol2", f_min, f_max)
    # gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-18397.0), 2) + [0]*[0])", f_min, f_max)
    # gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-18391.0), 2) + [0]*[0])", f_min, f_max)
    # gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-18383.0), 2) + [0]*[0])", f_min, f_max)
    # gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-18384.0), 2) + [0]*[0])", f_min, f_max) #0727/test32-38
    # gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-18385.0), 2) + [0]*[0])", f_min, f_max) #0727/test11-18
    # gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-18388.0), 2) + [0]*[0])", f_min, f_max) #0727/test25-31
    # gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-18390.0), 2) + [0]*[0])", f_min, f_max) #0727/test19-24
    # gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-18404.0), 2) + [0]*[0])", f_min, f_max)
    # gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-18935.0), 2) + [0]*[0])", f_min, f_max) #129Xe
    gr_fit = ROOT.TF1("f", "[1]*[0]/(pow((x-[2]), 2) + [0]*[0])", f_min, f_max)


    gr_fit.SetParameters(4.0, 12.8, 18391.)
    # gr_fit.SetParameters(4.0, 12.8) #131Xe
    # gr_fit.SetParameters(0.7426, 2.195)
    #gr_fit.SetParameters(4.0, 18404., 12.8, 0.14)
    #gr_fit.SetParameters(13.13, 18920., 500.0, 1.5)
    # gr_fit.SetParameters(15.0, 18920., 500.0)
    # gr_fit.SetParameters(15.0, 500.0) #129Xe

    # gr_BGfit.SetParameters(-160.0, 0.015, -4.5)

    gr_fit.SetNpx(10000)
    gr.Fit(gr_fit, "QR")
    par = [gr_fit.GetParameter(k) for k in range(gr_fit.GetNpar())]
    print(par)

    integral = gr_fit.Integral(f_min, f_max)
    fwhm = 2*par[0]
    T2 = 1/fwhm
    print("FWHM is %f" %fwhm)
    print("T2 is %f" %T2)
    print("function integral is %f" %integral)
    ROOT.gPad.SetTopMargin(0.1)
    ROOT.gPad.SetBottomMargin(0.15)
    ROOT.gPad.SetLeftMargin(0.1)
    ROOT.gPad.SetRightMargin(0.05)
    ROOT.gStyle.SetStatX(0.9)
    ROOT.gStyle.SetStatY(0.8)
    ROOT.gStyle.SetStatW(0.14)
    ROOT.gStyle.SetStatH(0.2)
    gr.SetTitle("fitting peak after BG subtraction")
    gr.GetXaxis().SetTitle("frequency [Hz]")
    gr.GetYaxis().SetTitle("amplitude [#muV/Hz]")
    gr.GetXaxis().SetLabelSize(0.06)
    gr.GetYaxis().SetLabelSize(0.06)
    gr.GetXaxis().SetTitleSize(0.07)
    gr.GetYaxis().SetTitleSize(0.07)
    gr.GetXaxis().SetTitleOffset(0.85)
    gr.GetYaxis().SetTitleOffset(0.6)

    gr.Draw("APL")
    # gr.GetXaxis().SetRangeUser(f_min, f_max)
    gr.GetYaxis().SetRangeUser(0.0, par[1]/par[0]*1.5)
    ROOT.gStyle.SetOptFit(1)
    gr.SetMarkerStyle(7)
    gr.SetMarkerSize(10)

    #c1 = ROOT.gROOT.FindObject("c1")
    c.Update()
    c.Draw("same")
    # c2.Draw("same")
    c.SaveAs(DirPath + "PeakFit.pdf")
    #c.Close()

    f=open(argvs[1],"a")
    # f.write("%f %f %f %f %f\n" %(voltage, integral, par[0], par[1], par[2]))
    f.write("%f %f\n" %(integral, T2))
    f.close()


def FitPeak(DirPath, df):
    freqBG = []
    ampBG = []
    j = 0
    for i in df.freq:
        if i > f_minBG and i < f_min:
            freqBG.append(i)
            iamp = df.amplitude[j]
            ampBG.append(iamp)
        if i > f_max and i < f_maxBG:
            freqBG.append(i)
            iamp = df.amplitude[j]
            ampBG.append(iamp)
        j += 1

    amp = []
    j = 0
    for i in df.freq:
        if i > f_minBG and i < f_maxBG:
            iamp = df.amplitude[j]
            amp.append(iamp)
        j += 1
    amp_max = max(amp)

    # c = ROOT.TCanvas("c", "title", 900, 600)
    # #c2 = ROOT.TCanvas("c", "title", 900, 600)
    # c.Divide(1,2)
    # c.cd(1)
    
    grBG = ROOT.TGraph(len(freqBG), np.array(freqBG), np.array(ampBG))
    grBGplot = ROOT.TGraph(len(df.freq), np.array(df.freq), np.array(df.amplitude))
    gr_fitBG = ROOT.TF1("f", "pol2", f_minBG, f_maxBG)
    gr_fitBG.SetParameters(-160.0, 0.015, -4.5e-7)
    gr_fitBG.SetNpx(10000)
    resultBG = grBG.Fit(gr_fitBG, "QRS")
    fit_resultBG = ROOT.TFitResult(resultBG.Get())
    cov_matrixBG = fit_resultBG.GetCovarianceMatrix()
    cov_matrix_arrayBG = cov_matrixBG.GetMatrixArray()
    parBG = [gr_fitBG.GetParameter(k) for k in range(gr_fitBG.GetNpar())]
    parBGE = [gr_fitBG.GetParError(k) for k in range(gr_fitBG.GetNpar())]
    # print(parBG)
    # print(parBGE)
    grBG.SetMarkerStyle(7)
    grBG.SetMarkerSize(10)
    grBGplot.SetMarkerStyle(7)
    grBGplot.SetMarkerSize(10)
    grBG.SetTitle("fitting back ground")
    grBG.GetXaxis().SetTitle("frequency [Hz]")
    grBG.GetYaxis().SetTitle("amplitude [#muV/Hz]")
    grBG.GetXaxis().SetLabelSize(0.06)
    grBG.GetYaxis().SetLabelSize(0.06)
    grBG.GetXaxis().SetTitleSize(0.07)
    grBG.GetYaxis().SetTitleSize(0.07)
    grBG.GetXaxis().SetTitleOffset(0.85)
    grBG.GetYaxis().SetTitleOffset(0.6)

    grBG.Draw("AP")
    grBGplot.Draw("PL")
    grBG.GetXaxis().SetRangeUser(f_minBG, f_maxBG)
    grBG.GetYaxis().SetRangeUser(0.0, amp_max*1.5)
    ROOT.gPad.SetTopMargin(0.1)
    ROOT.gPad.SetBottomMargin(0.15)
    ROOT.gPad.SetLeftMargin(0.1)
    ROOT.gPad.SetRightMargin(0.05)
    # c.Update()

    # c.cd(2)
    gr = ROOT.TGraph(len(df.freq), np.array(df.freq), np.array(df.amplitude))
    # gr = ROOT.TGraph(len(freqBG), np.array(freqBG), np.array(ampBG))
    grFit = ROOT.TF1("f", "[1]*[0]/(pow((x-[2]), 2) + [0]*[0]) + [3] + [4]*x + [5]*pow(x,2)", f_minBG, f_maxBG)
    # grFit.SetParameters(5.300703134755664, 5.808296699448432, 18391., -95.8629532294724, 0.010326628640125438, -2.7777627288466405e-07)
    # grFit.SetParameters(5.300703134755664, 5.808296699448432, 18382., parBG[0], parBG[1], parBG[2])
    grFit.SetParameters(3.0, 2.050427771930654, 18391., parBG[0], parBG[1], parBG[2]) # for 0726 41-47
    # grFit.SetParameters(15.0, 10.0, 18397., parBG[0], parBG[1], parBG[2]) # for 0728 155ド./
    # grFit.FixParameter(2, 18391.) # for 0727/test01-07
    # grFit.FixParameter(2, 18385.) # for #0727/test11-18
    # grFit.FixParameter(2, 18390.) #0727/test19-24
    # grFit.FixParameter(2, 18388.) #0727/test25-31
    # grFit.FixParameter(2, 18384.) #0727/test32-38
    # grFit.FixParameter(2, 18397.) # for 155ド131Xe 0728
    # grFit.FixParameter(2, 18935.) #129Xe
    grFit.FixParameter(3, parBG[0])
    grFit.FixParameter(4, parBG[1])
    grFit.FixParameter(5, parBG[2])
    # gr.Fit(grFit, "QR")
    grFit.SetNpx(10000)
    result = gr.Fit(grFit, "QRS")
    fit_result = ROOT.TFitResult(result.Get())
    cov_matrix = fit_result.GetCovarianceMatrix()
    cov_matrix_array = cov_matrix.GetMatrixArray()
    # print(cov_matrix)
    par = [grFit.GetParameter(k) for k in range(grFit.GetNpar())]
    parE = [grFit.GetParError(k) for k in range(grFit.GetNpar())]
    fwhm = 2*par[0]
    fwhmE = 2*parE[0]
    T2 = 1/fwhm
    T2E = fwhmE/fwhm**2
    # parE = [grFit.GetParError(k) for k in range(grFit.GetNpar())]
    # parE = grFit.GetCovarianceMatrix()
    
    # parE[3] = parE[3] + parBGE[0]
    # parE[4] = parE[4] + parBGE[1]
    # parE[5] = parE[5] + parBGE[2]
    # print(par)
    # print(parE)
    gr.Draw("APL")
    # grBG.Draw("")
    gr.GetXaxis().SetRangeUser(f_minBG, f_maxBG)
    ROOT.gPad.SetTopMargin(0.1)
    ROOT.gPad.SetBottomMargin(0.15)
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetRightMargin(0.05)
    ROOT.gStyle.SetOptFit(0000000000)
    # ROOT.gStyle.SetStatX(0.9)
    # ROOT.gStyle.SetStatY(0.8)
    # ROOT.gStyle.SetStatW(0.14)
    # ROOT.gStyle.SetStatH(0.2)
    # gr.SetTitle("fitting peak after BG subtraction")
    gr.SetTitle(" ")
    gr.GetXaxis().SetTitle("frequency [Hz]")
    gr.GetYaxis().SetTitle("amplitude [#muV/Hz]")
    gr.GetXaxis().SetLabelSize(0.06)
    gr.GetYaxis().SetLabelSize(0.06)
    gr.GetXaxis().SetTitleSize(0.07)
    gr.GetYaxis().SetTitleSize(0.07)
    gr.GetXaxis().SetTitleOffset(0.85)
    gr.GetYaxis().SetTitleOffset(0.8)
    gr.GetXaxis().SetRangeUser(18100.0, 18700.)
    gr.GetYaxis().SetRangeUser(0.0, amp_max*1.5)
    # gr.GetYaxis().SetRangeUser(0.0, par[1]/par[0]*1.5)
    ROOT.gStyle.SetOptFit(1)
    gr.SetMarkerStyle(7)
    gr.SetMarkerSize(10)
    c = ROOT.gROOT.FindObject("c1")
    c.Update()
    c.Draw("same")
    c.SaveAs(DirPath + "PeakFit.pdf")
    # c.SaveAs("PeakFit.pdf")
    # print(par[:2])
    # integral = grFit.IntegralError(f_min, f_max, np.array(par[:3]), np.array(parE[:3]))
    integral = gr_fitBG.Integral(f_min, f_max)
    integral1 = grFit.Integral(f_min, f_max)
    integralE = gr_fitBG.IntegralError(f_min, f_max, np.array(parBG), cov_matrix_arrayBG)
    integralE1 = grFit.IntegralError(f_min, f_max, np.array(par), cov_matrix_array)
    # integral = grFit.Integral(f_min, f_max)
    print(integral)
    print(integral1)
    print(integralE)
    print(integralE1)
    print(T2)
    print(T2E)
    peak = integral1 - integral
    peakE = np.sqrt(integralE**2 + integralE1**2)

    f=open(argvs[1],"a")
    # f.write("%f %f %f %f %f\n" %(voltage, integral, par[0], par[1], par[2]))
    f.write("%f %f %f\n" %(peak, peakE, T2))
    f.close()

if __name__ == "__main__":
    DirPath = "./" + conf.DataDirectryName
    # FitFunc(DirPath, df)
    FitPeak(DirPath, df)