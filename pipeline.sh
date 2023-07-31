#!/bin/bash

pip install --upgrade mne-bids-pipeline
pip install numpy matplotlib scipy numba scikit-learn mne PyWavelets pandas
pip install mne-features

mne_bids_pipeline --config=config_shai.py
