"""
17 February 2022
Abraham Tishelman-Charny 

The purpose of this module is to provide functionality and tools for Plot_L1_Ratio. 
"""

# imports 
import argparse 
from matplotlib import pyplot as plt
import os 
import numpy as np 

def GetArgs():
    # command line arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument("--ol", help = "Output location")
    parser.add_argument("--inDir", help = "Input directory with rate files")
    parser.add_argument("--error", action="store_true", help = "Plot error bars")
    parser.add_argument("--includeAll", action="store_true", help = "Plot all configs")
    parser.add_argument("--seedsPerPage", type = int, help = "Number of rates to plot per page")
    args = parser.parse_args()

    arg_names = ["ol", "inDir", "error", "includeAll", "seedsPerPage"]

    return args, arg_names 


def GetSeeds():

    seeds_ = [
                'L1_SingleMuCosmics', 'L1_SingleMuCosmics_BMTF', 'L1_SingleMuCosmics_OMTF', 'L1_SingleMuCosmics_EMTF', 'L1_SingleMuOpen', 'L1_SingleMu0_DQ', 'L1_SingleMu0_BMTF', 'L1_SingleMu0_OMTF', 'L1_SingleMu0_EMTF', 'L1_SingleMu3', 'L1_SingleMu5', 'L1_SingleMu7_DQ', 'L1_SingleMu7', 'L1_SingleMu12_DQ_BMTF', 'L1_SingleMu12_DQ_OMTF', 'L1_SingleMu12_DQ_EMTF', 'L1_SingleMu15_DQ', 'L1_SingleMu18', 'L1_SingleMu20', 'L1_SingleMu22', 'L1_SingleMu22_BMTF', 'L1_SingleMu22_OMTF', 
                'L1_SingleMu22_EMTF', 'L1_SingleMu25', 'L1_SingleMu6er1p5', 'L1_SingleMu7er1p5', 'L1_SingleMu8er1p5', 'L1_SingleMu9er1p5', 'L1_SingleMu10er1p5', 'L1_SingleMu12er1p5', 'L1_SingleMu14er1p5', 'L1_SingleMu16er1p5', 'L1_SingleMu18er1p5', 'L1_DoubleMu0_OQ', 'L1_DoubleMu0', 'L1_DoubleMu0_SQ', 'L1_DoubleMu0_SQ_OS', 'L1_DoubleMu0_Mass_Min1', 'L1_DoubleMu8_SQ', 'L1_DoubleMu9_SQ', 'L1_DoubleMu_12_5', 'L1_DoubleMu_15_5_SQ', 'L1_DoubleMu_15_7', 'L1_DoubleMu_15_7_SQ', 'L1_DoubleMu_15_7_Mass_Min1', 'L1_DoubleMu18er2p1', 'L1_DoubleMu0er2p0_SQ_dR_Max1p4', 'L1_DoubleMu0er2p0_SQ_OS_dR_Max1p4', 'L1_DoubleMu0er1p5_SQ', 'L1_DoubleMu0er1p5_SQ_OS', 'L1_DoubleMu0er1p5_SQ_dR_Max1p4', 'L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4', 'L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4', 'L1_DoubleMu4_SQ_OS', 'L1_DoubleMu4_SQ_OS_dR_Max1p2', 'L1_DoubleMu4p5_SQ_OS', 'L1_DoubleMu4p5_SQ_OS_dR_Max1p2', 'L1_DoubleMu4p5er2p0_SQ_OS', 'L1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7', 'L1_DoubleMu4p5er2p0_SQ_OS_Mass7to18', 'L1_TripleMu0_OQ', 'L1_TripleMu0', 'L1_TripleMu0_SQ', 'L1_TripleMu3', 'L1_TripleMu3_SQ', 'L1_TripleMu_5SQ_3SQ_0OQ', 'L1_TripleMu_5_3p5_2p5', 'L1_TripleMu_5_3_3', 'L1_TripleMu_5_3_3_SQ', 'L1_TripleMu_5_5_3', 'L1_TripleMu_5_3p5_2p5_OQ_DoubleMu_5_2p5_OQ_OS_Mass_5to17', 'L1_TripleMu_5_3p5_2p5_DoubleMu_5_2p5_OS_Mass_5to17', 'L1_TripleMu_5_4_2p5_DoubleMu_5_2p5_OS_Mass_5to17', 'L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9', 'L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9', 'L1_QuadMu0_OQ', 'L1_QuadMu0', 'L1_QuadMu0_SQ', 'L1_Mu5_EG23er2p5', 'L1_Mu7_EG20er2p5', 'L1_Mu7_EG23er2p5', 'L1_Mu20_EG10er2p5', 'L1_Mu5_LooseIsoEG20er2p5', 'L1_Mu7_LooseIsoEG20er2p5', 'L1_Mu7_LooseIsoEG23er2p5', 'L1_Mu6_DoubleEG10er2p5', 'L1_Mu6_DoubleEG12er2p5', 'L1_Mu6_DoubleEG15er2p5', 'L1_Mu6_DoubleEG17er2p5', 'L1_DoubleMu4_SQ_EG9er2p5', 'L1_DoubleMu5_SQ_EG9er2p5', 'L1_DoubleMu3_OS_DoubleEG7p5Upsilon', 'L1_DoubleMu5Upsilon_OS_DoubleEG3', 'L1_Mu3_Jet30er2p5', 'L1_Mu3_Jet16er2p5_dR_Max0p4', 'L1_Mu3_Jet35er2p5_dR_Max0p4', 'L1_Mu3_Jet60er2p5_dR_Max0p4', 'L1_Mu3_Jet80er2p5_dR_Max0p4', 'L1_Mu3_Jet120er2p5_dR_Max0p8', 'L1_Mu3_Jet120er2p5_dR_Max0p4', 'L1_Mu3er1p5_Jet100er2p5_ETMHF40', 'L1_Mu3er1p5_Jet100er2p5_ETMHF50', 'L1_Mu6_HTT240er', 'L1_Mu6_HTT250er', 'L1_Mu10er2p3_Jet32er2p3_dR_Max0p4_DoubleJet32er2p3_dEta_Max1p6', 'L1_Mu12er2p3_Jet40er2p3_dR_Max0p4_DoubleJet40er2p3_dEta_Max1p6', 'L1_Mu12er2p3_Jet40er2p1_dR_Max0p4_DoubleJet40er2p1_dEta_Max1p6', 'L1_DoubleMu0_dR_Max1p6_Jet90er2p5_dR_Max0p8', 'L1_DoubleMu3_dR_Max1p6_Jet90er2p5_dR_Max0p8', 'L1_DoubleMu3_SQ_ETMHF50_HTT60er', 'L1_DoubleMu3_SQ_ETMHF50_Jet60er2p5_OR_DoubleJet40er2p5', 'L1_DoubleMu3_SQ_ETMHF50_Jet60er2p5', 'L1_DoubleMu3_SQ_ETMHF60_Jet60er2p5', 'L1_DoubleMu3_SQ_HTT220er', 'L1_DoubleMu3_SQ_HTT240er', 'L1_DoubleMu3_SQ_HTT260er', 'L1_SingleEG8er2p5', 'L1_SingleEG10er2p5', 'L1_SingleEG15er2p5', 'L1_SingleEG26er2p5', 'L1_SingleEG28_FWD2p5', 'L1_SingleEG28er2p5', 'L1_SingleEG28er2p1', 'L1_SingleEG28er1p5', 'L1_SingleEG34er2p5', 'L1_SingleEG36er2p5', 'L1_SingleEG38er2p5', 'L1_SingleEG40er2p5', 'L1_SingleEG42er2p5', 'L1_SingleEG45er2p5', 'L1_SingleEG50', 'L1_SingleEG60', 'L1_SingleLooseIsoEG26er2p5', 'L1_SingleLooseIsoEG26er1p5', 'L1_SingleLooseIsoEG28_FWD2p5', 'L1_SingleLooseIsoEG28er2p5', 'L1_SingleLooseIsoEG28er2p1', 'L1_SingleLooseIsoEG28er1p5', 'L1_SingleLooseIsoEG30er2p5', 'L1_SingleLooseIsoEG30er1p5', 'L1_SingleIsoEG24er2p1', 'L1_SingleIsoEG24er1p5', 'L1_SingleIsoEG26er2p5', 'L1_SingleIsoEG26er2p1', 'L1_SingleIsoEG26er1p5', 'L1_SingleIsoEG28_FWD2p5', 'L1_SingleIsoEG28er2p5', 'L1_SingleIsoEG28er2p1', 'L1_SingleIsoEG28er1p5', 'L1_SingleIsoEG30er2p5', 'L1_SingleIsoEG30er2p1', 'L1_SingleIsoEG32er2p5', 'L1_SingleIsoEG32er2p1', 'L1_SingleIsoEG34er2p5', 'L1_IsoEG32er2p5_Mt40', 'L1_IsoEG32er2p5_Mt44', 'L1_IsoEG32er2p5_Mt48', 'L1_DoubleEG_15_10_er2p5', 'L1_DoubleEG_20_10_er2p5', 'L1_DoubleEG_22_10_er2p5', 'L1_DoubleEG_25_12_er2p5', 'L1_DoubleEG_25_14_er2p5', 'L1_DoubleEG_27_14_er2p5', 'L1_DoubleEG_LooseIso20_10_er2p5', 'L1_DoubleEG_LooseIso22_10_er2p5', 'L1_DoubleEG_LooseIso22_12_er2p5', 'L1_DoubleEG_LooseIso25_12_er2p5', 'L1_DoubleLooseIsoEG22er2p1', 'L1_DoubleLooseIsoEG24er2p1', 'L1_TripleEG_16_12_8_er2p5', 'L1_TripleEG_16_15_8_er2p5', 'L1_TripleEG_18_17_8_er2p5', 'L1_TripleEG_18_18_12_er2p5', 'L1_TripleEG16er2p5', 'L1_LooseIsoEG26er2p1_Jet34er2p5_dR_Min0p3', 'L1_LooseIsoEG28er2p1_Jet34er2p5_dR_Min0p3', 'L1_LooseIsoEG30er2p1_Jet34er2p5_dR_Min0p3', 'L1_LooseIsoEG24er2p1_HTT100er', 'L1_LooseIsoEG26er2p1_HTT100er', 'L1_LooseIsoEG28er2p1_HTT100er', 'L1_LooseIsoEG30er2p1_HTT100er', 'L1_DoubleEG8er2p5_HTT260er', 'L1_DoubleEG8er2p5_HTT280er', 'L1_DoubleEG8er2p5_HTT300er', 'L1_DoubleEG8er2p5_HTT320er', 'L1_DoubleEG8er2p5_HTT340er', 'L1_LooseIsoEG22er2p1_IsoTau26er2p1_dR_Min0p3', 'L1_LooseIsoEG24er2p1_IsoTau27er2p1_dR_Min0p3', 'L1_LooseIsoEG22er2p1_Tau70er2p1_dR_Min0p3', 'L1_SingleTau120er2p1', 'L1_SingleTau130er2p1', 'L1_DoubleTau70er2p1', 'L1_DoubleIsoTau28er2p1', 'L1_DoubleIsoTau30er2p1', 'L1_DoubleIsoTau32er2p1', 'L1_DoubleIsoTau34er2p1', 'L1_DoubleIsoTau36er2p1', 'L1_DoubleIsoTau28er2p1_Mass_Max90', 'L1_DoubleIsoTau28er2p1_Mass_Max80', 'L1_DoubleIsoTau30er2p1_Mass_Max90', 'L1_DoubleIsoTau30er2p1_Mass_Max80', 'L1_Mu18er2p1_Tau24er2p1', 'L1_Mu18er2p1_Tau26er2p1', 'L1_Mu22er2p1_IsoTau28er2p1', 'L1_Mu22er2p1_IsoTau30er2p1', 'L1_Mu22er2p1_IsoTau32er2p1', 
                'L1_Mu22er2p1_IsoTau34er2p1', 'L1_Mu22er2p1_IsoTau36er2p1', 'L1_Mu22er2p1_IsoTau40er2p1', 'L1_Mu22er2p1_Tau70er2p1', 'L1_IsoTau40er2p1_ETMHF80', 'L1_IsoTau40er2p1_ETMHF90', 'L1_IsoTau40er2p1_ETMHF100', 'L1_IsoTau40er2p1_ETMHF110', 
                'L1_QuadJet36er2p5_IsoTau52er2p1', 'L1_SingleJet35', 'L1_SingleJet60', 'L1_SingleJet90', 'L1_SingleJet120', 'L1_SingleJet180', 'L1_SingleJet200', 'L1_SingleJet35er2p5', 'L1_SingleJet60er2p5', 'L1_SingleJet90er2p5', 'L1_SingleJet120er2p5', 'L1_SingleJet140er2p5', 'L1_SingleJet160er2p5', 'L1_SingleJet180er2p5', 'L1_SingleJet35_FWD3p0', 'L1_SingleJet60_FWD3p0', 'L1_SingleJet90_FWD3p0', 'L1_SingleJet120_FWD3p0', 'L1_SingleJet8erHE', 'L1_SingleJet10erHE', 'L1_SingleJet12erHE', 'L1_SingleJet140er2p5_ETMHF70', 'L1_SingleJet140er2p5_ETMHF80', 'L1_SingleJet140er2p5_ETMHF90', 'L1_DoubleJet40er2p5', 'L1_DoubleJet100er2p5', 'L1_DoubleJet120er2p5', 'L1_DoubleJet150er2p5', 'L1_DoubleJet100er2p3_dEta_Max1p6', 'L1_DoubleJet112er2p3_dEta_Max1p6', 'L1_DoubleJet30er2p5_Mass_Min150_dEta_Max1p5', 'L1_DoubleJet30er2p5_Mass_Min200_dEta_Max1p5', 'L1_DoubleJet30er2p5_Mass_Min250_dEta_Max1p5', 'L1_DoubleJet30er2p5_Mass_Min300_dEta_Max1p5', 'L1_DoubleJet30er2p5_Mass_Min330_dEta_Max1p5', 'L1_DoubleJet30er2p5_Mass_Min360_dEta_Max1p5', 'L1_DoubleJet_90_30_DoubleJet30_Mass_Min620', 'L1_DoubleJet_100_30_DoubleJet30_Mass_Min620', 'L1_DoubleJet_110_35_DoubleJet35_Mass_Min620', 'L1_DoubleJet_115_40_DoubleJet40_Mass_Min620', 'L1_DoubleJet_120_45_DoubleJet45_Mass_Min620', 'L1_DoubleJet_115_40_DoubleJet40_Mass_Min620_Jet60TT28', 'L1_DoubleJet_120_45_DoubleJet45_Mass_Min620_Jet60TT28', 'L1_DoubleJet35_Mass_Min450_IsoTau45_RmOvlp', 'L1_DoubleJet_80_30_Mass_Min420_IsoTau40_RmOvlp', 'L1_DoubleJet_80_30_Mass_Min420_Mu8', 'L1_DoubleJet_80_30_Mass_Min420_DoubleMu0_SQ', 'L1_TripleJet_95_75_65_DoubleJet_75_65_er2p5', 'L1_TripleJet_100_80_70_DoubleJet_80_70_er2p5', 'L1_TripleJet_105_85_75_DoubleJet_85_75_er2p5', 'L1_QuadJet_95_75_65_20_DoubleJet_75_65_er2p5_Jet20_FWD3p0', 'L1_QuadJet60er2p5', 'L1_HTT280er_QuadJet_70_55_40_35_er2p4', 'L1_HTT320er_QuadJet_70_55_40_40_er2p4', 'L1_HTT320er_QuadJet_80_60_er2p1_45_40_er2p3', 'L1_HTT320er_QuadJet_80_60_er2p1_50_45_er2p3', 'L1_HTT120er', 'L1_HTT160er', 'L1_HTT200er', 'L1_HTT255er', 'L1_HTT280er', 'L1_HTT320er', 'L1_HTT360er', 'L1_HTT400er', 'L1_HTT450er', 'L1_ETT1200', 'L1_ETT1600', 'L1_ETT2000', 'L1_ETM120', 'L1_ETM150', 'L1_ETMHF100', 'L1_ETMHF110', 'L1_ETMHF120', 'L1_ETMHF130', 'L1_ETMHF140', 'L1_ETMHF150', 'L1_ETMHF90_HTT60er', 'L1_ETMHF100_HTT60er', 'L1_ETMHF110_HTT60er', 'L1_ETMHF120_HTT60er', 'L1_ETMHF130_HTT60er', 'L1_ETMHF120_NotSecondBunchInTrain', 'L1_ETMHF110_HTT60er_NotSecondBunchInTrain', 'L1_SingleMuOpen_NotBptxOR', 'L1_SingleMuOpen_er1p4_NotBptxOR_3BX', 'L1_SingleMuOpen_er1p1_NotBptxOR_3BX', 'L1_SingleJet20er2p5_NotBptxOR', 'L1_SingleJet20er2p5_NotBptxOR_3BX', 'L1_SingleJet43er2p5_NotBptxOR_3BX', 'L1_SingleJet46er2p5_NotBptxOR_3BX', 'L1_AlwaysTrue', 'L1_ZeroBias', 'L1_ZeroBias_copy', 'L1_MinimumBiasHF0_AND_BptxAND', 'L1_NotBptxOR', 'L1_BptxOR', 'L1_BptxXOR', 'L1_BptxPlus', 'L1_BptxMinus', 'L1_UnpairedBunchBptxPlus', 'L1_UnpairedBunchBptxMinus', 'L1_IsolatedBunch', 'L1_FirstBunchBeforeTrain', 'L1_FirstBunchInTrain', 'L1_SecondBunchInTrain', 'L1_SecondLastBunchInTrain', 'L1_LastBunchInTrain', 'L1_FirstBunchAfterTrain', 'L1_LastCollisionInTrain', 'L1_FirstCollisionInTrain', 'L1_FirstCollisionInOrbit', 'L1_BPTX_NotOR_VME', 'L1_BPTX_OR_Ref3_VME', 'L1_BPTX_OR_Ref4_VME', 
                'L1_BPTX_RefAND_VME', 'L1_BPTX_AND_Ref1_VME', 'L1_BPTX_AND_Ref3_VME', 'L1_BPTX_AND_Ref4_VME', 'L1_BPTX_BeamGas_Ref1_VME', 'L1_BPTX_BeamGas_Ref2_VME', 'L1_BPTX_BeamGas_B1_VME', 'L1_BPTX_BeamGas_B2_VME', 'L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142', 'L1_HCAL_LaserMon_Trig', 'L1_HCAL_LaserMon_Veto', 'L1_TOTEM_1', 'L1_TOTEM_2', 'L1_TOTEM_3', 'L1_TOTEM_4', 'Total rate'
            ]

    return seeds_ 

##-- CMS header 
def Add_CMS_Header(plt, ax, upperRightText, xmin, addLumi, lumi):
    plt.text(
        0., 1., u"CMS ",
        fontsize=14, fontweight='bold',
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

def MakePlot(
                plot_i, N_files, fileLabels, seedsPerPage, ol, x_indicies, seeds_used, 
                df_out_0, df_out_1, df_out_2, df_out_3, 
                yerr0, yerr1, yerr2, yerr3, 
                ratios_to_data0, ratios_to_data2, ratios_to_data3, 
                ratios_to_data0_errs, ratios_to_data2_errs, ratios_to_data3_errs
            ):
    fig, axarr = plt.subplots(1,2, 
                                sharey=True, 
                                gridspec_kw={
                                    # 'hspace': 0.2,
                                    'hspace': 0.4,
                                    'width_ratios': (0.7,0.9)
                                    }
                                )  

    leftPlot = axarr[0]
    rightPlot = axarr[1]
    degrees = 0 
    leftPlot.set_yticks(x_indicies)
    leftPlot.set_yticklabels(seeds_used)

    colors = ['C0', 'C1', 'C2', 'C3']
    markers = ['s', 'o', 'X', '*']

    alpha = 1 

    for file_i in range(0, N_files):
        color, marker = colors[file_i], markers[file_i]

        exec("leftPlot.plot(df_out_%s, x_indicies, color = color, marker = marker, alpha = alpha, linewidth = 0)"%(file_i))
        exec("leftPlot.errorbar(df_out_%s, x_indicies, xerr=yerr%s, fmt='', capsize = 3, linestyle='', color = color, marker = marker, alpha = alpha, linewidth = 0)"%(file_i, file_i))

    leftPlot.set_xlabel('Rate (Hz)', fontsize=15)
    leftPlot.grid(True)
    ymin, ymax = leftPlot.get_ylim()

    if(not os.path.isdir(ol)):
        print("Creating directory:",ol)
        os.system("mkdir -p %s"%(ol))

    upperRightText = "0.210 fb-1"
    xmin = 0.33
    addLumi = 1     
    lumi = 0.210
    Add_CMS_Header(plt, leftPlot, upperRightText, xmin, addLumi, lumi)

    for file_i in range(0, N_files):
        if(file_i == 1): continue # don't include data unpacked
        color, marker = colors[file_i], markers[file_i]
        exec("rightPlot.plot(ratios_to_data%s, x_indicies, color = color, marker = marker, alpha = alpha, linewidth = 0)"%(file_i))
        exec("rightPlot.errorbar(ratios_to_data%s, x_indicies, xerr = ratios_to_data%s_errs, color=color, marker = marker, capsize = 3, alpha = alpha, linestyle='')"%(file_i, file_i))

    rightPlot.set_xlabel('Ratio to Data', fontsize=15)
    rightPlot.grid(True)
    rightPlot.set_xlim(0.5, 1.5)
    nSeeds = len(seeds_used)
    rightPlot.axvline(1., ymin, ymax, color = 'C1', linestyle = "--", alpha = 0.5)
    fig.set_size_inches(5, 10)

    leftPlot.legend(fileLabels, bbox_to_anchor=(2, 1), framealpha=1)

    # leftPlot.set_ylim(-5, 5)
    # rightPlot.set_ylim(-5, 5)

    ymin, ymax = leftPlot.get_ylim()
    # print("ylim_vals:",ylim_vals)

    # make space for legend 
    space = seedsPerPage * 0.15 # 15% 
    leftPlot.set_ylim(ymin, ymax + space)
    rightPlot.set_ylim(ymin, ymax + space)

    rightPlot.set_zorder(-1)

    outName = "{ol}/plot_{plot_i}.png".format(ol=ol, plot_i=plot_i)
    plt.savefig(outName, dpi = 300, bbox_inches='tight')

    outName = "{ol}/plot_{plot_i}.pdf".format(ol=ol, plot_i=plot_i)
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