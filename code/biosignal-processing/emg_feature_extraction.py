#!/usr/bin/env python3
"""
EMG Feature Extraction
======================

Extract time-domain and frequency-domain features from EMG signals for
prosthetic control and gesture recognition.

Author: Jack Doyle (J9ck)
Website: https://www.jgcks.com
"""

import numpy as np
from scipy import signal
from scipy.stats import skew, kurtosis


def extract_time_features(emg):
    """
    Extract time-domain features from EMG signal.
    
    Parameters:
    -----------
    emg : array
        EMG signal
        
    Returns:
    --------
    features : dict
        Dictionary of time-domain features
    """
    features = {}
    
    # Mean Absolute Value (MAV)
    features['mav'] = np.mean(np.abs(emg))
    
    # Root Mean Square (RMS)
    features['rms'] = np.sqrt(np.mean(emg**2))
    
    # Variance
    features['var'] = np.var(emg)
    
    # Standard Deviation
    features['std'] = np.std(emg)
    
    # Waveform Length (WL)
    features['wl'] = np.sum(np.abs(np.diff(emg)))
    
    # Zero Crossings (ZC)
    features['zc'] = zero_crossings(emg, threshold=0)
    
    # Slope Sign Changes (SSC)
    features['ssc'] = slope_sign_changes(emg, threshold=0)
    
    # Skewness
    features['skewness'] = skew(emg)
    
    # Kurtosis
    features['kurtosis'] = kurtosis(emg)
    
    return features


def extract_frequency_features(emg, fs):
    """
    Extract frequency-domain features from EMG signal.
    
    Parameters:
    -----------
    emg : array
        EMG signal
    fs : float
        Sampling frequency (Hz)
        
    Returns:
    --------
    features : dict
        Dictionary of frequency-domain features
    """
    # Compute power spectral density
    freqs, psd = signal.welch(emg, fs, nperseg=min(256, len(emg)//2))
    
    features = {}
    
    # Mean Frequency (MNF)
    features['mean_freq'] = np.average(freqs, weights=psd)
    
    # Median Frequency (MDF)
    cumsum_psd = np.cumsum(psd)
    idx = np.where(cumsum_psd >= cumsum_psd[-1] / 2)[0]
    features['median_freq'] = freqs[idx[0]] if len(idx) > 0 else 0
    
    # Peak Frequency
    features['peak_freq'] = freqs[np.argmax(psd)]
    
    # Total Power
    features['total_power'] = np.trapz(psd, freqs)
    
    # Spectral Entropy
    psd_norm = psd / np.sum(psd)
    features['spectral_entropy'] = -np.sum(psd_norm * np.log2(psd_norm + 1e-10))
    
    return features


def zero_crossings(signal, threshold=0):
    """Count number of zero crossings."""
    crossings = np.where(np.diff(np.sign(signal - threshold)))[0]
    return len(crossings)


def slope_sign_changes(signal, threshold=0):
    """Count number of slope sign changes."""
    diff_signal = np.diff(signal)
    changes = np.where(np.diff(np.sign(diff_signal)))[0]
    return len(changes)


def extract_all_features(emg, fs):
    """
    Extract both time and frequency domain features.
    
    Parameters:
    -----------
    emg : array
        EMG signal
    fs : float
        Sampling frequency (Hz)
        
    Returns:
    --------
    features : dict
        Combined feature dictionary
    """
    time_features = extract_time_features(emg)
    freq_features = extract_frequency_features(emg, fs)
    
    # Combine dictionaries
    features = {**time_features, **freq_features}
    
    return features


def main():
    """Demonstration of EMG feature extraction."""
    
    # Generate synthetic EMG data (2 seconds of muscle activation)
    fs = 1000  # 1 kHz sampling rate
    duration = 2
    t = np.linspace(0, duration, int(fs * duration))
    
    # Synthetic EMG: Random bursts + filtered noise (20-450 Hz typical for EMG)
    emg = np.random.randn(len(t))
    
    # Bandpass filter (20-450 Hz)
    b, a = signal.butter(4, [20, 450], btype='band', fs=fs)
    emg = signal.filtfilt(b, a, emg)
    
    # Add muscle activation bursts
    for i in range(5):
        start = int(np.random.rand() * len(t))
        length = int(0.2 * fs)  # 200 ms bursts
        if start + length < len(t):
            emg[start:start+length] *= 5  # Amplify burst regions
    
    # Rectify (full-wave rectification)
    emg_rect = np.abs(emg)
    
    # Extract features
    features = extract_all_features(emg_rect, fs)
    
    print("EMG Features:")
    print("\nTime-Domain:")
    print(f"  MAV:      {features['mav']:.4f}")
    print(f"  RMS:      {features['rms']:.4f}")
    print(f"  Variance: {features['var']:.4f}")
    print(f"  WL:       {features['wl']:.2f}")
    print(f"  ZC:       {features['zc']}")
    print(f"  SSC:      {features['ssc']}")
    
    print("\nFrequency-Domain:")
    print(f"  Mean Freq:   {features['mean_freq']:.2f} Hz")
    print(f"  Median Freq: {features['median_freq']:.2f} Hz")
    print(f"  Peak Freq:   {features['peak_freq']:.2f} Hz")
    print(f"  Total Power: {features['total_power']:.4f}")
    
    print("\nFeatures extracted successfully!")
    print("These features can be used for prosthetic control or gesture classification.")


if __name__ == "__main__":
    main()
