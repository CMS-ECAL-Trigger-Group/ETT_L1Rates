# FENIX weight encoding and SQLite File creation 

The purpose of this directory is to produce the FENIX integer encoded versions of decimal weights, and produce SQLite files in order to overwrite ODD weights that would be picked up from the DB. This 
is useful for re-emulating with a custom set of ODD weights that were not necessarily used at the time of data taking, and in particular for which a class which may 
not exist. 

## Weight encoding 

If one has decimal weights they would like to convert to integers (encoded version of weights to be read by the FENIX), one can use the python module `weights_encoder.py`, passing the decimal values (in steps of 1/64.) like so:

```
cd ETTAnalyzer/ETTAnalyzer/weights
cmsenv
python3 weights_encoder.py --DecimalWeights " -0.703125,0.0,-0.546875,0.984375,0.265625" # note that a space at the start of the string is necessary in order to avoid a negative value appearing to be a flag 
```

This will take a set of ODD amplitude weights output from the [Numerical Optimization](https://github.com/CMS-ECAL-Trigger-Group/DoubleWeightsOptimization) which have been converted to intervals of 1/64 (FENIX decimal precision), in this case the 5 values passed by the `DecimalWeights` option, and will return the encoded integer values to be passed to the FENIX and used for re-emulation with a custom ODD weights set. 

## Creating a TPGOddWeightIdMap SQLite file (weight values to be used by stips)

To create a map from weight ID to encoded weight values, one should input a text file with one row per weight group into `updateTPGOddWeightIdMap.py`, which should output an SQLite file. An example usage would be using the text file `input/MinDelta_2p5Prime_OddWeights.txt`, takes weight values from the encoding step above:

```
cd ETTAnalyzer/ETTAnalyzer/weights
cmsRun updateTPGOddWeightIdMap.py input=input/MinDelta_2p5_OddWeights.txt output=output/MinDelta_2p5_OddWeights.db
```

If this works properly, you should have an output SQLite file `output/test.db`. The following are some miscellanous commands that can be used for inpsecting this SQLite file with `sqlite3` (available currently on lxplus):

```
sqlite3 
.open output/MinDelta_2p5_OddWeights.db
.tables
SELECT * FROM 'IOV';
SELECT * FROM 'PAYLOAD';
SELECT * FROM 'TAG';
SELECT * FROM 'TAG_LOG';
```

And to see the encoded weight values (formatted in some particular way, but they are in there) go to this [web browser SQLite viewer](https://inloop.github.io/sqlite-viewer/), drop your .db file onto the page and try the following (because I can't figure out how to do this with sqlite3):

```
SELECT DATA FROM 'PAYLOAD';
```

## Creating a TPGOddWeightGroup SQLite file (weight groups assigned to each strip)

The purpose of creating a TPGOddWeightGroup SQLite file is to assign weight group IDs for each ECAL strip. Strip IDs come from the `stripid` column of the following DOF (Degree of freedom) files: [EB](https://gitlab.cern.ch/cms-ecal-dpg/ecall1algooptimization/-/blob/master/PileupMC/parameters/DOF_EB_2018.csv), [EE](https://gitlab.cern.ch/cms-ecal-dpg/ecall1algooptimization/-/blob/master/PileupMC/parameters/DOF_EE_2018.csv). (at least for EE...to be confirmed for EB).

One can use the script `GetStripIDs.py` to output a text file with a pairing of EB/EE strip to weight group. One has already been produced and placed in `input/OneEBOneEEset.txt`, corresponding to one set of weights for EB and one for EE. EB strips are assigned group 0 aka row 0 from the above produced `output/MinDelta_2p5_OddWeights.db`, and group 1, aka row 1 from `output/MinDelta_2p5_OddWeights.db` is assigned to EE strips. One can produce the corresponding SQLite file from this text file using (the file is already in the `output` direc by default but you can create it for yourself here):

```
cmsRun updateTPGOddWeightGroup.py input=input/OneEBOneEEset.txt output=output/OneEBOneEEset.db
```

If this works properly, the OddWeightGroup SQLite file should be placed at `output/OneEBOneEEset.db`. 

## Notes 

With the above two files, one can then create custom weight groups and ID maps. For example, creating more granular ODD weights sets, such as a specific set of ODD weights per strip. This can be useful if one has strip by strip optimized ODD weights. 
