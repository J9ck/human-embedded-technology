#!/usr/bin/env python3
"""
EEG Preprocessing Pipeline
===========================

Demonstrates bandpass filtering, artifact removal, and epoching for EEG signals.

Author: Jack Doyle (J9ck)
Website: https://www.jgcks.com
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def bandpass_filter(data, lowcut, highcut, fs, order=4):
    """
    Apply Butterworth bandpass filter to EEG signal.
    
    Parameters:
    -----------
    data : array
        Input EEG signal
    lowcut : float
        Low cutoff frequency (Hz)
    highcut : float
        High cutoff frequency (Hz)
    fs : float
        Sampling frequency (Hz)
    order : int
        Filter order
        
    Returns:
    --------
    filtered : array
        Bandpass filtered signal
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    
    b, a = signal.butter(order, [low, high], btype='band')
    filtered = signal.filtfilt(b, a, data)
    
    return filtered


def notch_filter(data, freq, fs, Q=30):
    """
    Remove power line interference (50/60 Hz).
    
    Parameters:
    -----------
    data : array
        Input signal
    freq : float
        Frequency to remove (Hz)
    fs : float
        Sampling frequency (Hz)
    Q : float
        Quality factor (higher = narrower notch)
        
    Returns:
    --------
    filtered : array
        Notch filtered signal
    """
    nyq = 0.5 * fs
    w0 = freq / nyq
    
    b, a = signal.iirnotch(w0, Q)
    filtered = signal.filtfilt(b, a, data)
    
    return filtered


def compute_psd(data, fs, nperseg=256):
    """
    Compute power spectral density using Welch's method.
    
    Parameters:
    -----------
    data : array
        Input signal
    fs : float
        Sampling frequency (Hz)
    nperseg : int
        Length of each segment
        
    Returns:
    --------
    freqs : array
        Frequency bins
    psd : array
        Power spectral density
    """
    freqs, psd = signal.welch(data, fs, nperseg=nperseg, scaling='density')
    return freqs, psd


def extract_band_power(data, fs, low, high):
    """
    Extract power in specific frequency band.
    
    Parameters:
    -----------
    data : array
        Input signal
    fs : float
        Sampling frequency (Hz)
    low : float
        Lower frequency bound (Hz)
    high : float
        Upper frequency bound (Hz)
        
    Returns:
    --------
    power : float
        Band power
    """
    freqs, psd = compute_psd(data, fs)
    idx = np.logical_and(freqs >= low, freqs <= high)
    power = np.trapz(psd[idx], freqs[idx])
    return power


def epoch_data(data, fs, epoch_length, overlap=0.5):
    """
    Split continuous data into epochs.
    
    Parameters:
    -----------
    data : array
        Continuous signal
    fs : float
        Sampling frequency (Hz)
    epoch_length : float
        Epoch duration (seconds)
    overlap : float
        Overlap between epochs (0-1)
        
    Returns:
    --------
    epochs : array
        Array of shape (n_epochs, epoch_samples)
    """
    epoch_samples = int(epoch_length * fs)
    step = int(epoch_samples * (1 - overlap))
    
    epochs = []
    for start in range(0, len(data) - epoch_samples + 1, step):
        epoch = data[start:start + epoch_samples]
        epochs.append(epoch)
    
    return np.array(epochs)


def preprocess_eeg(data, fs):
    """
    Complete preprocessing pipeline for EEG.
    
    Parameters:
    -----------
    data : array
        Raw EEG signal
    fs : float
        Sampling frequency (Hz)
        
    Returns:
    --------
    clean : array
        Preprocessed EEG
    """
    # 1. Remove power line noise
    clean = notch_filter(data, 60, fs)  # 60 Hz for US, use 50 Hz for EU
    
    # 2. Bandpass filter (0.5-40 Hz typical for EEG)
    clean = bandpass_filter(clean, 0.5, 40, fs)
    
    # 3. Normalize
    clean = (clean - np.mean(clean)) / np.std(clean)
    
    return clean


def main():
    """Demonstration of EEG preprocessing."""
    
    # Generate synthetic EEG data (10 seconds)
    fs = 250  # 250 Hz sampling rate
    duration = 10
    t = np.linspace(0, duration, int(fs * duration))
    
    # Synthetic EEG: alpha (10 Hz) + beta (20 Hz) + noise + 60 Hz interference
    eeg = (np.sin(2 * np.pi * 10 * t) +  # Alpha
           0.5 * np.sin(2 * np.pi * 20 * t) +  # Beta
           0.3 * np.random.randn(len(t)) +  # Noise
           0.5 * np.sin(2 * np.pi * 60 * t))  # Power line
    
    # Preprocess
    clean_eeg = preprocess_eeg(eeg, fs)
    
    # Extract band powers
    delta_power = extract_band_power(clean_eeg, fs, 0.5, 4)
    theta_power = extract_band_power(clean_eeg, fs, 4, 8)
    alpha_power = extract_band_power(clean_eeg, fs, 8, 13)
    beta_power = extract_band_power(clean_eeg, fs, 13, 30)
    
    print("EEG Band Powers:")
    print(f"  Delta (0.5-4 Hz): {delta_power:.3f}")
    print(f"  Theta (4-8 Hz):   {theta_power:.3f}")
    print(f"  Alpha (8-13 Hz):  {alpha_power:.3f}")
    print(f"  Beta (13-30 Hz):  {beta_power:.3f}")
    
    # Visualization
    fig, axes = plt.subplots(3, 1, figsize=(12, 8))
    
    # Raw EEG
    axes[0].plot(t, eeg)
    axes[0].set_title('Raw EEG Signal')
    axes[0].set_xlabel('Time (s)')
    axes[0].set_ylabel('Amplitude (µV)')
    axes[0].grid(True)
    
    # Cleaned EEG
    axes[1].plot(t, clean_eeg)
    axes[1].set_title('Preprocessed EEG Signal')
    axes[1].set_xlabel('Time (s)')
    axes[1].set_ylabel('Amplitude (normalized)')
    axes[1].grid(True)
    
    # Power spectrum
    freqs, psd = compute_psd(clean_eeg, fs)
    axes[2].semilogy(freqs, psd)
    axes[2].set_title('Power Spectral Density')
    axes[2].set_xlabel('Frequency (Hz)')
    axes[2].set_ylabel('PSD (µV²/Hz)')
    axes[2].set_xlim([0, 40])
    axes[2].grid(True)
    
    plt.tight_layout()
    plt.savefig('/tmp/eeg_preprocessing_demo.png', dpi=150)
    print("\nPlot saved to /tmp/eeg_preprocessing_demo.png")


if __name__ == "__main__":
    main()
