"""
15 February 2022
Created by Uttiya Sarkar, updated by Abraham Tishelman-Charny

The purpose of this module is to plot L1 rates for different seeds in order to evaluate the effect of different ECAL L1 configurations on L1 rates.

Example usage:

cmsenv 
python3 Plot_Rates.py --ol /eos/user/a/atishelm/www/EcalL1Optimization/L1_Quantities/rates/ --error --includeAll --inDir /afs/cern.ch/work/a/atishelm/private/CMS-ECAL-Trigger-Group/L1Rates/CMSSW_12_3_0_pre1/src/L1MenuTools/rate-estimation/results/ --seedsPerPage 30

"""

# imports 
from Plot_Rates_Tools import GetArgs, Add_CMS_Header, GetSeeds, MakePlot
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np 
import math 
import distutils

args, arg_names = GetArgs()
for arg in arg_names: exec("{arg} = args.{arg}".format(arg=arg))

# Get csv files with rate information 
print("inDir:",inDir)

files = [
    "{inDir}/Run_324725_Run2_NosimECALTP.csv".format(inDir=inDir),
    "{inDir}/Run_324725_Run2_NosimECALTP_Unpacked.csv".format(inDir=inDir),
    "{inDir}/Run_324725_Run2_simECALTP.csv".format(inDir=inDir),
    "{inDir}/Run_324725_StripZeroing_simECALTP.csv".format(inDir=inDir)
]   

fileNames = [f.split('/')[-1].split('.')[0] for f in files]

fileLabelDict = {
    "Run_324725_Run2_NosimECALTP" : "NoECALSim Emu",
    "Run_324725_Run2_NosimECALTP_Unpacked" : "NoECALSim Unpacked",
    "Run_324725_Run2_simECALTP" : "ECALSim Run2Mode",
    "Run_324725_StripZeroing_simECALTP" : "ECALSim StripZeroing"
}

fileLabels = [fileLabelDict[label] for label in fileNames]

seeds = GetSeeds()

x_indicies = [] 
seeds_used = []

for file_i in range(0, len(files)):
    exec("rates%s = []"%(file_i))
    exec("yerr%s = []"%(file_i))
    if(file_i == 1): # data unpacked, don't compute ratio
        continue 
    else:
        exec("ratios_to_data%s = []"%(file_i))  
        exec("ratios_to_data%s_errs = []"%(file_i))  

for seed in seeds:

    for file_i in range(0, len(files)):
        exec("f%s = files[file_i]"%(file_i))
        exec("df%s = pd.read_csv(f%s)"%(file_i, file_i))  
        exec("df%s.set_index('L1SeedName', inplace=True)"%(file_i))  
        exec("df%s = df%s.loc[seed]"%(file_i, file_i))
        exec("rate%s = df%s.iloc[2]"%(file_i, file_i))
        exec("rate%s_err = df%s.iloc[3]"%(file_i, file_i))

        # if(seed == "Total rate"):
        #     exec("rate%s *= 1000 "%(file_i))
        #     exec("rate%s_err *= 1000 "%(file_i))

    # if(rate0 != 0 and rate1 != 0 and rate2 != 0):
    if(rate0 != 0 and rate1 != 0 and rate2 != 0 and rate3 != 0):
        seeds_used.append(seed)

        for file_i in range(0, len(files)):
            exec("rates%s.append(rate%s)"%(file_i, file_i))
            exec("yerr%s.append(rate%s_err)"%(file_i, file_i))
            if(file_i == 1): # data unpacked, don't compute ratio
                continue 
            else:
                exec("ratio_%s = float(rate%s) / float(rate1)"%(file_i, file_i))
                exec("ratios_to_data%s.append(ratio_%s)"%(file_i, file_i)) # assumes rate 1 is the unpacked data 
                exec("rel_err_%s = math.sqrt( (rate%s_err / rate%s)**2 + (rate1_err / rate1)**2 )"%(file_i, file_i, file_i)) # Poissonion error (no MC weights)
                exec("abs_err_%s = rel_err_%s * ratio_%s"%(file_i, file_i, file_i))
                exec("ratios_to_data%s_errs.append(abs_err_%s)"%(file_i, file_i))

x_indicies = [i for i in range(0,len(rates1))]

for file_i in range(0, len(files)):
    exec("df_out_%s = pd.DataFrame({'rate' : rates%s})"%(file_i, file_i))

# Make a plot for every 10 rates 
print("Number of non-zero rates:",len(seeds_used))

N_plots = math.ceil(float(len(seeds_used)) / float(seedsPerPage))
print("Number of plots to make:",N_plots)
i_min, i_max = 0, seedsPerPage
N_files = len(files)

for plot_i in range(0, N_plots):
    print("Making plot",plot_i)
    lists_to_pass = ["x_indicies", "seeds_used", 
                     "df_out_0", "df_out_1", "df_out_2", "df_out_3",
                     "yerr0", "yerr1", "yerr2", "yerr3",  
                     "ratios_to_data0", "ratios_to_data2", "ratios_to_data3",
                     "ratios_to_data0_errs", "ratios_to_data2_errs", "ratios_to_data3_errs"
                     ]

    for item in lists_to_pass:
        if("df_out" in item):
            exec("%s_ = np.copy(%s['rate'][i_min:i_max])"%(item, item))
        else:
            exec("%s_ = np.copy(%s[i_min:i_max])"%(item, item))

    MakePlot(
        plot_i, N_files, fileLabels, seedsPerPage, ol, x_indicies_, seeds_used_, 
        df_out_0_, df_out_1_, df_out_2_, df_out_3_, 
        yerr0_, yerr1_, yerr2_, yerr3_, 
        ratios_to_data0_, ratios_to_data2_, ratios_to_data3_,
        ratios_to_data0_errs_, ratios_to_data2_errs_, ratios_to_data3_errs_
    )

    i_min += seedsPerPage
    i_max += seedsPerPage