# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: l1NtupleRAWEMU_2018 -s RAW2DIGI --era=Run2_2018 --customise=L1Trigger/Configuration/customiseReEmul.L1TReEmulFromRAW --customise=L1Trigger/L1TNtuples/customiseL1Ntuple.L1NtupleRAWEMU --conditions=101X_dataRun2_HLT_v7 -n 200 --data --no_exec --no_output --filein=/store/data/Run2018C/ZeroBias/RAW/v1/000/320/040/00000/0C4F86A1-D78D-E811-BB76-FA163EBE2E0D.root
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018

from ConfigParams import ECAL_options 

process = cms.Process('RAW2DIGI',Run2_2018)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(200),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/data/Run2018C/ZeroBias/RAW/v1/000/320/040/00000/0C4F86A1-D78D-E811-BB76-FA163EBE2E0D.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('l1NtupleRAWEMU_2018 nevts:200'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag

process.GlobalTag = GlobalTag(process.GlobalTag, '101X_dataRun2_HLT_v7', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.endjob_step = cms.EndPath(process.endOfProcess)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.endjob_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Re-Emulate ECAL TPs, then re-construct L1 objects using those emulated ECAL TPs.
# This is used for testing different ECAL configurations 
if(ECAL_options.simECALTP):
    from L1Trigger.Configuration.customiseReEmul import L1TReEmulFromRAWsimEcalTP 
    process = L1TReEmulFromRAWsimEcalTP(process)    

# Re-construct L1 objects from data TPs
else:
    from L1Trigger.Configuration.customiseReEmul import L1TReEmulFromRAW 
    process = L1TReEmulFromRAW(process)

# Automatic addition of the customisation function from L1Trigger.L1TNtuples.customiseL1Ntuple
from L1Trigger.L1TNtuples.customiseL1Ntuple import L1NtupleRAWEMU 

#call to customisation function L1NtupleRAWEMU imported from L1Trigger.L1TNtuples.customiseL1Ntuple
process = L1NtupleRAWEMU(process)

# End of customisation functions

# Customisation from command line

# Set ECAL DB records if not contained in event setup with given global tag 
if(ECAL_options.OverrideWeights):
    print("Setting double weights records to user input values")
    process.load("CondCore.CondDB.CondDB_cfi")
    # input database (in this case the local sqlite file)

    process.EcalOnTheFlyTPGconf = cms.ESSource("PoolDBESSource",
        DumpStat=cms.untracked.bool(True),
        toGet = cms.VPSet(cms.PSet(
                                record = cms.string('EcalTPGOddWeightIdMapRcd'),
                                tag = cms.string("EcalTPGOddWeightIdMap_test"),
                                connect = cms.string('sqlite_file:%s'%(ECAL_options.OddWeightsSqliteFile))
                            ),
                        cms.PSet(
                                record = cms.string('EcalTPGOddWeightGroupRcd'),
                                tag = cms.string("EcalTPGOddWeightGroup_test"),
                                connect = cms.string('sqlite_file:%s'%(ECAL_options.OddWeightsGroupSqliteFile))
                            ),
                        cms.PSet(
                                record = cms.string('EcalTPGTPModeRcd'),
                                tag = cms.string(ECAL_options.TPModeTag),
                                connect = cms.string('sqlite_file:%s'%(ECAL_options.TPModeSqliteFile))
                            )
        ),
    )

    # in case they're necesssary 
    #process.es_prefer_tpmode = cms.ESPrefer("PoolDBESSource","EcalOnTheFlyTPGconf") # https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideHowToUseESPrefer
    #process.es_prefer_CaloParams = cms.ESPrefer("PoolDBESSource","l1conddb") # https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideHowToUseESPrefer

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
