from sovaflow.utils import topomap
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import pandas as pd 
import os
from os import listdir
from os.path import isfile, join
from functions import (signal_upload,signal_filtering,periodogram,run_hpica,run_wicalp,reject,removeMuscle, noisy_channel)
from Utils.quality_metrics import calculate_oha, calculate_thv,add_results
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
from sovaflow.utils import createRaw
 
electrodes = ['FP1','FP2','C3','C4','P7','P8','O1','O2'] # Electrodes used in the recording
bands ={'Delta':(4,6),
    'Theta':(6,8.5),
        'Alpha-1':(8.5,10.5),
        'Alpha-2':(10.5,12.5),
        'Beta1':(12.5,18.5),
        'Beta2':(18.5,21),
        'Beta3':(21,30),
        'Gamma':(30,70)
        }
fs = 250# Sampling frecuency
low_fre = 4 # Low cut frecuency
high_fre = 50 # High cut frecuency
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

#PATH="F:\BIOMARCADORES\sub-CTR021\ses-V0\eeg\sub-CTR021_ses-V0_task-CE_eeg.vhdr"
ruta_archivo=r"C:\Users\Luisa\OneDrive - Universidad de Antioquia\Datos EEG Portables\EEG\OpenBCISession_Sub-CTR001_ses_V0_task_CE_eeg\OpenBCI-RAW-2023-10-23_11-04-32.txt"
#signal_uploaded= mne.io.read_raw(PATH)
signal_uploaded = signal_upload(ruta_archivo, PP=True)
signal_uploaded=createRaw(signal_uploaded,fs,'eeg',electrodes)
signal_uploaded,correct_montage= organize_channels(signal_uploaded,correct_montage,fun_names_map)
signal_uploaded,montage = set_montage(signal_uploaded,montage_kind)

if correct_montage is not None:
    assert correct_montage == set(signal_uploaded.info['ch_names'])
    
signal_uploaded.pick_channels(ch_names=electrodes)
signal_uploaded.resample(fs, npad='auto', verbose='error')

#filtered_signal=signal_filtering(signal_uploaded,highpass, lowpass,electrodes,fs, HP=False)
filtered_signal=signal_filtering(signal_uploaded.get_data(),highpass, lowpass,signal_uploaded.info['ch_names'],fs, HP=False,filter_mne=True,L_FREQ=4,H_FREQ=50)
S,A,W,pca_mean,pre_whitener,_ = run_hpica(filtered_signal,None,ica_method,show=False,verbose=False)
sig,wica_info = run_wicalp(S,A,pca_mean,pre_whitener,filtered_signal.info['sfreq'],ica_method,filtered_signal.info['ch_names'],h_freq=50,epoch_length=5)


epoch_signal,reject_info=reject(sig, mode='autorej',epoch_length=5)

raw = epoch_signal.copy()
raw,correct_montage= organize_channels(raw,correct_montage,fun_names_map)
raw,montage = set_montage(raw,montage_kind)

if correct_montage is not None:
    assert correct_montage == set(raw.info['ch_names'])

reconst_raw=removeMuscle(raw, score=0.6,ica_method='infomax',verbose=False)
info_noisy=noisy_channel(reconst_raw)
print(info_noisy)

thresholds = [10, 20, 30, 50, 60, 70]  # Thresholds in µV

if all(v is not None for v in [signal_uploaded, filtered_signal, sig, epoch_signal, reconst_raw]):
    # Crear un DataFrame unificado para almacenar todos los resultados
    all_results_df = pd.DataFrame()
    
    # Agregar resultados para cada condición
    conditions = {
        'RAW': signal_uploaded,
        'WAVELET': filtered_signal,
        'WICA': sig,
        'EPOCH REJECT': epoch_signal,
        'Remove Noisy Muscular': reconst_raw
    }
    
    for condition, raw_data in conditions.items():
        results = add_results(condition, raw_data, thresholds)
        df = pd.DataFrame(results)
        all_results_df = pd.concat([all_results_df, df], ignore_index=True)
    
    # Imprimir el DataFrame unificado
    print(all_results_df)
    
    # Configuración de subplots para OHA
    unique_channels = all_results_df['Channel'].unique()
    n_channels = len(unique_channels)
    fig_oha, axes_oha = plt.subplots(2, 4, figsize=(20, 10), sharex=True, sharey=True)
    fig_oha.suptitle('OHA by Channel and Condition', fontsize=16)
    
    for idx, channel in enumerate(unique_channels):
        row, col = divmod(idx, 4)
        channel_data = all_results_df[all_results_df['Channel'] == channel]
        
        sns.lineplot(data=channel_data, x='Threshold', y='OHA', hue='Condition', style='Condition', markers=True, dashes=False, ax=axes_oha[row, col])
        axes_oha[row, col].set_title(f'Channel {channel}')
        axes_oha[row, col].legend(loc='upper right', fontsize='small')
        axes_oha[row, col].set_xlabel('Threshold (µV)')
        axes_oha[row, col].set_ylabel('OHA')
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()
    
    # Configuración de subplots para THV
    fig_thv, axes_thv = plt.subplots(2, 4, figsize=(20, 10), sharex=True, sharey=True)
    fig_thv.suptitle('THV by Channel and Condition', fontsize=16)
    
    for idx, channel in enumerate(unique_channels):
        row, col = divmod(idx, 4)
        channel_data = all_results_df[all_results_df['Channel'] == channel]
        
        sns.lineplot(data=channel_data, x='Threshold', y='THV', hue='Condition', style='Condition', markers=True, dashes=False, ax=axes_thv[row, col])
        axes_thv[row, col].set_title(f'Channel {channel}')
        axes_thv[row, col].legend(loc='upper right', fontsize='small')
        axes_thv[row, col].set_xlabel('Threshold (µV)')
        axes_thv[row, col].set_ylabel('THV')
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()
else:
    print("Error: Asegúrate de que todas las variables contienen datos válidos.")

pot,ss,ffo=periodogram(signal_uploaded.get_data(), signal_uploaded.info['sfreq'], bands,all=True)
pot_wav,ss_wav,ffo_wav=periodogram(filtered_signal.get_data(), filtered_signal.info['sfreq'], bands,all=True)
pot_wica,ss_wica,ffo_wica=periodogram(sig.get_data(), sig.info['sfreq'], bands,all=True)
pot_reject,ss_reject,ffo_reject=periodogram(epoch_signal.get_data(), epoch_signal.info['sfreq'], bands,all=True)
pot_dm,ss_dm,ffo_dm=periodogram(reconst_raw.get_data(), reconst_raw.info['sfreq'], bands,all=True)

print(signal_uploaded.info['ch_names'])
print(filtered_signal.info['ch_names'])
print(sig.info['ch_names'])
print(epoch_signal.info['ch_names'])
print(reconst_raw.info['ch_names'])

num_rows=4
fig, axs = plt.subplots(num_rows, 2, figsize=(15, 2*num_rows))
row_index=0
for i,ch in enumerate(sorted(signal_uploaded.info.ch_names)):
    row = row_index // 2  # Determina la fila del subplot
    col = row_index % 2
    axs[row,col].plot(signal_uploaded.get_data()[i,:],label='raw')
    axs[row,col].plot(filtered_signal.get_data()[i,:],label='wavelet')
    axs[row,col].plot(sig.get_data()[i,:],label='wica')
    axs[row,col].plot(raw.get_data()[i,:],label='reject')
    axs[row,col].plot(reconst_raw.get_data()[i,:],label='Muscle')
    axs[row, col].legend()
    row_index += 1
    axs[row, col].set_title(ch) 
plt.tight_layout()
plt.show()

num_rows=4
fig1, axs1 = plt.subplots(num_rows, 2, figsize=(15, 2*num_rows))
row_index=0
for i,ch in enumerate(signal_uploaded.info.ch_names):
    row = row_index // 2  # Determina la fila del subplot
    col = row_index % 2
    axs1[row,col].plot(ffo[i],ss[i],label='raw')
    axs1[row,col].plot(ffo_wav[i],ss_wav[i],label='wavelet')
    axs1[row,col].plot(ffo_wica[i],ss_wica[i],label='wica')
    axs1[row,col].plot(ffo_reject[i],ss_reject[i],label='reject')
    axs1[row,col].plot(ffo_dm[i],ss_dm[i],label='Muscle')
    axs1[row, col].legend()
    row_index += 1
    axs1[row, col].set_title(ch) 
plt.tight_layout()
plt.show()
print('done')