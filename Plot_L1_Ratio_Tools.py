"""
17 February 2022
Abraham Tishelman-Charny 

The purpose of this module is to provide functionality and tools for Plot_L1_Ratio. 
"""

# imports 
import argparse 

def GetArgs():
    # command line arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument("--ol", help = "Output location")
    parser.add_argument("--inDir", help = "Input directory with rate files")
    parser.add_argument("--error", action="store_true", help = "Plot error bars")
    parser.add_argument("--includeAll", action="store_true", help = "Plot all configs")
    args = parser.parse_args()

    arg_names = ["ol", "inDir", "error", "includeAll"]

    return args, arg_names 


def GetSeeds():
    seeds_ = [
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

    return seeds_ 

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