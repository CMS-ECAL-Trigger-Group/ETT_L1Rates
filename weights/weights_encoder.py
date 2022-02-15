''' 
2 February 2022 
Abraham Tishelman-Charny 

Simplified version of WRS encoding script to derive FENIX encoded weights. 

Original code by William Richard Smith (2019) here: https://gitlab.cern.ch/cms-ecal-dpg/ecall1algooptimization/-/blob/942db3e6cac733e9684a42e7d2b314572ed14129/PileupMC/weights_encoder.py

This script simulates the loss of precision in decimal weights given by the encoding. 
'''

import argparse
import numpy as np 
from matplotlib import pyplot as plt 

parser = argparse.ArgumentParser()
parser.add_argument("--DecimalWeights", type=str, required=True, help="Comma separated list of input decimal weights to encode.")
args = parser.parse_args()

DecimalWeights = [float(w_) for w_ in args.DecimalWeights.split(',')]
N_weights = len(DecimalWeights)
if(N_weights != 5):
    raise Exception("Number of weights must equal 5 - Exiting")

#Encoded weights back to decimals to look at differences
def encoded_to_decimal(enc_weights_not_corrected):
    back_weights = [0]*5
    for count, encw in enumerate(enc_weights_not_corrected):
        if encw > 63:
            encw = -(128 -encw)
        back_weights[count] = encw/64
    
    return back_weights

def decimal_to_encoded(weights):
    enc_weights_not_corrected = [0]*5
    for count, w in enumerate(weights):
        if w >0:
            encodedw = w*64
            encodedw = int(round(encodedw))
        elif w == 0:
            encodedw = 0
        else:
            encodedw = w*64
            encodedw = abs(encodedw)
            encodedw = int(round(encodedw))
            encodedw = 128 - encodedw

        enc_weights_not_corrected[count] = encodedw
            
    return enc_weights_not_corrected

# Scan a range of encoded values to see what decimal values you would get (seems slightly different from actual encoding for larger values)
def ScanValues(min, max):
    encoded_vals = []
    decimal_vals = []

    for i in range(min, max):
        weight = [int(i)]
        decimal = encoded_to_decimal(weight)
        print("Encoded, Decimal: %s, %s"%(weight[0], decimal[0])) 
        encoded_vals.append(weight[0])
        decimal_vals.append(decimal[0])

    fig, ax = plt.subplots()
    plt.plot(encoded_vals, decimal_vals)
    plt.savefig("weights.png")
    plt.close()

if (__name__ == '__main__'): 

    # Start with a set of decimal weights and obtain their encoded values 
    EncodedWeights = decimal_to_encoded(DecimalWeights)
    print("Decimal weights (ideally in steps of 1/64):",DecimalWeights)
    print("Sum of decimal weights:",np.sum(DecimalWeights)) 
    print("Encoded weights:",EncodedWeights)
    print("Sum of decimal weights:",np.sum(EncodedWeights)) 
    print("DONE")
