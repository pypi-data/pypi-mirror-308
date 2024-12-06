import sys
import os
import mne
import numpy as np
import re
import copy
from sovaflow.flow import organize_channels,standardize, set_montage
from sovaharmony.metrics.features import _get_power, _get_sl,_get_coh, _get_pme,_get_entropy,_get_psd
from sovaharmony.preprocessing import write_json
from sovaflow.flow import fit_spatial_filter
from sovaharmony.spatial import get_spatial_filter
from sovaharmony.preprocessing import get_derivative_path
from bids import BIDSLayout
from sovaflow.utils import cfg_logger
from sovareject.tools import format_data
from sovaharmony.utils import _verify_epoch_continuous,_verify_epochs_axes
import matplotlib.pyplot as plt
import pandas as pd
from bids.layout import parse_file_entities
from scipy import stats
from astropy.stats import mad_std
import statsmodels.api as sm


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DATASET import *



foo_map={
    'absPower':_get_power,
    'power':_get_power,
    'power_osc':_get_power,
    'power_ape':_get_power,
    'sl':_get_sl,
    'cohfreq':_get_coh,
    'crossfreq':_get_pme,
    'entropy':_get_entropy,
    'psd': _get_psd
}

def report_epochs(
    THE_DATASET = dict,
    epoch= 5,
    score_muscle = 0.7,
    correlation_threshold = 0.2,
    frac_bad = 0.05,
    
):
    
    input_path = THE_DATASET.get('input_path',None)
    layout_dict = THE_DATASET.get('layout',None)
    layout = BIDSLayout(input_path)
    bids_root = layout.root
    eegs = layout.get(**layout_dict)
    pipeline = 'APPLEE'
    derivatives_root = os.path.join(layout.root,'derivatives',pipeline)
    log_path = os.path.join(derivatives_root,'code')
    os.makedirs(log_path, exist_ok=True)
    logger,currentdt = cfg_logger(log_path)
    num_files = len(eegs)
    default_channels = ['AF3',	'AF4',	'C1',	'C2',	'C3',	'C4',	'C5',	'C6',	'CP1',	'CP2',	'CP3',	'CP4',	'CP5',	'CP6',	'CPZ',	'CZ',	'F1',	'F2',	'F3',	'F4',	'F5',	'F6',	'F7',	'F8',	'FC1',	'FC2',	'FC3',	'FC4',	'FC5',	'FC6',	'FP1',	'FP2',	'FZ',	'O1',	'O2',	'OZ',	'P1',	'P2',	'P3',	'P4',	'P5',	'P6',	'P7',	'P8',	'PO3',	'PO4',	'PO7',	'PO8',	'POZ',	'PZ','T5','T6'	,'T7',	'T8',	'TP7',	'TP8'] #Yorguin
    channels = THE_DATASET.get('channels',default_channels)
    task=THE_DATASET.get('layout')['task']
    name_bd = THE_DATASET.get('name')
    # Get all combinations of the parameters
    info_feature=[]
    for i,eeg_file in enumerate(eegs):     
        #process=str(i)+'/'+str(num_files)
        msg =f"File {i+1} of {num_files} ({(i+1)*100/num_files}%) : {eeg_file}"
        logger.info(msg)
        
        param_id = f'sm{score_muscle}_ct{correlation_threshold}_fb{frac_bad}'
        DM_path = get_derivative_path(layout,eeg_file,f'Muscle_{param_id}','eeg','.fif',bids_root,derivatives_root)
        qc_root = os.path.join(layout.root,'derivatives', 'QC.xlsx')
        QC=pd.read_excel(qc_root,sheet_name=f'sm0.7_ct0.2_fb0.05_{task}')
        try: 
            signal_DM = mne.io.read_raw(DM_path)
            data = signal_DM.get_data()
            sources_epoch, _ = format_data(data, signal_DM.info['sfreq'], epoch)
            num_canales = sources_epoch.shape[0]
            (c, s, t) = sources_epoch.shape
            signal_epochs = mne.make_fixed_length_epochs(signal_DM,duration=s/signal_DM.info['sfreq'],reject_by_annotation=False,preload=True)
            (c, s, t) = signal_epochs.shape
            QC['sfreq'] = signal_DM.info['sfreq']
            QC['epochs'] = s
        except:
            print(f'siganl {DM_path} no existe')

def get_derivative_ld(in_signal,feature,kwargs,spatial_filter=None):
    signal = in_signal.copy()
    if spatial_filter is not None:
        A,W,spatial_filter_chs,sf_name = spatial_filter['A'],spatial_filter['W'],spatial_filter['ch_names'],spatial_filter['name']
        intersection_chs = list(set(spatial_filter_chs).intersection(signal.ch_names))
        W_adapted = fit_spatial_filter(W,spatial_filter_chs,intersection_chs,mode='demixing')
        signal.reorder_channels(intersection_chs)
        signal_data = signal.get_data() 
        nchans, points = signal_data.shape
        ics = W_adapted @ signal_data
        comps = ics.shape[0]
        ics_data = np.reshape(ics,(comps,points),order='F')
        info_ics=mne.create_info(spatial_filter['labels'], in_signal.info['sfreq'], ch_types='eeg')
        signal = mne.io.RawArray(ics_data,info_ics)
              
    else:
        output=foo_map[feature](signal,**kwargs)
        output['metadata']['space']='sensors'
    return output



def get_metrics(THE_DATASET=dict,
                bands=dict,
                path=str,
                score_muscle = 0.7,
                correlation_threshold = 0.2,
                frac_bad = 0.05,
                path_demographics = None,
                def_spatial_filter= None,
                portables = True,
                montage_select='openBCI',
                feature=None,
                kwargs=dict,
                electrodes= list,
                epoch=5,
                norm= False,
                z_score= False,
                huber= False,
                fir=False
                ):
    '''
    Calculate metrics for the given dataset.
    
    Parameters:
        - THE_DATASET (dict): The dataset to calculate metrics on.
        - electrodes (list): List of electrodes.
        - bands (dict): Dictionary of bands.
        - path (str): Path to save the metrics.
        - score_muscle (float): Score for muscle.
        - correlation_threshold (float): Correlation threshold.
        - frac_bad (float): Fraction of bad data.
        - scale (str): Scale of the data.
        - path_demographics (str): Path to demographics data.
        - def_spatial_filter (str): Default spatial filter.
        - portables (bool): Whether the data is portable.
        - montage_select (str): Montage selection.
        - feature (str): Feature to calculate metrics on.
        - kwargs (dict): Additional keyword arguments.
    
    Returns:
        - None
                
    '''
    
    if THE_DATASET.get('spatial_filter',def_spatial_filter):
        spatial_filter = get_spatial_filter(THE_DATASET.get('spatial_filter',def_spatial_filter),portables=portables,montage_select=montage_select)
    else:
        spatial_filter = None
    OVERWRITE=False
    input_path = THE_DATASET.get('input_path',None)
    layout_dict = THE_DATASET.get('layout',None)
    e = 0
    archivosconerror = []
    # Static Params
    pipelabel = '['+THE_DATASET.get('run-label', '')+']'
    layout = BIDSLayout(input_path)
    bids_root = layout.root
    eegs = layout.get(**layout_dict)
    pipeline = 'APPLEE'
    derivatives_root = os.path.join(layout.root,'derivatives',pipeline)
    log_path = os.path.join(derivatives_root,'code')
    os.makedirs(log_path, exist_ok=True)
    logger,currentdt = cfg_logger(log_path)
    num_files = len(eegs)
    default_channels = ['AF3',	'AF4',	'C1',	'C2',	'C3',	'C4',	'C5',	'C6',	'CP1',	'CP2',	'CP3',	'CP4',	'CP5',	'CP6',	'CPZ',	'CZ',	'F1',	'F2',	'F3',	'F4',	'F5',	'F6',	'F7',	'F8',	'FC1',	'FC2',	'FC3',	'FC4',	'FC5',	'FC6',	'FP1',	'FP2',	'FZ',	'O1',	'O2',	'OZ',	'P1',	'P2',	'P3',	'P4',	'P5',	'P6',	'P7',	'P8',	'PO3',	'PO4',	'PO7',	'PO8',	'POZ',	'PZ','T5','T6'	,'T7',	'T8',	'TP7',	'TP8'] #Yorguin
    channels = THE_DATASET.get('channels',default_channels)
    task=THE_DATASET.get('layout')['task']
    name_bd = THE_DATASET.get('name')
    # Get all combinations of the parameters
    info_feature=[]
    for i,eeg_file in enumerate(eegs):     
        #process=str(i)+'/'+str(num_files)
        msg =f"File {i+1} of {num_files} ({(i+1)*100/num_files}%) : {eeg_file}"
        logger.info(msg)
        
        param_id = f'sm{score_muscle}_ct{correlation_threshold}_fb{frac_bad}'
        if fir:
            DM_path = get_derivative_path(layout,eeg_file,f'reject_fir','eeg','.fif',bids_root,derivatives_root)
        else:

            DM_path = get_derivative_path(layout,eeg_file,f'Muscle_{param_id}','eeg','.fif',bids_root,derivatives_root)
        #qc_root = os.path.join(layout.root,'derivatives', 'QC.xlsx')
        #QC=pd.read_excel(qc_root,sheet_name=f'sm0.7_ct0.2_fb0.05_{task}')
        info_bids_sujeto = parse_file_entities(eeg_file)
        try: 
            signal_DM = mne.io.read_raw(DM_path)
            if def_spatial_filter is not None:
                signal_DM = get_derivative_ld(signal_DM,spatial_filter =spatial_filter) # corregir
            else:   
                signal_DM.pick(electrodes)
                
                if norm:
                    if z_score:
                        data = stats.zscore(signal_DM.get_data(),axis=1)
                        signal_copy =  mne.io.RawArray(data, signal_DM.info)
                    elif huber:
                        signal2 = signal_DM.copy()
                        signal_DM.load_data()
                        signal_lp = signal_DM.filter(None,20,fir_design='firwin')
                        std_ch = []
                        for ch in signal_lp._data:
                            std_ch.append(mad_std(ch))
                        huber = sm.robust.scale.Huber() 
                        k = huber(np.array(std_ch))[0] # o np.median(np.array(std_ch)) o np.mean(np.array(std_ch))
                        data=signal2.get_data()/k
                        signal_copy =  mne.io.RawArray(data, signal_lp.info)
                else:
                    data = signal_DM.get_data()
                    signal_copy =  signal_DM.copy()
                
                sources_epoch, _ = format_data(data, signal_DM.info['sfreq'], epoch)
                num_canales = sources_epoch.shape[0]
                (c, s, t) = sources_epoch.shape
                signal_epochs = mne.make_fixed_length_epochs(signal_copy,duration=s/signal_copy.info['sfreq'],reject_by_annotation=False,preload=True)    
                values = get_derivative_ld(signal_epochs,feature,kwargs,spatial_filter=None)
                bandas = values['metadata']['axes']['bands']
                key_prefixes = ['spaces', 'spaces1', 'spaces2']
                for key_prefix in key_prefixes:
                    if key_prefix in values['metadata']['axes'].keys():
                        sensors = values['metadata']['axes'][key_prefix]
                
                regex = re.search('(.+).{3}',info_bids_sujeto['subject'])
                metric_values = np.array(values['values'])
                group = THE_DATASET.get('group_regex')
                if values['metadata']['type']!= 'crossfreq' and values['metadata']['type']!= 'psd' :
                    info_feature.extend([{
                        'subject': 'sub-' + info_bids_sujeto['subject'],
                        'Sensors': sensor,  
                        feature: np.mean(metric_values[b][s]) if values['metadata']['type'] in ['sl', 'coherence-bands'] else metric_values[b][s],   # Aquí se usan los índices s y b
                        'Band': band,
                        'Task': info_bids_sujeto['task'],
                        'group':'HC' if group is None else regex.string[regex.regs[-1][0]:regex.regs[-1][1]],
                        'center':name_bd
                    } for s, sensor in enumerate(sensors) for b, band in enumerate(bands)])
                
                elif values['metadata']['type']== 'psd':
                    freqs = np.array(values['freqs'])
                    info_feature.extend([
                    {'subject': 'sub-'+ info_bids_sujeto['subject'], 
                        'Sensors': sensor, 
                        'freqs': freqs[s], 
                        'psd': metric_values[s],
                        'group':'HC' if group is None else regex.string[regex.regs[-1][0]:regex.regs[-1][1]],
                        'Task': info_bids_sujeto['task'],
                        'center':name_bd
                        }
                    for s, sensor in enumerate(sensors)])
                    
                else:
                    info_feature.extend([{
                    'subject': 'sub-' + info_bids_sujeto['subject'],
                    'Sensors': sensor,  
                    feature: metric_values[s][b][b1],   # Aquí se usan los índices s y b
                    'Band': band,
                    'Mband': f'M{band1}',
                    'Task': info_bids_sujeto['task'],
                    'group':'HC' if group is None else regex.string[regex.regs[-1][0]:regex.regs[-1][1]],
                    'center':name_bd
                } for s, sensor in enumerate(sensors) for b, band in enumerate(bands) for b1,band1 in enumerate(bands)])  
        except:
            print(f'File not found: {DM_path}')
    
    df_metric_long=pd.DataFrame(info_feature)
    if values['metadata']['type']== 'crossfreq':
        df_metric_long = df_metric_long.loc[df_metric_long['crossfreq'] != 0]
    print(df_metric_long)
    df_values_copy = df_metric_long.copy()
    name_bd = THE_DATASET.get('name') 

    if values['metadata']['type']!= 'crossfreq'  and values['metadata']['type']!= 'psd':

        df_values_copy['Sensors_Band'] = df_values_copy['Sensors'] + '_' + df_values_copy['Band']

        # Pivotar el DataFrame copiado para que las columnas sean 'Sensors_Band'
        df_metric_column = df_values_copy.pivot_table(index=['subject', 'Task', 'group'], columns='Sensors_Band', values=feature)

        # Restablecer el índice si lo deseas para tener un DataFrame más plano
        df_metric_column = df_metric_column.reset_index()
        df_metric_column.columns.name = None
            
        df_metric_column=df_metric_column.assign(center=name_bd)
        print(df_metric_column)

    elif values['metadata']['type']== 'crossfreq':
        
        df_values_copy['Sensors_Band_Mband'] = df_values_copy['Sensors'] + '_' + df_values_copy['Band'] + '-' + df_values_copy['Mband']
        df_metric_column = df_values_copy.pivot_table(index=['subject', 'Task', 'group'], columns='Sensors_Band_Mband', values=feature)

        df_metric_column = df_metric_column.reset_index()
        df_metric_column.columns.name = None
            
        df_metric_column=df_metric_column.assign(center=name_bd)
        print(df_metric_column)
                
    if def_spatial_filter is not None:
        if norm == False:
            path_save_long=os.path.join(path, f'{feature}_{name_bd}_{task}_{def_spatial_filter}_long.feather')
            path_save=os.path.join(path, f'{feature}_{name_bd}_{task}_{def_spatial_filter}_columns.feather')
        elif norm:
            if z_score:
                path_save_long=os.path.join(path, f'{feature}_{name_bd}_{task}_{def_spatial_filter}_zscore_long.feather')
                path_save=os.path.join(path, f'{feature}_{name_bd}_{task}_{def_spatial_filter}_zscore_columns.feather')
            elif huber:
                path_save_long=os.path.join(path, f'{feature}_{name_bd}_{task}_{def_spatial_filter}_huber_long.feather')
                path_save=os.path.join(path, f'{feature}_{name_bd}_{task}_{def_spatial_filter}_huber_columns.feather')   
        
        df_metric_long.rename(columns={'Sensors': 'Component'})
    else:
        if norm == False:
            if fir==False:
                path_save_long=os.path.join(path, f'{feature}_{name_bd}_{task}_long.feather')
                path_save=os.path.join(path, f'{feature}_{name_bd}_{task}_columns.feather')
            else:
                path_save_long=os.path.join(path, f'{feature}_{name_bd}_{task}_fir_long.feather')
                path_save=os.path.join(path, f'{feature}_{name_bd}_{task}_fir_columns.feather')
            
        elif norm:
            if z_score:
                path_save_long=os.path.join(path, f'{feature}_{name_bd}_{task}_zscore_long.feather')
                path_save=os.path.join(path, f'{feature}_{name_bd}_{task}_zscore_columns.feather')
            elif huber:
                path_save_long=os.path.join(path, f'{feature}_{name_bd}_{task}_huber_long.feather')
                path_save=os.path.join(path, f'{feature}_{name_bd}_{task}_huber_columns.feather')
    
    if path_demographics is not None :
        if values['metadata']['type']!= 'psd':
            data_demographics = pd.read_excel(path_demographics)
            df_metric_column = pd.merge(df_metric_column, data_demographics, on=['subject', 'group'], how='outer')
            df_metric_long.to_feather(path_save_long)
            df_metric_column.to_feather(path_save)
            
        else:
            df_metric_long.to_feather(path_save_long)
            
  
    else:
        if values['metadata']['type']!= 'psd':
            df_metric_long.to_feather(path_save_long)
            df_metric_column.to_feather(path_save)
            
        else:
            df_metric_long.to_feather(path_save_long)

def run_postprocessing (DATASET= dict,electrodes =list,def_spatial_filter =None, bands=dict, features_tuples=list, path=str,epoch=int, norm =False, z_score=False, huber=False,fir=False):
    
    """
    Run postprocessing on the given dataset.

    This function performs various postprocessing steps on the provided dataset,
    including applying spatial filters, extracting features, and saving the results
    to a specified path in long and column format.
THE_DATASET
    Parameters:
    - DATASET: The dataset to be processed. This could be an EEG dataset or any other
               type of data that requires postprocessing.
    - def_spatial_filter: The default spatial filter to be applied. If None, no spatial
                          filter is applied by default. This parameter is optional.
    - bands: A dictionary defining the frequency bands to be used in feature extraction.
             This parameter is optional and defaults to an empty dictionary.
    - features_tuples: A list of tuples where each tuple contains the name of a feature
                       extraction method and a dictionary of parameters for that method.
                       This parameter is optional and defaults to an empty list.
                       Example:
                       features_tuples=[
                           ('cohfreq', {'window': 3, 'bands': bands_task}),
                           ('sl', {'bands': bands_task}),
                           ('power', {'bands': bands_task, 'irasa': False, 'osc': False, 'aperiodic': False}),
                           ('crossfreq', {'bands': bands_task}),
                           ('entropy',{'bands':bands,'D':3}),
                           ('psd', {'bands': bands_ce}),
                       ]
    - path: The path where the postprocessed results will be saved. This parameter is
            optional and defaults to an empty string.

    Returns:
    - None: The function performs postprocessing and saves the results to the specified path.
    """
    for feature,kwargs in features_tuples:
        get_metrics(THE_DATASET=DATASET, 
                    bands=bands,
                    path=path,
                    def_spatial_filter =def_spatial_filter,
                    feature=feature,
                    kwargs=kwargs,
                    path_demographics=DATASET.get('demographic',None),
                    electrodes=electrodes,
                    epoch=epoch,
                    norm=norm,
                    z_score=z_score,
                    huber=huber,
                    fir=fir
                    )

def get_time(THE_DATASET=dict,
                score_muscle = 0.7,
                correlation_threshold = 0.2,
                frac_bad = 0.05,
                ):
    input_path = THE_DATASET.get('input_path',None)
    layout_dict = THE_DATASET.get('layout',None)
    # Static Params
    layout = BIDSLayout(input_path)
    bids_root = layout.root
    eegs = layout.get(**layout_dict)
    pipeline = 'APPLEE'
    derivatives_root = os.path.join(layout.root,'derivatives',pipeline)
    log_path = os.path.join(derivatives_root,'code')
    os.makedirs(log_path, exist_ok=True)
    logger,currentdt = cfg_logger(log_path)
    num_files = len(eegs)
    default_channels = ['AF3',	'AF4',	'C1',	'C2',	'C3',	'C4',	'C5',	'C6',	'CP1',	'CP2',	'CP3',	'CP4',	'CP5',	'CP6',	'CPZ',	'CZ',	'F1',	'F2',	'F3',	'F4',	'F5',	'F6',	'F7',	'F8',	'FC1',	'FC2',	'FC3',	'FC4',	'FC5',	'FC6',	'FP1',	'FP2',	'FZ',	'O1',	'O2',	'OZ',	'P1',	'P2',	'P3',	'P4',	'P5',	'P6',	'P7',	'P8',	'PO3',	'PO4',	'PO7',	'PO8',	'POZ',	'PZ','T5','T6'	,'T7',	'T8',	'TP7',	'TP8'] #Yorguin
    channels = THE_DATASET.get('channels',default_channels)
    task=THE_DATASET.get('layout')['task']
    # Get all combinations of the parameters
    info_feature=[]
    signal_time =[]
    name_bd = THE_DATASET.get('name')
    for i,eeg_file in enumerate(eegs):     
        #process=str(i)+'/'+str(num_files)
        msg =f"File {i+1} of {num_files} ({(i+1)*100/num_files}%) : {eeg_file}"
        logger.info(msg)
        
        param_id = f'sm{score_muscle}_ct{correlation_threshold}_fb{frac_bad}'
        DM_path = get_derivative_path(layout,eeg_file,f'Muscle_{param_id}','eeg','.fif',bids_root,derivatives_root)
        info_bids_sujeto = parse_file_entities(eeg_file)
        signal_DM = mne.io.read_raw(DM_path)
        if name_bd == 'Chile' or name_bd == 'Argentina' or name_bd =='Medellín hd' or name_bd == 'Cuba':
            data = signal_DM.get_data()*1e6
        else:
            data =signal_DM.get_data()
        signal_time.extend([
            {'subject': 'sub-'+ info_bids_sujeto['subject'], 'Sensors': sensor, 'time': time}
            for sensor, time in zip(signal_DM.info['ch_names'], data)])
    df_time=pd.DataFrame(signal_time)
    return df_time  

