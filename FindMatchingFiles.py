"""
18 February 2022
Abraham Tishelman-Charny 

The purpose of this script is to find the common file names between directories in order to compare rates assuring the same events are used. 
"""

import os 

d_main = "/eos/cms/store/group/dpg_ecal/alca_ecalcalib/Trigger/DoubleWeights/L1_Rates_and_TurnOns/Run_324725/"
d_1 = "Run_324725_Run2_NosimECALTP/220217_204339/all/"
d_2 = "Run_324725_Run2_simECALTP/220217_204856/all/"
d_3 = "Run_324725_StripZeroing_simECALTP/220217_205223/all/"

files_1 = os.listdir("%s/%s"%(d_main, d_1))
files_2 = os.listdir("%s/%s"%(d_main, d_2))
files_3 = os.listdir("%s/%s"%(d_main, d_3))

#print("files_1:",files_1)
common_files = []
for file in files_1:
    if((file in files_2) and (file in files_3)):
        common_files.append(file)

print("common_files:",common_files)
print("len(files_1):",len(files_1))
print("len(files_2):",len(files_2))
print("len(files_3):",len(files_3))
print("len(common_files):",len(common_files))