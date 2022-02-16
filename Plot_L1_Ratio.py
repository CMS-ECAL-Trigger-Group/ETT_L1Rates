"""
15 February 2022
Created by Uttiya Sarkar, updated by Abraham Tishelman-Charny

The purpose of this module is to plot L1 rates for different seeds in order to evaluate the effect of different ECAL L1 configurations on L1 rates.

Example usage:

python Plot_L1_Ratio.py --ol /eos/user/a/atishelm/www/EcalL1Optimization/L1_Quantities/rates/ --error

"""

# imports 
import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse 
import numpy as np 
import math 

# command line arguments 
parser = argparse.ArgumentParser()
parser.add_argument("--ol", help = "Output location")
parser.add_argument("--error", action="store_true", help = "Plot error bars")
parser.add_argument("--includeAll", action="store_true", help = "Plot all configs")
args = parser.parse_args()

ol = args.ol 
error = args.error 
includeAll = args.includeAll

##-- CMS header 
def Add_CMS_Header(plt, ax, upperRightText, xmin, addLumi, lumi):
    plt.text(
        0., 1., u"CMS ",
        fontsize=12, fontweight='bold',
        horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax.transAxes
    )

    prelim_x = xmin
    
    ##-- Preliminary 
    plt.text(
        prelim_x, 0.999, u"$\it{Preliminary}$",
        fontsize=12,
        horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax.transAxes
    )    

    # # upper right text 
    # plt.text(
    #     1., 1., upperRightText,
    #     fontsize=16, horizontalalignment='right', 
    #     verticalalignment='bottom', 
    #     transform=ax.transAxes
    # )  

    if(addLumi):
        upperRightText = r"%s fb$^{-1}$ (13 TeV)"%(str(lumi))
    else:
        upperRightText = r"(13 TeV)"

    ##-- Lumi 
    plt.text(
        2.7, 1., upperRightText,
        fontsize=12, horizontalalignment='right', 
        verticalalignment='bottom', 
        transform=ax.transAxes
    )   

# Get csv files with rate information 
# FileDirec = "/afs/cern.ch/work/a/atishelm/private/CMS-ECAL-Trigger-Group/L1Rates/CMSSW_12_3_0_pre1/src/L1MenuTools/rate-estimation/results_wrongGT/"
FileDirec = "/afs/cern.ch/work/a/atishelm/private/CMS-ECAL-Trigger-Group/L1Rates/CMSSW_12_3_0_pre1/src/L1MenuTools/rate-estimation/results_correctGT/"
# FileDirec = "/afs/cern.ch/work/a/atishelm/private/CMS-ECAL-Trigger-Group/L1Rates/CMSSW_12_3_0_pre1/src/L1MenuTools/rate-estimation/results/"

print("FileDirec:",FileDirec)

# f1 = "{FileDirec}/Data_fewFiles.csv".format(FileDirec=FileDirec)
# f2 = "{FileDirec}/Data_Unpacked_fewFiles.csv".format(FileDirec=FileDirec)
# f3 = "{FileDirec}/StripSubConfig.csv".format(FileDirec=FileDirec)

f1 = "{FileDirec}/Run2Config.csv".format(FileDirec=FileDirec)
f2 = "{FileDirec}/Run2Config_unpackedData.csv".format(FileDirec=FileDirec)
f3 = "{FileDirec}/StripSubConfig.csv".format(FileDirec=FileDirec)

# f1 = "{FileDirec}/Data_Emu_oneFile.csv".format(FileDirec=FileDirec)
# f2 = "{FileDirec}/Data_Unpacked_oneFile.csv".format(FileDirec=FileDirec)
# f3 = "{FileDirec}/StripSubConfig.csv".format(FileDirec=FileDirec)

seeds = [
    "L1_Mu5_EG23er2p5",      
    "L1_Mu7_EG20er2p5",     
    "L1_Mu7_EG23er2p5",    
    "L1_Mu20_EG10er2p5",      
    "L1_Mu5_LooseIsoEG20er2p5",      
    "L1_Mu7_LooseIsoEG20er2p5",      
    "L1_Mu7_LooseIsoEG23er2p5",      
    "L1_Mu6_DoubleEG10er2p5",      
    "L1_Mu6_DoubleEG12er2p5",      
    "L1_Mu6_DoubleEG15er2p5",   
    "L1_Mu6_DoubleEG17er2p5",     
    "L1_DoubleMu4_SQ_EG9er2p5",      
    "L1_DoubleMu5_SQ_EG9er2p5",     
    "L1_DoubleMu3_OS_DoubleEG7p5Upsilon",     
    "L1_DoubleMu5Upsilon_OS_DoubleEG3",  

    "L1_SingleEG8er2p5",      
    "L1_SingleEG10er2p5",      
    "L1_SingleEG15er2p5",      
    "L1_SingleEG26er2p5",      
    "L1_SingleEG28_FWD2p5",      
    "L1_SingleEG28er2p5",      
    "L1_SingleEG28er2p1",      
    "L1_SingleEG28er1p5",   
    "L1_SingleEG34er2p5",      
    "L1_SingleEG36er2p5",
    "L1_SingleEG38er2p5",      
    "L1_SingleEG40er2p5",      
    "L1_SingleEG42er2p5",      
    "L1_SingleEG45er2p5",      
    "L1_SingleEG50",      
    "L1_SingleEG60",    

    "L1_SingleLooseIsoEG26er2p5",      
    "L1_SingleLooseIsoEG26er1p5",      
    "L1_SingleLooseIsoEG28_FWD2p5",      
    "L1_SingleLooseIsoEG28er2p5",      
    "L1_SingleLooseIsoEG28er2p1",      
    "L1_SingleLooseIsoEG28er1p5",      
    "L1_SingleLooseIsoEG30er2p5",      
    "L1_SingleLooseIsoEG30er1p5",    

    "L1_SingleIsoEG24er2p1",      
    "L1_SingleIsoEG24er1p5",      
    "L1_SingleIsoEG26er2p5",      
    "L1_SingleIsoEG26er2p1",      
    "L1_SingleIsoEG26er1p5",      
    "L1_SingleIsoEG28_FWD2p5",      
    "L1_SingleIsoEG28er2p5",      
    "L1_SingleIsoEG28er2p1",      
    "L1_SingleIsoEG28er1p5",      
    "L1_SingleIsoEG30er2p5",      
    "L1_SingleIsoEG30er2p1",      
    "L1_SingleIsoEG32er2p5",      
    "L1_SingleIsoEG32er2p1",      
    "L1_SingleIsoEG34er2p5",   

    "L1_IsoEG32er2p5_Mt40",      
    "L1_IsoEG32er2p5_Mt44",      
    "L1_IsoEG32er2p5_Mt48",    
    "L1_DoubleEG_15_10_er2p5",      
    "L1_DoubleEG_20_10_er2p5",      
    "L1_DoubleEG_22_10_er2p5",      
    "L1_DoubleEG_25_12_er2p5",    
    "L1_DoubleEG_25_14_er2p5",     
    "L1_DoubleEG_27_14_er2p5",   
    "L1_DoubleEG_LooseIso20_10_er2p5",      
    "L1_DoubleEG_LooseIso22_10_er2p5",      
    "L1_DoubleEG_LooseIso22_12_er2p5",     
    "L1_DoubleEG_LooseIso25_12_er2p5",    
    "L1_DoubleLooseIsoEG22er2p1",      
    "L1_DoubleLooseIsoEG24er2p1",   

    "L1_TripleEG_16_12_8_er2p5",      
    "L1_TripleEG_16_15_8_er2p5",      
    "L1_TripleEG_18_17_8_er2p5",      
    "L1_TripleEG_18_18_12_er2p5",      
    "L1_TripleEG16er2p5",      

    "L1_LooseIsoEG26er2p1_Jet34er2p5_dR_Min0p3",      
    "L1_LooseIsoEG28er2p1_Jet34er2p5_dR_Min0p3",   
    "L1_LooseIsoEG30er2p1_Jet34er2p5_dR_Min0p3",    
    "L1_LooseIsoEG24er2p1_HTT100er",      
    "L1_LooseIsoEG26er2p1_HTT100er",     
    "L1_LooseIsoEG28er2p1_HTT100er",      
    "L1_LooseIsoEG30er2p1_HTT100er",   

    "L1_DoubleEG8er2p5_HTT260er",      
    "L1_DoubleEG8er2p5_HTT280er",      
    "L1_DoubleEG8er2p5_HTT300er",      
    "L1_DoubleEG8er2p5_HTT320er",      
    "L1_DoubleEG8er2p5_HTT340er",    

    "L1_LooseIsoEG22er2p1_IsoTau26er2p1_dR_Min0p3",      
    "L1_LooseIsoEG24er2p1_IsoTau27er2p1_dR_Min0p3",      
    "L1_LooseIsoEG22er2p1_Tau70er2p1_dR_Min0p3",      
]

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
    leftPlot.legend(['Run 2 Emu','Run 2 Data', 'Strip zeroing'])
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
rightPlot.axvline(1., ymin, ymax, color = 'black', linestyle = "-")
fig.set_size_inches(5, 10)
outName = "{ol}/plot.png".format(ol=ol)
plt.savefig(outName, dpi = 300, bbox_inches='tight')

outName = "{ol}/plot.pdf".format(ol=ol)
plt.savefig(outName, dpi = 300, bbox_inches='tight')

### When you want to plot rates per fill 
"""

# assign path
path1, dirs1, files1 = next(os.walk("./onceperfill/"))
file_countopf = len(files1)

# assign path
path2, dirs2, files2 = next(os.walk("./twiceperweek/"))
file_counttpw = len(files2)

# create empty lists
dfs_listopf = []
dfs_listtpw = []
filenameopf = []
filenametpw = []
# append datasets to the list
for i in range(file_countopf):
    temp_df = pd.read_csv("./onceperfill/"+files1[i])
    names = files1[i]
    filenameopf.append(names)
    dfs_listopf.append(temp_df)  

for i in range(file_counttpw):
    temp_df = pd.read_csv("./twiceperweek/"+files2[i])
    names = files2[i]
    filenametpw.append(names)
    dfs_listtpw.append(temp_df)

# display datsets
#for dataset in dfs_listtpw:
#    display(dataset)
filenameopf = [x.replace('_246', '') for x in filenameopf]
filenameopf = [x.replace('.csv', '') for x in filenameopf]
filenametpw = [x.replace('_54', '') for x in filenametpw]
filenametpw = [x.replace('.csv', '') for x in filenametpw]

#--------sometimes important to uncomment and check if 
#there is any ghost fillnumber other than the expected---------------
#filenametpw 
#filenameopf

# set index to L1SeedName and print the rate0
rateopf = []
ratetpw = []
rateopf2 = []
ratetpw2 = []
for df in dfs_listopf:
    df.set_index('L1SeedName', inplace=True)
    df = df.loc[['L1_SingleIsoEG28er2p5','L1_SingleMu22']]
    df = df.reset_index()
    l = df.iloc[0]['rate0']
    l2 = df.iloc[1]['rate0']
    l = l/l2
    rateopf.append(l)
    
for df in dfs_listtpw:
    df.set_index('L1SeedName', inplace=True)
    df = df.loc[['L1_SingleIsoEG28er2p5','L1_SingleMu22']]
    df = df.reset_index()
    l = df.iloc[0]['rate0']
    l2 = df.iloc[1]['rate0']
    l = l/l2
    ratetpw.append(l)


#creating dataframe from the seed rates
df_opf = pd.DataFrame({'Fill_Number':filenameopf, 'rate':rateopf})
df_opf = df_opf.sort_values(by=['Fill_Number'])
df_tpw = pd.DataFrame({'Fill_Number':filenametpw, 'rate':ratetpw})
df_tpw = df_tpw.sort_values(by=['Fill_Number'])

#finally a sigh of relief after all the juggling
fig, ax = plt.subplots(figsize=(8,4))
ax.scatter(df_tpw["Fill_Number"],df_tpw["rate"],color="blue",marker="+", alpha=0.5)
ax.scatter(df_opf["Fill_Number"],df_opf["rate"],color="red",marker="o", alpha=0.5)
ax.set_xlabel('Fill Number', fontsize=15)
ax.set_ylabel('Rate (Hz)', fontsize=15)
ax.set_title('L1_SingleIsoEG28er2p5 Normalized by L1_SingleMu22')
ax.legend(['54 iov','246 iov'])
ax.grid(True)
fig.tight_layout()

outName = "{ol}/plot.png".format(ol=ol)
plt.savefig(outName, dpi = 300)

outName = "{ol}/plot.pdf".format(ol=ol)
plt.savefig(outName, dpi = 300)

"""