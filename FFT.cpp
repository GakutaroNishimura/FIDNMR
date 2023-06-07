#include <iostream>
#include <TFile.h>
#include <TTree.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <TF1.h>

void PerformFourierTransform(const TH1F* input, TH1F* output) {
    // ヒストグラムのバイナル数とビン幅を取得
    int numBins = input->GetNbinsX();
    double binWidth = input->GetBinWidth(1);

    // FFTを実行する
    input->FFT(output, "MAG");

    // 周波数軸を設定する
    for (int i = 1; i <= numBins / 2; ++i) {
        double frequency = i / (binWidth * numBins);
        output->SetBinContent(i, output->GetBinContent(i) / (numBins / 2));
        output->SetBinError(i, output->GetBinError(i) / (numBins / 2));
        output->SetBinLabel(i, Form("%.2f", frequency));
    }
}

int main() {
    // ROOTファイルを開く
    TFile* file = new TFile("input.root", "READ");

    // ツリーとデータブランチを取得する
    TTree* tree = (TTree)file->Get("tree_name");
    float data;
    TBranch branch = tree->GetBranch("branch_name");
    branch->SetAddress(&data);

    // ヒストグラムを作成する
    int numBins = 1000;
    TH1F* hist = new TH1F("histogram", "Data Distribution", numBins, 0, numBins);
    hist->GetXaxis()->SetTitle("Time");
    hist->GetYaxis()->SetTitle("Amplitude");

    // ツリーからデータを読み込んでヒストグラムに詰める
    int numEntries = tree->GetEntries();
    for (int i = 0; i < numEntries; ++i) {
        tree->GetEntry(i);
        hist->Fill(data);
    }

    // フーリエ変換の結果を格納するヒストグラムを作成する
    TH1F* fftHist = new TH1F("fftHistogram", "Fourier Transform", numBins / 2, 0, numBins / 2);
    fftHist->GetXaxis()->SetTitle("Frequency");
    fftHist->GetYaxis()->SetTitle("Amplitude");

    // フーリエ変換を実行する
    PerformFourierTransform(hist, fftHist);

    // 結果を表示する
    TCanvas* canvas = new TCanvas("canvas", "Canvas", 800, 600);
    canvas->Divide(2, 1);
    canvas->cd(1);
    hist->Draw();
    canvas->cd(2);
    fftHist->Draw();

    // ファイルを保存する
    canvas->Print("output.pdf");

    // メモリの解放
    delete canvas;
    delete hist;
    delete fftHist;
    delete file;

    return 0;
}