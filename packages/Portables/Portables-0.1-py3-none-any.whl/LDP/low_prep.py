from sovaflow.utils import topomap
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import pandas as pd 
import os
from os import listdir
from os.path import isfile, join
from functions import (signal_upload,signal_filtering,periodogram,run_hpica,run_wicalp,reject,removeMuscle, noisy_channel)
from sovachronux.qeeg_psd_chronux import qeeg_psd_chronux
from time import time
import pingouin as pg
import numpy as np
from portables.LDP.pipeline_stages.linearFIR import filter_design, mfreqz
from portables.LDP.pipeline_stages.wavelet_filtering import wnoisest, wthresh, thselect
import pywt
from sovareject.tools import format_data
import mne
from mne.preprocessing import ICA
from sklearn.decomposition import FastICA
from sovaflow.flow import organize_channels, set_montage, standardize, run_reject
from sovawica.wica import removeStrongArtifacts_wden
import copy
from pyprep.find_noisy_channels import NoisyChannels
from mne.preprocessing import ICA
import pickle
 
#path = r'D:\portablesPP\Portables\EEG'
#path=r'D:\portablesPP\Portables_NoCTR002'
path=r'D:\portablesProyecto\EEG_PORTABLES'
#path=r'D:\portablesProyecto\prueba'
electrodes = ['FP2','FP1','C3','C4','P7','P8','O1','O2'] # Electrodes used in the recording
bands ={'Delta':(4,6),
    'Theta':(6,8.5),
        'Alpha-1':(8.5,10.5),
        'Alpha-2':(10.5,12.5),
        'Beta1':(12.5,18.5),
        'Beta2':(18.5,21),
        'Beta3':(21,30),
        'Gamma':(30,70)
        }
fs = 250 # Sampling frecuency
low_fre = 4 # Low cut frecuency
high_fre = 45 # High cut frecuency
num_logmars = 7 # Number of logmars evaluated



# Filters design
order, highpass = filter_design(fs, locutoff = low_fre, hicutoff = 0, revfilt = 1)
#mfreqz(highpass,1,order, fs/2)
order, lowpass = filter_design(fs, locutoff = 0, hicutoff = high_fre, revfilt = 0)
#mfreqz(lowpass,1,order, fs/2)

correct_montage=electrodes
montage_kind='standard_1005'
fun_names_map=standardize
info = mne.create_info(ch_names=electrodes, sfreq=fs, ch_types='eeg')
ica_method='infomax'
tareas = ['CE', 'DTAN', 'DTCT', 'DTF', 'DTS1', 'DTS7', 'DTV', 'ST1', 'ST2']

signals_task = {}

for subdir in os.listdir(path):
    #if subdir.startswith('OpenBCISession_Sub-CTR'):
    if subdir.startswith('sub-SAN'):
        # Construir la ruta completa a la carpeta del sujeto
        ruta_sujeto = os.path.join(path, subdir)
        ruta_sesion = os.path.join(ruta_sujeto, 'ses-V0')
        ruta_eeg = os.path.join(ruta_sesion, 'eeg')

        #partes_nombre = ruta_sujeto.split('_')
        #nombre_tarea = partes_nombre[6]
      
        #for archivo in os.listdir(ruta_sujeto):
        for archivo in os.listdir(ruta_eeg):
            try:
                if archivo.endswith('.txt'):

                    #ruta_archivo = os.path.join(ruta_sujeto, archivo)
                    #ruta_archivo = ruta_archivo.replace('\\', '/')  # Asegurarse de que la ruta tenga el formato correcto
                    partes_nombre = archivo.split('_')
                    nombre_tarea = partes_nombre[-2]
                    #nombre_tarea = partes_nombre[4]
                    # Cargar la señal utilizando tu función load_files
                    if nombre_tarea in tareas:
                        ruta_archivo = os.path.join(ruta_eeg, archivo)
                        ruta_archivo = ruta_archivo.replace('\\', '/')
                        signal_uploaded = signal_upload(ruta_archivo, PP=False)
                        filtered_signal=signal_filtering(signal_uploaded,highpass, lowpass,electrodes,fs, HP=False)
                        correct_montage = copy.deepcopy(correct_montage)
                        raw = filtered_signal.copy() #raw = read_raw(filename, preload=True)#mne_open(filename)
                        raw,correct_montage= organize_channels(raw,correct_montage,fun_names_map)
                        raw,montage = set_montage(raw,montage_kind)
    #
                        if correct_montage is not None:
                            assert correct_montage == set(raw.info['ch_names'])
    #
                        S,A,W,pca_mean,pre_whitener,_ = run_hpica(raw,4,ica_method,show=False,verbose=False)
                        sig,wica_info = run_wicalp(S,A,pca_mean,pre_whitener,raw.info['sfreq'],ica_method,raw.info['ch_names'],h_freq=50,epoch_length=5)
    #
                        epoch_signal,reject_info=reject(sig, mode='autorej',epoch_length=5)

                        raw = epoch_signal.copy() #raw = read_raw(filename, preload=True)#mne_open(filename)
                        raw,correct_montage= organize_channels(raw,correct_montage,fun_names_map)
                        raw,montage = set_montage(raw,montage_kind)
    #
                        if correct_montage is not None:
                            assert correct_montage == set(raw.info['ch_names'])
    #
                        reconst_raw=removeMuscle(raw, score=0.6,ica_method='infomax',verbose=False)
                        info_noisy=noisy_channel(reconst_raw)
    #
                        print(info_noisy)
    #
                        if nombre_tarea not in signals_task:
                            signals_task[nombre_tarea] = []
                            #freq[nombre_tarea] = []
                        signals_task[nombre_tarea].append(reconst_raw)
                        #freq[nombre_tarea].append(ffo)
                    #
#
            except:
                print("ERROR con senal: " + archivo)
                print(signal_uploaded.shape)


print(signals_task.keys())
for i in signals_task:
    print(len(signals_task[i]))
#ruta = r'D:\\OneDrive - Universidad de Antioquia\\Posgrado\\2024-1\\Reporte_piloto_DT'
ruta=r'D:\\portablesProyecto\\dataframes'
with open(os.path.join(ruta,'signals_task_SAN.pkl'), 'wb') as archivo:
    pickle.dump(signals_task, archivo)

#all_signals = {}
#all_spect={}
#all_freq={}
#
#for i in signals_task:
#    all_spect[i]=[]
#    all_signals[i]=[]
#    all_freq[i]=[]
#    for j in signals_task[i]:
#        pot,ss,ffo=periodogram(j, fs, bands,all=True)
#        all_spect[i].append(ss)
#        all_signals[i].append(pot)
#        all_freq[i].append(ffo)
#

#with open(os.path.join(ruta,'all_spect.pkl'), 'wb') as archivo:
#    pickle.dump(all_spect, archivo)
#
#with open(os.path.join(ruta,'all_freq.pkl'), 'wb') as archivo:
#    pickle.dump(all_freq, archivo)
#
#with open(os.path.join(ruta,'all_sig.pkl'), 'wb') as archivo:
#    pickle.dump(all_signals, archivo)




  