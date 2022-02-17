"""
15 February 2022
Created by Uttiya Sarkar, updated by Abraham Tishelman-Charny

The purpose of this module is to plot L1 rates for different seeds in order to evaluate the effect of different ECAL L1 configurations on L1 rates.

Example usage:

cmsenv 
python3 Plot_L1_Ratio.py --ol /eos/user/a/atishelm/www/EcalL1Optimization/L1_Quantities/rates/ --error --includeAll --inDir /afs/cern.ch/work/a/atishelm/private/CMS-ECAL-Trigger-Group/L1Rates/CMSSW_12_3_0_pre1/src/L1MenuTools/rate-estimation/results/ 

"""

# imports 
from Plot_L1_Ratio_Tools import GetArgs, Add_CMS_Header, GetSeeds
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np 
import math 

args, arg_names = GetArgs()
for arg in arg_names: exec("{arg} = args.{arg}".format(arg=arg))

# Get csv files with rate information 
print("inDir:",inDir)

files = [
    "{inDir}/Run_320038_NoECALsim_NotUnpacked.csv".format(inDir=inDir),
    "{inDir}/Run_320038_NoECALsim_Unpacked.csv".format(inDir=inDir),
    "{inDir}/Run_320038_Run2Mode_WithECALSim.csv".format(inDir=inDir),
    "{inDir}/Run_320038_StripZeroingMode_WithECALSim.csv".format(inDir=inDir)
]

fileLabels = [f.split('/')[-1].split('.')[0] for f in files]

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

    if((rate0 != 0) and (rate1 != 0) and (rate2 != 0) and (rate3 != 0)):
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

fig, axarr = plt.subplots(1,2, 
                            sharey=True, 
                            gridspec_kw={
                                'hspace': 0.2,
                                'width_ratios': (0.7,0.9)
                                }
                            )  

leftPlot = axarr[0]
rightPlot = axarr[1]
degrees = 0 
leftPlot.set_yticks(x_indicies)
leftPlot.set_yticklabels(seeds_used)

colors = [
    'C0', 'C1', 'C2', 'C3'
]

markers = [
    's', 'o', 'X', '*'
]

for file_i in range(0, len(files)):
    color, marker = colors[file_i], markers[file_i]
    exec("leftPlot.plot(df_out_%s['rate'], x_indicies, color = color, marker = marker, alpha = 0.5, linewidth = 0)"%(file_i))
    exec("leftPlot.errorbar(df_out_%s['rate'], x_indicies, xerr=yerr%s, fmt='', capsize = 3, linestyle='', color = color, marker = marker, alpha = 0.5, linewidth = 0)"%(file_i, file_i))

leftPlot.legend(fileLabels)
leftPlot.set_xlabel('Rate (Hz)', fontsize=15)

# if(includeAll):
#     leftPlot.legend(['Run 2 Emu','Run 2 Data', 'Run2ECALSim'])
# else:
#     leftPlot.legend(['Run 2 Emu','Run 2 Data'])

leftPlot.grid(True, axis = "y")
ymin, ymax = leftPlot.get_ylim()

if(not os.path.isdir(ol)):
    print("Creating directory:",ol)
    os.system("mkdir -p %s"%(ol))

upperRightText = "0.210 fb-1"
xmin = 0.30
addLumi = 1     
lumi = 0.210
Add_CMS_Header(plt, leftPlot, upperRightText, xmin, addLumi, lumi)

for file_i in range(0, len(files)):
    if(file_i == 1): continue # don't include data unpacked
    color, marker = colors[file_i], markers[file_i]
    exec("rightPlot.plot(ratios_to_data%s, x_indicies, color = color, marker = marker, alpha = 0.5, linewidth = 0)"%(file_i))
    exec("rightPlot.errorbar(ratios_to_data%s, x_indicies, xerr = ratios_to_data%s_errs, color=color, marker = marker, capsize = 3, alpha = 0.5, linestyle='')"%(file_i, file_i))

# if(error):
#     rightPlot.errorbar(ratios_to_data1, x_indicies, xerr = ratios_to_data1_errs, color="b", marker = "s", capsize = 3, alpha = 0.5, linestyle='')
#     if(includeAll): rightPlot.errorbar(ratios_to_data3, x_indicies, xerr = ratios_to_data3_errs, color="g", marker = "x", capsize = 3, alpha = 0.5, linestyle='')    

rightPlot.set_xlabel('Ratio to Data', fontsize=15)
rightPlot.grid(True)
rightPlot.set_xlim(0.5, 1.5)
nSeeds = len(seeds_used)
rightPlot.axvline(1., ymin, ymax, color = 'C1', linestyle = "--", alpha = 0.5)
fig.set_size_inches(5, 10)
outName = "{ol}/plot.png".format(ol=ol)
plt.savefig(outName, dpi = 300, bbox_inches='tight')

outName = "{ol}/plot.pdf".format(ol=ol)
plt.savefig(outName, dpi = 300, bbox_inches='tight')