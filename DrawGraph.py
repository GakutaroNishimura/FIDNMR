#======================================================================
#  Calculation of neutron spin rotation
#  ver.1.0:     2019            T.Okudaira  (AFPNMR_FS/DrawGraph_1226.py)
#  ver.2.0:     2022            S.Takahashi (AFPNMRGUI/DrawGraph_1226_forGUI.py)
#  ver.3.0:     2022            S.Takahashi (AFPNMRGUI_ver3/DrawGraph_1226_forGUI.py)
#  ver.4.0:     2023/03/28      S.Takada    (AFPNMR/DrawGraph.py)
#======================================================================

import ROOT
from array import array
from datetime import datetime as dt
import pandas as pd
import Config as conf

def GraphDesign():
    ROOT.gStyle.SetTitleSize(0.05, "X")
    ROOT.gStyle.SetTitleSize(0.05, "Y")
    ROOT.gStyle.SetLabelSize(0.045, "X")
    ROOT.gStyle.SetLabelSize(0.045, "Y")
    ROOT.gStyle.SetTitleXOffset(0.8)
    ROOT.gStyle.SetTitleYOffset(0.8)
    ROOT.gStyle.SetLabelFont(132, "X")
    ROOT.gStyle.SetLabelFont(132, "Y")
    ROOT.gStyle.SetTitleFont(132, "Y")
    ROOT.gStyle.SetTitleFont(132, "X")
    ROOT.gStyle.SetTitleFont(132, "")
    #    ROOT.gStyle.SetTitleOffset(0.1, "X")
    #    ROOT.gStyle.SetTitleOffset(0.1, "Y")

def MakeGraph(df, XAxisName, YAxisName, XErrorName, YErrorName):
    #    print(df)
    # Data
    XArray = array("d", df[XAxisName])
    XErrorArray = array("d", df[XErrorName])
    YArray = array("d", df[YAxisName])
    YErrorArray = array("d", df[YErrorName])
    
    # Graph
    graph = ROOT.TGraphErrors(len(df), XArray, YArray, XErrorArray, YErrorArray)
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(0.5)    
    graph.SetLineWidth(1)
    
    return graph

def FitPeakValue(gPeakValue):
    # Function
    Function = ""
    if conf.OptBuildRelax=="B":
        Function = conf.FunctionBuild
    elif conf.OptBuildRelax=="R":
        Function = conf.FunctionRelaxation
    
    fPeakValue = ROOT.TF1("f", Function, 0, gPeakValue.GetN()*2)

    # set parameter
    for iPara in range(2):
        if conf.OptBuildRelax=="B":
            fPeakValue.SetParameter(iPara, conf.InitialValueBuild[iPara])
            #            fPeakValue.SetParLimits(iPara, conf.ParameterLimitBuild[iPara][0], conf.ParameterLimitBuild[iPara][1])
        elif conf.OptBuildRelax=="R":
            fPeakValue.SetParameter(iPara, conf.InitialValueRelax[iPara])
            #            fPeakValue.SetParLimits(iPara, conf.ParameterLimitRelax[iPara][0], conf.ParameterLimitRelax[iPara][1])
            #            print(conf.InitialValueRelax, conf.ParameterLimitRelax)
    # Fit
    for iFit in range(0, 10):
        gPeakValue.Fit("f", "", "", 0, gPeakValue.GetN()*2)
        print(gPeakValue.GetN()*2)
        
    return fPeakValue


def main():
    # Read datafile
    df = pd.read_csv(conf.FileNamePeakValue,
                     names=("Time", "Elapsed", "PeakValue", "PeakValueError"), header=0)
    df["Elapsed"] = df["Elapsed"]/60.    # [min] -> [hour]    
    df["Time"]    = pd.to_datetime(df["Time"])
    df["Time"]    = df["Time"].dt.strftime("%Y/%m/%d %H:%M")    
    df["XError"] = [0 for ip in range(len(df))]
    
    # Canavs
    c = ROOT.TCanvas("c", "c", 800, 400)
    GraphDesign()
    
    # Draw graph
    gPeakValue = MakeGraph(df, "Elapsed", "PeakValue", "XError", "PeakValueError")
    gPeakValue.SetMarkerStyle(31)
    gPeakValue.SetMarkerStyle(7)
    gPeakValue.SetMarkerSize(1)
    gPeakValue.SetMarkerColor(2)
    gPeakValue.SetLineColor(2)
    # gPeakValue.SetTitle("NMR Signal")
    gPeakValue.GetXaxis().SetTitle("Time [hour]")
    gPeakValue.GetYaxis().SetTitle("NMR Signal [mV]")
    #gPeakValue.GetXaxis().SetTitle("Number of Flip")
    #    gPeakValue.GetYaxis().SetRangeUser(0, 0.6)
    gPeakValue.GetYaxis().SetRangeUser(0, 0.1)
    gPeakValue.Draw("AP")
    
    # Fitting
    fPeakValue = FitPeakValue(gPeakValue)
    
    # Draw time
    CurrentTime = df["Time"].tail(1).to_string(index=False)
    ttime = ROOT.TText(0.14, 0.33, "Last Measurement : %s" % CurrentTime)
    ttime.SetNDC(1)
    ttime.SetTextSize(0.04)
    ttime.SetTextFont(22)
    ttime.Draw("")
    
    # Draw Relaxation or Buildup time
    TimeText = ""
    if conf.OptBuildRelax=="B":
        if fPeakValue.GetParameter(1) == float("nan"):
            TimeText = "Buildup Time : nan [hour]"
        else:
            TimeText = "Buildup Time : {0} +/- {1} [hour]".format(round(fPeakValue.GetParameter(1),3), round(fPeakValue.GetParError(1),3))

    else:
        if fPeakValue.GetParameter(1) == float("nan"):
            TimeText = "Relaxation Time : nan [hour]"
        else:
            TimeText = "Relaxation Time : {0} +/- {1} [hour]".format(round(fPeakValue.GetParameter(1),3), round(fPeakValue.GetParError(1),3))
    tpoint = ROOT.TText(0.14, 0.25, TimeText)
    tpoint.SetNDC(1)
    tpoint.SetTextSize(0.05)
    tpoint.SetTextFont(22)
    tpoint.Draw("")

    # Canvas update
    c.SetGrid()
    c.Update()

    # Save PDF
    c.SaveAs(conf.FileNamePeakValuePDF)

if __name__ == "__main__":
    main()
