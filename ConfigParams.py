"""
16 August 2021
Abraham Tishelman-Charny

The purpose of this cmssw configuration file is to provide command line options for CMSSW configuration files 
"""

import FWCore.ParameterSet.VarParsing as VarParsing

##-- Options that can be set on the command line 
ECAL_options = VarParsing.VarParsing('analysis')

ECAL_options.register ('userMaxEvents',
                -1, # default value
                VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                VarParsing.VarParsing.varType.int,           # string, int, or float
                "userMaxEvents")
ECAL_options.register ('TPinfoPrintout',
                False, # default value
                VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                VarParsing.VarParsing.varType.bool,           # string, int, or float
                "TPinfoPrintout")
ECAL_options.register ('Debug',
                False, # default value
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.bool,          
                "Debug")   
ECAL_options.register ('BarrelOnly',
                # False, # default value
                True, # default value
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.bool,          
                "BarrelOnly")                                
ECAL_options.register ('TPModeSqliteFile',
                'EcalTPG_TPMode_Run3_zeroing.db',
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.string,          
                "TPModeSqliteFile")    
ECAL_options.register ('TPModeTag',
                'EcalTPG_TPMode_Run3_zeroing', # default value -- 0 = Run 2 
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.string,          
                "TPModeTag")  
ECAL_options.register ('OddWeightsSqliteFile',                                        
                'weights/output/MinDelta_2p5Prime_OddWeights.db', 
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.string,          
                "OddWeightsSqliteFile") 
ECAL_options.register ('OddWeightsGroupSqliteFile',                                        
                'weights/output/OneEBOneEEset.db', 
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.string,          
                "OddWeightsGroupSqliteFile")                 
ECAL_options.register ('RunETTAnalyzer', ##-- If true, produce output ntuple with ETTAnalyzer 
                True, # default value
                VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                VarParsing.VarParsing.varType.bool,           # string, int, or float
                "RunETTAnalyzer")     
ECAL_options.register ('inFile',                                        
                '', 
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.string,          
                "inFile")   
ECAL_options.register ('RecoMethod', ##-- Offline energy reconstruction method                               
                'weights', 
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.string,          
                "RecoMethod")                                               
##-- If using es_prefer to override odd weights records over global tag. If global tag does not contain TPG odd weight records, may need to do this 
ECAL_options.register ('OverrideWeights', 
                False, # default value
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.bool,           
                "OverrideWeights")    
# reconstruct L1 objects using emulated ECAL TPs 
ECAL_options.register ('simECALTP', 
                False, # default value
                VarParsing.VarParsing.multiplicity.singleton, 
                VarParsing.VarParsing.varType.bool,           
                "simECALTP")    

# ECAL_options.register ('UserGlobalTag', ##-- global tag                           
#                 '101X_dataRun2_HLT_v7', 
#                 VarParsing.VarParsing.multiplicity.singleton, 
#                 VarParsing.VarParsing.varType.string,          
#                 "UserGlobalTag") 


ECAL_options.parseArguments()