# -*- coding: utf-8 -*-

import argparse
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import csv
    
if __name__ == "__main__":  
       
#    fragment = '../traditional_dataset/density/fragments/density_first_fragment_zoon'

    parser = argparse.ArgumentParser(description="Synthesize pitch sequence.")
    parser.add_argument("inputfile", help="Path to input file for slicing")

    args = parser.parse_args()
    if args.inputfile is not None:    
    
        audio_file = args.inputfile 
        gt_file = args.inputfile[:-9]  + '.csv'
        
        fs, audio = wav.read(audio_file)
        t = np.arange(len(audio)) * (1/44100.0)
    
        cr = csv.reader(open(gt_file,"rb"))
        onset=[]
        notes=[]
        for row in cr:
            onset.append(row[0]) 
            notes.append(row[1])
        onset = np.array(onset, 'float32')
        i=0
        aux_vad_gt = np.empty([0,])
        for note in notes:
            if note=='0':
                aux_vad_gt = np.r_[aux_vad_gt,0]
            else:
                aux_vad_gt = np.r_[aux_vad_gt,1]
            i=i+1
        j=0
        vad_gt = np.empty([len(t),], 'float32')
        for i in range(1,len(onset)):
            while (j<len(t) and t[j]>=onset[i-1] and t[j]<=onset[i]):
                vad_gt[j]=aux_vad_gt[i-1]
                j=j+1
                
        silence = audio[np.where(vad_gt==0)]
        activity = audio[np.where(vad_gt==1)]
    #    plt.subplot(2,1,1)    
    #    plt.plot(audio)
    #    plt.grid()    
    #    plt.subplot(2,1,2)    
    #    plt.plot(silence)
    #    plt.grid()
        
        output_silence = args.inputfile[:-9] + '_silence.wav'
        output_activity = args.inputfile[:-9] + '_activity.wav'
        wav.write(output_silence, fs, silence)
        wav.write(output_activity, fs, activity)