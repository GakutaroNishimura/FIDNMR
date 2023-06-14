#======================================================================
#  Calculation of neutron spin rotation
#  ver.1.0:     2019            T.Okudaira  (AFPNMR_FS/NMRRelax.py)
#  ver.2.0:     2022            S.Takahashi (AFPNMRGUI/NMRRelax_forGUI.py)
#  ver.3.0:     2022            S.Takahashi (AFPNMRGUI_ver3/NMRRelax_forGUI.py)
#  ver.4.0:     2023/03/28      S.Takada    (AFPNMR/AFPNMR.py)
#======================================================================

import sys
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import sys
import subprocess
import SpinFlip
import Lockin
import DrawGraph
import time
import pathlib
import shutil
import Config as conf
import FileInfo


def CopyDataToGoogleDrive():
    # Make directory
    os.makedirs(conf.GoogleDrivePath, exist_ok=True)
    
    # Copy to Google Drive
    rsync_cmd = ["rsync", "-au", "--no-links", conf.DataPath, conf.GoogleDrivePath]
    subprocess.run(rsync_cmd, check=True)
    
    # Get file list
    CopyFileList = FileInfo.GetAndSortBinFileList()
    
    # Copy timestamp of file birthtime
    for Filename in CopyFileList:
        # Get file stats
        src_stats = os.stat(conf.DataPath + Filename)
        src_birthtimestamp = src_stats.st_birthtime
        src_datetime = datetime.datetime.fromtimestamp(src_birthtimestamp)
    
        # Copy file and set creation time
        os.utime(conf.GoogleDrivePath + Filename, (src_datetime.timestamp(), src_datetime.timestamp()))
    
def main():
    print("==== Program for FIDNMR start ====")
    print(conf.const.StartTime)
    
    # Make directory
    os.makedirs(conf.DataPath, exist_ok=True)

    # start File number
    #BinaryFileName = ["", ""]
    BinaryFileName = [""]
    StartNo = FileInfo.GetMaxFileNumber() + 1
    StopNo  = conf.NumOfDataAcquisition
    nLoop   = 1
    # Over Write mode
    if conf.OptOverWrite:
        StartNo = 1
        try:
            os.remove(conf.FileNamePeakValue)
            os.remove(conf.FileNamePeakValuePDF)
        except:
            "CSV Files are nothing."

    # Only Rockin mode
    if conf.OptOnlyLockin:
        conf.TimeInterval = 0
        StartNo = 0
        try:
            os.remove(conf.FileNamePeakValue)
            os.remove(conf.FileNameLog)
            os.remove(conf.FileNameParameter)
            os.remove(conf.FileNamePeakValuePDF)
        except:
            "CSV Files are nothing."
        
    # File list check
    BinaryFileList = FileInfo.GetAndSortBinFileList()
    if not conf.OptOnlyLockin:
        if not conf.OptOverWrite:
            if not FileInfo.isEven(len(BinaryFileList)):
                if not conf.OptOnlySpinFlip:
                    print("!!!! Caution !!!!")
                    print("The number of data files is odd.")
                    print("If you want to do spin flip, please run SpinFlip.py")
                    sys.exit()

    print(BinaryFileList)
    
    # Loop start
    for iLoop in range(StartNo, StopNo):
        print("Loop {0} start ----------------".format(nLoop))
        # File name
        if conf.OptOnlyLockin:
            BinaryFileName[0] = conf.DataPath + BinaryFileList[iLoop]
            #BinaryFileName[1] = conf.DataPath + BinaryFileList[iLoop+1]
        else:
            BinaryFileName[0] = conf.DataPath + str(iLoop).zfill(4)   + ".bin"
            #BinaryFileName[1] = conf.DataPath + str(iLoop+1).zfill(4) + ".bin"
            """
            NowTime = datetime.datetime.now()
            dt_string = NowTime.strftime("%Y%m%d_%H%M")            
            BinaryFileName[0] = conf.DataPath + dt_string + "_1.bin"
            BinaryFileName[1] = conf.DataPath + dt_string + "_2.bin"
            """
        
        # Spin Flip
        if not conf.OptOnlyLockin:
            # Execute spin flipping
            print("RF apply {0}".format(BinaryFileName[0]))
            SpinFlip.main(BinaryFileName[0])
            # Wait (1 sec)
            #time.sleep(1)
                
        if conf.OptOnlySpinFlip:
            # Wait (sec)
            time.sleep(conf.TimeInterval)
            # if only spin filp, move to the next loop
            continue
        
        """
        # Lockin
        print("---> Lockin start")
        Lockin.main(BinaryFileName[0], BinaryFileName[1])
        """

        # fft
        print("---> fft start")
        V, Time = Lockin.Lockin(BinaryFileName[0])
        Ndata, frequency_spectrum, frequencies = Lockin.fft(BinaryFileName[0], V, Time)
        
        if iLoop == StartNo:
            freq_spectrum_mean = np.array([0.0 for i in range(Ndata)])
        freq_spectrum_mean += np.abs(frequency_spectrum)

        if iLoop == StopNo-1:
            freq_spectrum_mean = freq_spectrum_mean/(StopNo-1)
            plt.plot(frequencies, freq_spectrum_mean, ".")
            plt.xlim(16000, 22000)
            plt.ylim(0, 12)
            plt.savefig(conf.DataPath + "fft.pdf")
            


        """
        # DrawGraph
        print("---> DrawGraph start")
        DrawGraph.main()
        """
        print(conf.OptCopyToGoogleDrive)
        
        # Data copy to Google Drive
        if conf.OptCopyToGoogleDrive:
            print("---> Copy to Google Drive")
            CopyDataToGoogleDrive()
            
        # Wait (sec)
        print("Complete this loop. Waitting {0} sec".format(conf.TimeInterval))
        nLoop = nLoop + 1
        time.sleep(conf.TimeInterval)

        
if __name__ == "__main__":
    main()
