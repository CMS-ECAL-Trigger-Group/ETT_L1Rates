"""
16 August 2021 
Abraham Tishelman-Charny 

The purpose of this crab configuration file is to run the ETTAnalyzer over many CMSSW data files in parallel. 
crab submit -c CrabConfig_12_1_0_pre3.py 
"""

# runs, DatasetLabel, UserGlobalTag = DatasetInfo[Dataset]
DatasetLabel = "Run_320038"

# # Configuration parameters 
inDir = "/afs/cern.ch/work/a/atishelm/private/CMS-ECAL-Trigger-Group/L1Rates/CMSSW_12_3_0_pre1/src/ETT_L1Rates/"
simECALTP = 1 
oneFile = 0 # Run over one file as a test (recommended before running over large datasets to test incompatibility issues)
addFilePrefix = 0 # Add "file:" to start of file paths 
removeEOSprefix = 1 
# RecoMethod = "Multifit" # options: Multifit, weights
# ODD_PF = 1 # 0: No ODD peak finder. 1: With ODD peak finder

runs = ["320038"]
# ECAL_Config = "Run2"
ECAL_Config = "StripZeroing"

if(simECALTP):
  simECALTP_Tag = "simECALTP"
else:
  simECALTP_Tag = "NosimECALTP"

if(ECAL_Config == "Run2"):
  OverrideWeights = 1
  WeightsWP = "Run2Weights"
  OddWeightsSqliteFile = "MinDelta_2p5Prime_OddWeights.db" # because something needs to be passed in case a value for the record doesn't exist for the global tag / event setup 
  TPMode_file = "EcalTPG_TPMode_Run2_default.db"
  TPMode_Tag = "EcalTPG_TPMode_Run2_default"
else:
  OverrideWeights = 1 
  OddWeightsSqliteFile="MinDelta_2p5Prime_OddWeights.db"
  WeightsWP = "2p5Prime"
  TPMode_file = "EcalTPG_TPMode_Run3_zeroingOddPeakFinder.db"
  TPMode_Tag = "EcalTPG_TPMode_Run3_zeroingOddPeakFinder"

CMS_files = []
print("Adding CMS files...")

# By run number 
for run in runs:
     print("Run",run)
     text_file_path = "RunsAndFiles/Files_Run_%s.txt"%(run)
     with open(text_file_path) as f: # https://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list
         content = f.readlines()
         content = [x.strip() for x in content] 
         for file in content:
             if(addFilePrefix): file_path = "file:%s"%(file)
             else: 
                 if(removeEOSprefix): file = file.replace("/eos/cms", "")
                 file_path = file 

             CMS_files.append(file_path)

# To get 2018 ZeroBias data files 
"""
Nblocks = 11 # Max: 11 
##-- By block number 
for block_i in range(0, Nblocks):
    print "On block",block_i
    text_file_path = "RunsAndFiles/Files_Block_%s.txt"%(block_i)
    with open(text_file_path) as f: 
        content = f.readlines()
        content = [x.strip() for x in content] 
        for file in content:
            CMS_files.append(file)  

# for computing lumi 
# https://twiki.cern.ch/twiki/bin/view/CMS/AbrahamTishelmanCharnyHomepage#Checking_Dataset_Luminosity
# export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH
# pip install --install-option="--prefix=$HOME/.local" brilws
# https://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html
# voms 
# http://opendata.cern.ch/docs/cms-guide-luminosity-calculation ?

##-- brilcalc lumi -r 320038            

"""

if(oneFile):
  CMS_files = [CMS_files[0]] # take first file of files list 

print("Number of input files:",len(CMS_files))

# Crab configuration parameters
from CRABClient.UserUtilities import config
config = config()

oneFileStr = ""
if(oneFile): oneFileStr = "_oneFile"

# requestName = '{DatasetLabel}_{ODD_PF_string}_{RecoMethod}_{WeightsWP}ODDweights{oneFileStr}'.format(DatasetLabel=DatasetLabel, ODD_PF_string=ODD_PF_string, RecoMethod=RecoMethod, WeightsWP=WeightsWP, oneFileStr=oneFileStr)
requestName = '{DatasetLabel}_{ECAL_Config}_{simECALTP_Tag}{oneFileStr}'.format(DatasetLabel=DatasetLabel, ECAL_Config=ECAL_Config, simECALTP_Tag=simECALTP_Tag, oneFileStr=oneFileStr)

config.General.requestName = requestName
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True # Need this True to transfer output files, at least with eos output.
config.General.transferLogs = True 

# cmssw configuration file parameters 
config.JobType.pyCfgParams = [
                                'OverrideWeights=%s'%(OverrideWeights), # whether or not to override weights from global tag 
                                'simECALTP=%s'%(simECALTP), # re-construct L1 objects using re-emulated ECAL TPs 
                                'TPModeSqliteFile=%s'%(TPMode_file), # strip zeroing, with or without ODD PF configs to try: [EcalTPG_TPMode_Run3_zeroingOddPeakFinder.db, EcalTPG_TPMode_Run3_zeroing,db]
                                'OddWeightsGroupSqliteFile=OneEBOneEEset_adding2021Strips.db', # weights group for each strip - defines which set of ODD weights each strip should use 
                                'TPModeTag=%s'%(TPMode_Tag), # TPMode, aka electronics configuration
                                'OddWeightsSqliteFile=%s'%(OddWeightsSqliteFile), # Working points to try: [MinDelta_2p5Prime_OddWeights, MinDelta_0p5Prime_OddWeights.db]
                             ] 
                             
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '%s/l1NtupleRAWEMU_2018_RAW2DIGI.py'%(inDir)

# Splitting
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

# Output directory / file naming
config.Data.outputPrimaryDataset = '%s%s'%(DatasetLabel, oneFileStr)
config.Data.outputDatasetTag = '{DatasetLabel}_{ECAL_Config}_{simECALTP_Tag}{oneFileStr}'.format(DatasetLabel=DatasetLabel, ECAL_Config=ECAL_Config, simECALTP_Tag=simECALTP_Tag, oneFileStr=oneFileStr)

config.Data.outLFNDirBase = '/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/L1_Rates_and_TurnOns/' 
config.Data.publication = False 

config.Data.userInputFiles = CMS_files 

config.Site.whitelist = ['T2_CH_CERN'] ##-- Eventually had to change from 'T2_FR_GRIF_LLR' whitelist to this 
config.Site.storageSite = 'T2_CH_CERN'

# input files 
config.JobType.inputFiles = [
                             # ODD weights working points
                             '%s/weights/output/MinDelta_2p5Prime_OddWeights.db'%(inDir),
                             '%s/weights/output/MinDelta_0p5Prime_OddWeights.db'%(inDir),

                             # TPModes
                             '%s/TPModes/output/EcalTPG_TPMode_Run3_zeroing.db'%(inDir),
                             '%s/TPModes/output/EcalTPG_TPMode_Run3_zeroingOddPeakFinder.db'%(inDir),
                             '%s/TPModes/output/EcalTPG_TPMode_Run2_default.db'%(inDir),

                             # Misc
                             '%s/weights/output/OneEBOneEEset_adding2021Strips.db'%(inDir), # OddWeightsGroup - defines odd weights to be used by each ECAL strip 
                             '%s/ConfigParams.py'%(inDir) # To define cmssw config options 
                             ]    