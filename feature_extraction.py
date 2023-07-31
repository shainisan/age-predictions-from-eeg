#!/usr/bin/env python3

from mne_features.feature_extraction import extract_features
import mne
from joblib import Parallel, delayed
import pandas as pd

def compute_features(i, ch_name, epochs):
    ch_data = epochs.get_data(picks=ch_name)
    features = extract_features(ch_data, sfreq=epochs.info['sfreq'], selected_funcs=selected_funcs, funcs_params=selected_params, return_as_df=False)
    feature_dict = {}
    for feature_name, feature_values in zip(selected_funcs, features):
        feature_dict[f'{ch_name}_{feature_name}'] = feature_values[0]
    return feature_dict

def main():
    feature_df = pd.DataFrame()
    participants = pd.read_csv('../participants.tsv', sep='\t')
    subject_ids = participants['participant_id'].unique()
    frequency_bands = [0, 2, 4, 8, 13, 18, 24, 30, 49]
    selected_funcs = [
        'mean', 'std', 'kurtosis', 'skewness', 'quantile', 'ptp_amp',
        'pow_freq_bands', 'spect_entropy', 'app_entropy', 'samp_entropy', 
        'hurst_exp', 'hjorth_complexity', 'hjorth_mobility', 'line_length',
        'wavelet_coef_energy', 'higuchi_fd', 'zero_crossings', 'svd_fisher_info'
    ]
    selected_params = {
        'quantile__q': [0.1, 0.25, 0.75, 0.9],
        'pow_freq_bands__freq_bands': frequency_bands,
    }

    for sub_id in subject_ids:
        epochs = mne.read_epochs(f'../derivatives/{sub_id}/ses-t1/eeg/{sub_id}_ses-t1_task-resteyesc_proc-clean_epo.fif')
        results = Parallel(n_jobs=-1, backend='loky')(delayed(compute_features)(i, ch_name, epochs) for i, ch_name in enumerate(epochs.ch_names))
        feature_dict = {}
        for result in results:
            feature_dict.update(result)
        subject_age = participants.loc[participants['participant_id'] == sub_id, 'age'].values[0]
        feature_dict['age'] = subject_age
        feature_df = feature_df.append(pd.DataFrame(feature_dict, index=[0]), ignore_index=True)
        feature_df.to_csv('feature_df.csv', index=False)
if __name__ == "__main__":
    main()
