import mne
import pywt
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import pandas as pd 
from LDP.pipeline_stages.linearFIR import filter_design
from LDP.pipeline_stages.MyNoisyChannels import NoisyChannels
from sovachronux.qeeg_psd_chronux import qeeg_psd_chronux
from sovareject.tools import format_data
from sovawica.wica import removeStrongArtifacts_wden
from mne.preprocessing import ICA
from sovaflow.utils import topomap
from sklearn.decomposition import FastICA
from sovawica.wica import w_ica_matlab
from sovaflow.utils import createRaw
from sovaflow.flow import run_reject


def low_High_filter(fs=250,low_fre=4,high_fre=45,num_logmars=7):
  # Filters design
  order, highpass = filter_design(fs, locutoff = low_fre, hicutoff = 0, revfilt = 1)
  #mfreqz(highpass,1,order, fs/2)
  order, lowpass = filter_design(fs, locutoff = 0, hicutoff = high_fre, revfilt = 0)
  #mfreqz(lowpass,1,order, fs/2)
  return order, lowpass, highpass

def scalogram(signal, sampling_frequency, frequency_band, path):

  sampling_period =  1/sampling_frequency
  Frequency_Band = frequency_band #Corresponde a la banda de frecuencia a analizar [4, 13]

  # Métodos de obtener las escalas para el Complex Morlet Wavelet  
  # Método 1:
  # Determinar las frecuencias respectivas para una escalas definidas
  scales = np.arange(1, 250)
  frequencies = pywt.scale2frequency('cmor1.0-1.0', scales)/sampling_period
  # Extraer las escalas correspondientes a la banda de frecuencia a analizar
  scales = scales[np.where(frequencies >= Frequency_Band[0]) and np.where(frequencies <= Frequency_Band[1])] 

  points = signal.shape[0]

  #%%
  # Obtener el tiempo correspondiente a una epoca de la señal (en segundos)
  time_epoch = sampling_period*points

  # Analizar una epoca de un montaje (con las escalas del método 1)
  # Obtener el vector de tiempo adecuado para una epoca de un montaje de la señal
  time = np.arange(0, time_epoch, sampling_period)
  # Para la primera epoca del segundo montaje calcular la transformada continua de Wavelet, usando Complex Morlet Wavelet

  [coef, freqs] = pywt.cwt(signal, scales, 'cmor1.0-1.0', sampling_period)
  # Calcular la potencia 
  power = (np.abs(coef)) ** 2
  # Graficar el escalograma obtenido del análisis tiempo frecuencia
  f, ax = plt.subplots(figsize=(15, 10))
  scalogram = ax.contourf(time,
                  freqs,
                  power,
                  10, # Especificar 20 divisiones en las escalas de color 
                  extend='both')
  ax.set_ylim(np.amin(freqs), np.amax(freqs))
  ax.set_ylabel('frequency [Hz]')
  ax.set_xlabel('Time [s]')
  cbar = plt.colorbar(scalogram)

  # CAUTION! this code Always overwrites the plots
  
  #plt.savefig(path + '_spectrum.png')
  #plt.show()

def signal_upload(signal_path, PP=True):

  '''
  Function created to upload a signal from a csv file to the enviroment of 
  work, saving it in a pandas DataFrame and then in a numpy array. In this 
  function, to all the channels is substracted Fcz channel that works as 
  a reference. Then the raw signal is plotted.

  Input: signal_path --> str (path where the csv file is located with the data)

         subject --> str (code of identification of the subject)

         electrodes --> list (contains the names of the electrodes used in the recording)
         

  Output: vision_signal --> Numpy array (array with the uploaded signal)

          signals_marks --> Numpy array (array where the marks are located)
  '''
  if PP:
     
    signal=pd.read_csv(signal_path, skiprows=4,sep=',')
    signal.drop(['Sample Index',
                        ' Accel Channel 0',
                        ' Accel Channel 1',
                        ' Accel Channel 2',
                        ' Other', ' Other.1',
                        ' Other.2',' Other.3',
                        ' Other', ' Other.1',
                        ' Other.2', ' Other.3',
                        ' Other.4', ' Other.5',
                        ' Other.6', ' Analog Channel 0',
                        ' Analog Channel 1', ' Analog Channel 2',
                        ' Timestamp', ' Other.7',
                        ' Timestamp (Formatted)'],
                        axis=1,
                        inplace=True)
    
    signal = signal.to_numpy()[5:-5] #Quitando primeras y últimas 5 muestras por el pico al encender el open y el final del registro
    num_channels = signal.shape[1]

  else:
    signal=pd.read_csv(signal_path, skiprows=1,sep=',')
    signal = signal.to_numpy()[5:-5] #Quitando primeras y últimas 5 muestras por el pico al encender el open y el final del registro
    num_channels = signal.shape[1]

  return signal.T

def signal_filtering(uploaded_signal,highpass, lowpass,ch_names,sfreq,HP=False,filter_mne=False,L_FREQ=4,H_FREQ=50):

  '''
  Function that filters the signal. First, linear tendences are eliminated. Then,
  using designed linear filters (highpass and lowpass) the function defines
  a range of frecuencies. Last, using a non-linear filter (wavelet) the signal
  is filtrated again and plots the result.

  Inputs: uploaded_signal --> Numpy array (signal to be filtered)
          subject --> str (code of identification of the subject)
          electrodes --> list (contains the names of the electrodes used in the recording)
          highpass --> Numpy array (highpass filter)
          lowpass --> Numpy array (lowpass filter)
  Output: filtered signal --> Numpy array (resulting signal of the filtering process)
  '''

  detrend_signal = signal.detrend(uploaded_signal, axis=1, type='linear') # Delete linear trends
  num_channels,data = detrend_signal.shape
  
  if filter_mne:
      senal_w_hp=mne.filter.filter_data(detrend_signal,sfreq ,l_freq=L_FREQ,h_freq=None)
  else:
      senal_w_hp = signal.filtfilt(highpass, 1, detrend_signal, axis=1)
  

  epoch_sig,time=format_data(senal_w_hp, sfreq, 5)
  #sw=np.zeros((epoch_sig.shape[0],epoch_sig.shape[1],epoch_sig.shape[2]))
  components = np.array(list(range(epoch_sig.shape[0])))
  so,opt=removeStrongArtifacts_wden(epoch_sig,components,4,mode='sigma')
  sr=np.reshape(so,(so.shape[0],so.shape[1]*so.shape[2]),order='F')
  if filter_mne:
    lp_sig = mne.filter.filter_data(sr, sfreq ,l_freq=None,h_freq=H_FREQ)
  else:
    lp_sig = signal.filtfilt(lowpass, 1, sr,axis=1)
  
     
  # Crear la info del objeto MNE
  info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')
  # Crear un objeto RawArray
  filtered_signal = mne.io.RawArray(lp_sig, info)
  filtered_hp=mne.io.RawArray(senal_w_hp, info)
  if HP:
    return filtered_signal,filtered_hp
  else:
    return filtered_signal
  
def noisy_channel(raw,ransac=False, correlation_secs=1.0, correlation_threshold=0.2, frac_bad=0.1):
    #Find noisy channels
    noisy_detector=NoisyChannels(raw,do_detrend=False)
    noisy_detector.find_all_bads(ransac=ransac, correlation_secs= correlation_secs, correlation_threshold=correlation_threshold, frac_bad=frac_bad)
    info_noisy=noisy_detector.get_bads(as_dict=True)
    return(info_noisy)

def removeMuscle(raw, score=0.6, ica_method='infomax',verbose=True):

    #Using MNE ICA, muscle components are detected and eliminated the ones that has 0.6> probability 
    ica = ICA(random_state=97, n_components= len(raw.info['ch_names']) , method = ica_method, fit_params=dict(extended=True),verbose=verbose)
    ica.fit(raw)
    muscle_idx_auto, scores = ica.find_bads_muscle(raw)
    muscle = np.where(scores > score)[0].tolist()
    ica.exclude = muscle
    reconst_raw = raw.copy()
    ica.apply(reconst_raw)
    #return MNE reconstructed signal with muscle components eliminated
    return (reconst_raw,muscle)

def reject(sig, mode='autorej',epoch_length=int):

    signal_r,reject_info=run_reject(sig, mode='autorej',epoch_length=epoch_length)
    signal_data = signal_r.get_data()
    da_eeg_cont = np.concatenate(signal_data,axis=-1)

    info = mne.create_info(ch_names=signal_r.info['ch_names'], sfreq=signal_r.info['sfreq'], ch_types='eeg')
    epoch_signal=mne.io.RawArray(da_eeg_cont, info)

    return epoch_signal, reject_info
  
def run_hpica(raw,l_freq,ica_method,show,verbose=True):
    raw = raw.copy()
    #raw = raw.filter(l_freq,None,fir_design='firwin')
    pca_mean = None
    pre_whitener = None
        # ICA
    if ica_method == 'infomax' or ica_method == 'picard':
        ica = ICA(random_state=97, n_components= len(raw.info['ch_names']) , method = ica_method, fit_params=dict(extended=True),verbose=True)
    elif ica_method == 'fastica':
        ica = ICA(random_state=97, n_components=len(raw.info['ch_names']), method = ica_method,verbose=verbose)

    if ica_method == 'infomax' or ica_method == 'picard' or ica_method == 'fastica':
        raw.info['bads']=[]
        icafit = ica.fit(raw,verbose=verbose)
        A = np.dot(icafit.mixing_matrix_.T[:,:icafit.n_components_],icafit.pca_components_[:icafit.n_components_]).T # see ica.py _pick_sources() Notice @ is matrix multiplication and \ is skip line, also (AB).T = B.T A.T for comparison to get_components()
        W = np.dot(icafit.unmixing_matrix_,icafit.pca_components_[:icafit.n_components_]) # see ica.py _transform()
        S = icafit.get_sources(raw)
        pre_whitener = icafit.pre_whitener_
        pca_mean = icafit.pca_mean_
        S = S._data
        if show:
            fig = icafit.plot_components(cmap='seismic',show=show)
        else:
            fig = None
        """
        IS ALL HERE
        _n_pca_comp = self._check_n_pca_components(self.n_pca_components)
        n_ch, _ = data.shape
        # Mixing and unmixing should both be shape (self.n_components_, 2),
        # and we need to put these into the upper left part of larger mixing
        # and unmixing matrices of shape (n_ch, _n_pca_comp)
        pca_components = self.pca_components_[:_n_pca_comp]
        assert pca_components.shape == (_n_pca_comp, n_ch)
        assert self.unmixing_matrix_.shape == \
            self.mixing_matrix_.shape == \
            (self.n_components_,) * 2
        unmixing = np.eye(_n_pca_comp)
        unmixing[:self.n_components_, :self.n_components_] = \
            self.unmixing_matrix_
        unmixing = np.dot(unmixing, pca_components)

        mixing = np.eye(_n_pca_comp)
        mixing[:self.n_components_, :self.n_components_] = \
            self.mixing_matrix_
        mixing = pca_components.T @ mixing
        assert mixing.shape == unmixing.shape[::-1] == (n_ch, _n_pca_comp)

        # keep requested components plus residuals (if any)
        sel_keep = np.concatenate(
        (sel_keep, np.arange(self.n_components_, _n_pca_comp)))
        proj_mat = np.dot(mixing[:, sel_keep], unmixing[sel_keep, :])
        data = np.dot(proj_mat, data)
        """
    if ica_method == 'sklearn':
        transformer = FastICA(n_components=np.linalg.matrix_rank(raw._data),random_state=0)
        S = np.transpose(transformer.fit_transform(np.transpose(raw._data)))
        W = transformer.components_
        A = transformer.mixing_
        white = transformer.whitening_
        if show:
            fig = topomap(A,W,transformer.components_.shape[1],raw.info,cmap='seismic',show=show)
        else:
            fig = None
    return S,A,W,pca_mean,pre_whitener,fig

def run_wicalp(S,A,pca_mean,pre_whitener,s_freq,ica_method,ch_names,h_freq=50,epoch_length=5):
    # Epoch Segmentation
    sources_epoch,_ = format_data(S,s_freq,epoch_length) #segmentacion por epocas paper de Ximena: 2s , pacho 5s

    # wICA
    components = np.array(list(range(S.shape[0])))
    sources_wica,filtered_matrix= w_ica_matlab(sources_epoch,components)
    sources_wica = np.reshape(sources_wica,(S.shape[0],sources_wica.shape[1]*sources_wica.shape[2]),order='F')
    # Reconstruct the mixed signals (eeg channels)

    mixed = np.dot(A,sources_wica)
    
    if ica_method in ['infomax','fastica','picard']: #see ica.py _pick_sources()
        pca_mean = np.reshape(pca_mean,(1,pca_mean.shape[0]),order='F')
        mixed += np.transpose(pca_mean)
        mixed *= pre_whitener
    
    """
        if self.pca_mean_ is not None:
        data += self.pca_mean_[:, None]

    # restore scaling
    if self.noise_cov is None:  # revert standardization
        data *= self.pre_whitener_
    else:
        data = np.dot(linalg.pinv(self.pre_whitener_, cond=1e-14), data)

    return data
    """
    mixedMNE = createRaw(mixed,s_freq,'eeg',ch_names)
    #mixedMNE.filter(None,h_freq=h_freq,fir_design='firwin',picks='all')

    return mixedMNE,filtered_matrix

def periodogram(signal_filtered, sampling_frecuency, bands, epoch_length=2, all=False, channels=list, ep=True):
    '''
    Function to obtain the periodogram of each logmar for each signal using Multitaper
    technique.

    Inputs: 
        signal_filtered --> Numpy array (signal to be used to find the periodogram)
        sampling_frecuency --> int (sampling frecuency of the EEG recorder)
        bands --> Frequency bands 
        epoch_length --> Length of each epoch
        all --> Whether to return all values
        channels --> List of channels
        ep --> Whether to use epochs or not
    '''
    if ep == True:
        sources_epoch, _ = format_data(signal_filtered, sampling_frecuency, epoch_length)
        num_canales = sources_epoch.shape[0]
    elif ep==False:
        sources_epoch = signal_filtered
        num_canales = sources_epoch.shape[0]
    
    c_pot = {}
    c_spect = []
    c_frq = []
    
    for ch in range(num_canales):
        ss, ffo, pot = qeeg_psd_chronux(sources_epoch[ch,:,:], sampling_frecuency, bands, normalized=True, spectro=True)
        c_pot[channels[ch]] = pot 
        c_spect.append(ss) 
        c_frq.append(ffo) 

    if all:
        return c_pot, c_spect, c_frq
    else:
        return c_pot
