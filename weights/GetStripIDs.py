"""
4 February 2022 
Abraham Tishelman-Charny 

The purpose of this module is to get column stripID values from DOF csv files.

Example usage:
python3 GetStripIDs.py 
"""

import pandas as pd

def AppendStripIDs(f_):
    stripIDs_ = []
    df = pd.read_csv(f_)
    AllstripIDs = df["stripid"]
    for stripID in AllstripIDs:
        if(stripID not in stripIDs_):
            stripIDs_.append(stripID)

    return stripIDs_

if(__name__ == '__main__'):

    d = '/afs/cern.ch/work/a/atishelm/private/ecall1algooptimization/PileupMC/parameters/'
    EE_f = '{d}/DOF_EE_2018.csv'.format(d=d)
    EB_f = '{d}/DOF_EB_2018.csv'.format(d=d)

    EB_stripIDs = AppendStripIDs(EB_f)
    EE_stripIDs = AppendStripIDs(EE_f)

    print("len(EB_stripIDs):",len(EB_stripIDs))
    print("len(EE_stripIDs):",len(EE_stripIDs))

    outName = "OneEBOneEEset.txt"

    with open(outName, 'w') as f:
        for EB_stripID in EB_stripIDs:
            line = "{EB_stripID}\t0\n".format(EB_stripID=EB_stripID) # assign EB strips weight group 0 
            f.write(line)
        for EE_stripID in EE_stripIDs: 
            line = "{EE_stripID}\t1\n".format(EE_stripID=EE_stripID) # assign EE strips weight group 1 
            f.write(line)            
        
    f.close()
    print("Wrote output file:",outName)