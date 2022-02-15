# L1Rates

The purpose of this repository is to compute L1 rates resulting from different ECAL L1 configurations, in order to understand the downstream effect of different ECAL configurations. 

## Setup

`To be added` 

[L1 ntuple production](https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1TriggerExpertAnalyst#L1NTuple_production)

[rate estimation using L1 ntuples](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HowToL1TriggerMenu#4_Run_3_settings)

## Rough workflow 

```
crab submit -c <Configuration_1>
crab submit -c <Configuration_2>

cd CMSSW_12_3_0_pre1/src/L1MenuTools/rate-estimation

./makeFileList.py /eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/L1_Rates_and_TurnOns/Run_320038/Run_320038_Run2/220215_145146/0000/ > DoubleWeights_Run2Config.list  # Make ntuple list 1 (output files from Configuration 1)
./makeFileList.py /eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/L1_Rates_and_TurnOns/Run_320038/Run_320038_StripZeroing/220215_145518/0000/ > DoubleWeights_StripSubConfig.list # Make ntuple list 2 (output files from Configuration 2)

Create lumi csv 
Create prescale csv 

cd

./testMenu2016 -u menu/run_lumi.csv -m menu/Prescale_2022_v0_1_1.csv -l ntuple/Configuration_1_files.list -o Configuration_1_emu -b 2544 --doPlotRate --doPlotEff --maxEvent 20000 --SelectCol 2E+34 --doPrintPU --allPileUp
./testMenu2016 -u menu/run_lumi.csv -m menu/Prescale_2022_v0_1_1.csv -l ntuple/Configuration_1_files.list -o Configuration_1_unpackedData -b 2544 --doPlotRate --doPlotEff --maxEvent 20000 --SelectCol 2E+34 --doPrintPU --allPileUp --UseUnpackTree
./testMenu2016 -u menu/run_lumi.csv -m menu/Prescale_2022_v0_1_1.csv -l ntuple/Configuration_2_files.list -o Configuration_2 -b 2544 --doPlotRate --doPlotEff --maxEvent 20000 --SelectCol 2E+34 --doPrintPU --allPileUp

```
