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

f1 = "{inDir}/Run_320038_NoECALsim_NotUnpacked.csv".format(inDir=inDir)
f2 = "{inDir}/Run_320038_NoECALsim_Unpacked.csv".format(inDir=inDir)
f3 = "{inDir}/Run_320038_Run2Mode_WithECALSim.csv".format(inDir=inDir)
# f3 = "{inDir}/StripSubConfig.csv".format(inDir=inDir)

seeds = GetSeeds()

rates1 = []
rates2 = []
rates3 = [] 

yerr1 = []
yerr2 = []
yerr3 = []

x_indicies = [] 
seeds_used = []

ratios_to_data1 = []
ratios_to_data3 = []

ratios_to_data1_errs = []
ratios_to_data3_errs = []

for seed in seeds:
    df1 = pd.read_csv(f1)
    df2 = pd.read_csv(f2)
    df3 = pd.read_csv(f3)

    df1.set_index('L1SeedName', inplace=True)
    df1 = df1.loc[seed]
    rate1 = df1.iloc[2]
    rate1_err = df1.iloc[3]  

    df2.set_index('L1SeedName', inplace=True)
    df2 = df2.loc[seed]
    rate2 = df2.iloc[2]
    rate2_err = df2.iloc[3]  

    df3.set_index('L1SeedName', inplace=True)
    df3 = df3.loc[seed]
    rate3 = df3.iloc[2]
    rate3_err = df3.iloc[3]  

    if((rate1 != 0) and (rate2 != 0) and (rate3 != 0)):
        seeds_used.append(seed)
        rates1.append(rate1) 
        rates2.append(rate2) 
        rates3.append(rate3)

        yerr1.append(rate1_err)
        yerr2.append(rate2_err)
        yerr3.append(rate3_err)

        ratio_1 = float(rate1) / float(rate2)
        ratio_3 = float(rate3) / float(rate2)

        ratios_to_data1.append(ratio_1) # assumes rate 2 is the unpacked data 
        ratios_to_data3.append(ratio_3)

        # Poissonion error (no MC weights)
        rel_err_1 = math.sqrt( (rate1_err / rate1)**2 + (rate2_err / rate2)**2)
        rel_err_3 = math.sqrt( (rate3_err / rate3)**2 + (rate2_err / rate2)**2)

        abs_err_1 = rel_err_1 * ratio_1 
        abs_err_3 = rel_err_3 * ratio_3 

        ratios_to_data1_errs.append(abs_err_1)
        ratios_to_data3_errs.append(abs_err_3)

x_indicies = [i for i in range(0,len(rates1))]

ymax = np.max(rates1)

df_out_1 = pd.DataFrame({"rate" : rates1})
df_out_2 = pd.DataFrame({"rate" : rates2})
df_out_3 = pd.DataFrame({"rate" : rates3})

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

leftPlot.plot(df_out_1["rate"], x_indicies, color="b", marker = "s", alpha = 0.5, linewidth = 0)
leftPlot.plot(df_out_2["rate"], x_indicies, color="r", marker = "o", alpha = 0.5, linewidth = 0)
if(includeAll): leftPlot.plot(df_out_3["rate"], x_indicies, color="g", marker = "X", alpha = 0.5, linewidth = 0)

if(error):
    leftPlot.errorbar(df_out_1["rate"], x_indicies,  xerr=yerr1, alpha = 0.5, fmt='', color = "b", capsize = 3, linestyle='')
    leftPlot.errorbar(df_out_2["rate"], x_indicies,  xerr=yerr2, alpha = 0.5, fmt='', color = "r", capsize = 3, linestyle='')
    if(includeAll): leftPlot.errorbar(df_out_3["rate"], x_indicies,  xerr=yerr3, alpha = 0.5, fmt='', color = "g", capsize = 3, linestyle='')

leftPlot.set_xlabel('Rate (Hz)', fontsize=15)
if(includeAll):
    leftPlot.legend(['Run 2 Emu','Run 2 Data', 'Run2ECALSim'])
else:
    leftPlot.legend(['Run 2 Emu','Run 2 Data'])
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

rightPlot.plot(ratios_to_data1, x_indicies, color="b", marker = "s", alpha = 0.5, linewidth = 0)
if(includeAll): rightPlot.plot(ratios_to_data3, x_indicies, color="g", marker = "x", alpha = 0.5, linewidth = 0)

if(error):
    rightPlot.errorbar(ratios_to_data1, x_indicies, xerr = ratios_to_data1_errs, color="b", marker = "s", capsize = 3, alpha = 0.5, linestyle='')
    if(includeAll): rightPlot.errorbar(ratios_to_data3, x_indicies, xerr = ratios_to_data3_errs, color="g", marker = "x", capsize = 3, alpha = 0.5, linestyle='')    

rightPlot.set_xlabel('Ratio to Data', fontsize=15)
rightPlot.grid(True)
rightPlot.set_xlim(0.5, 1.5)
nSeeds = len(seeds_used)
rightPlot.axvline(1., ymin, ymax, color = 'r', linestyle = "--", alpha = 0.5)
fig.set_size_inches(5, 10)
outName = "{ol}/plot.png".format(ol=ol)
plt.savefig(outName, dpi = 300, bbox_inches='tight')

outName = "{ol}/plot.pdf".format(ol=ol)
plt.savefig(outName, dpi = 300, bbox_inches='tight')