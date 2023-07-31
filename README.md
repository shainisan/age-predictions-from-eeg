# Age Prediction from EEG Data

This project aims to predict the age of individuals using electroencephalogram (EEG) data. It involves feature extraction, feature engineering, feature selection, and predictive modeling processes.

---

## Dataset Information

This project uses the EEG dataset available on OpenNeuro with the Accession Number `ds003775`. 

**Details about the Dataset:**

- Authors: Christoffer Hatlestad-Hall, Trine Waage Rygvold, Stein Andersson
- Modalities Available: EEG
- Version: 1.2.1, Created on 2022-11-23
- Task: resteyesc
- Uploaded by: Christoffer Hatlestad-Hall on 2021-08-25 
- Last Updated: 2022-11-23
- Sessions: 2
- Participants: 111

The dataset contains resting-state EEG.

You can find more about the dataset [here](https://openneuro.org/datasets/ds003775/versions/1.2.1).

To download the dataset, you can use the following command:

```bash
aws s3 sync --no-sign-request s3://openneuro.org/ds003775 ds003775-download/
```

Please ensure the dataset is downloaded to the correct path as specified in the scripts used in this project.

Certainly, here's an expanded version of that section:

---

## Running the MNE-BIDS Pipeline

The MNE-BIDS Pipeline is a powerful tool for processing and analyzing M/EEG data. It leverages the Brain Imaging Data Structure (BIDS) standard to ensure that the structure of the data and metadata is consistent and in a format that's accessible for further analysis. The pipeline takes raw EEG data as input, and processes it through various stages including filtering, artifact rejection, epoching, and more, to produce preprocessed data ready for feature extraction and modeling.

Install required dependencies first:

```bash
pip install --upgrade mne-bids-pipeline
pip install numpy matplotlib scipy numba scikit-learn mne PyWavelets pandas
pip install mne-features
```

After downloading and setting up the data, you can run the MNE-BIDS pipeline using the provided Bash script `pipeline.sh`.

Before running the script, ensure it's executable by running:

```bash
chmod +x pipeline.sh
```

Then, you can execute the pipeline with the following command:

```bash
./pipeline.sh
```

This script will automatically run the MNE-BIDS pipeline using the configuration file `config_shai.py`. This configuration file specifies a series of processing steps, such as filtering parameters, epoching details, artifact rejection criteria, etc., for the pipeline to follow. Please make sure that `config_shai.py` is available in the correct path as specified inside the `pipeline.sh` script.

By running the script, the raw data will be preprocessed according to the specifications provided in `config_shai.py`, readying it for subsequent stages of feature extraction and modeling.

---

## Feature Extraction

Feature extraction is performed using the Python script `feature_extraction.py`. The script loads each participant's EEG data, computes the features defined below, and appends these features to a DataFrame, which is saved as a .csv file after all the subjects' data have been processed. Make sure you have enough computational resources.

To run the script, ensure it's executable and then execute the following command in the terminal:

```bash
chmod +x feature_extraction.py
./feature_extraction.py
```
Or you can run it using the Python interpreter:

```bash
python3 feature_extraction.py
```

The features extracted from the EEG data include:

- Mean
- Standard Deviation
- Kurtosis
- Skewness
- Quantile
- Peak-to-peak amplitude (ptp_amp)
- Power in specific frequency bands (pow_freq_bands)
- Spectral entropy (spect_entropy)
- Approximate entropy (app_entropy)
- Sample entropy (samp_entropy)
- Hurst exponent (hurst_exp)
- Hjorth parameters: complexity and mobility (hjorth_complexity, hjorth_mobility)
- Line length
- Energy of wavelet coefficients (wavelet_coef_energy)
- Higuchi fractal dimension (higuchi_fd)
- Zero crossings
- Singular value decomposition-based Fisher information (svd_fisher_info)

---

# Approaches Used
Two distinct approaches were adopted for this project - one focusing on handcrafted features and the other based on deep learning.

## Approach 1: Handcrafted Features
In this approach, a series of machine learning models were trained on these features, with the SVM model achieving the best performance.

This is in the notebook `ML_features.ipynb`.

## Approach 2: Deep Learning
The second approach made use of ConvNets, achieving a mean absolute error of 3.2, a significant improvement over the handcrafted feature approach. However, due to the limited dataset size and computational resources, these results should be interpreted cautiously.

### Credit
The functions `create_model` and `create_estimator` that were used for the deep learning approach were taken from this [GitHub repository](https://github.com/meeg-ml-benchmarks/brain-age-benchmark-paper/blob/c57eba38c8b90dac9354f0f4f8148dbed7e56029/deep_learning_utils.py#L529). These functions were crucial for creating and compiling the model.

This is in the notebook `Deep_learning_braindecode.ipynb`
