#!/usr/bin/env python3
"""
ECG Analysis: R-Peak Detection and Heart Rate Variability
==========================================================

Detect QRS complexes and compute heart rate variability metrics.

Author: Jack Doyle (J9ck)
Website: https://www.jgcks.com
"""

import numpy as np
from scipy import signal


def detect_r_peaks(ecg, fs, threshold_factor=0.6):
    """
    Detect R-peaks in ECG signal using Pan-Tompkins algorithm.
    
    Parameters:
    -----------
    ecg : array
        ECG signal
    fs : float
        Sampling frequency (Hz)
    threshold_factor : float
        Factor for adaptive thresholding
        
    Returns:
    --------
    r_peaks : array
        Indices of detected R-peaks
    """
    # 1. Bandpass filter (5-15 Hz for QRS)
    b, a = signal.butter(2, [5, 15], btype='band', fs=fs)
    filtered = signal.filtfilt(b, a, ecg)
    
    # 2. Derivative (emphasizes QRS slope)
    diff = np.diff(filtered)
    
    # 3. Squaring (amplify QRS, suppress noise)
    squared = diff ** 2
    
    # 4. Moving window integration
    window_size = int(0.15 * fs)  # 150 ms window
    integrated = np.convolve(squared, np.ones(window_size)/window_size, mode='same')
    
    # 5. Adaptive thresholding
    threshold = threshold_factor * np.max(integrated)
    
    # 6. Find peaks above threshold
    peaks, _ = signal.find_peaks(integrated, height=threshold, distance=int(0.6*fs))
    
    return peaks


def compute_heart_rate(r_peaks, fs):
    """
    Compute instantaneous heart rate from R-peaks.
    
    Parameters:
    -----------
    r_peaks : array
        R-peak indices
    fs : float
        Sampling frequency (Hz)
        
    Returns:
    --------
    hr : array
        Heart rate in BPM for each beat
    """
    # Compute RR intervals (in seconds)
    rr_intervals = np.diff(r_peaks) / fs
    
    # Convert to BPM
    hr = 60.0 / rr_intervals
    
    return hr


def compute_hrv_metrics(r_peaks, fs):
    """
    Compute Heart Rate Variability (HRV) metrics.
    
    Parameters:
    -----------
    r_peaks : array
        R-peak indices
    fs : float
        Sampling frequency (Hz)
        
    Returns:
    --------
    hrv : dict
        Dictionary of HRV metrics
    """
    # RR intervals in milliseconds
    rr_intervals = np.diff(r_peaks) / fs * 1000
    
    hrv = {}
    
    # Time-domain metrics
    hrv['mean_rr'] = np.mean(rr_intervals)
    hrv['std_rr'] = np.std(rr_intervals)
    hrv['rmssd'] = np.sqrt(np.mean(np.diff(rr_intervals)**2))  # Root mean square of successive differences
    hrv['sdsd'] = np.std(np.diff(rr_intervals))  # Standard deviation of successive differences
    hrv['nn50'] = np.sum(np.abs(np.diff(rr_intervals)) > 50)  # Number of successive RR differences > 50 ms
    hrv['pnn50'] = hrv['nn50'] / len(rr_intervals) * 100  # Percentage
    
    # Frequency-domain metrics (simplified - requires longer recordings for accuracy)
    if len(rr_intervals) > 10:
        freqs, psd = signal.welch(rr_intervals, fs=1000.0/hrv['mean_rr'], nperseg=min(256, len(rr_intervals)))
        
        # LF power (0.04-0.15 Hz)
        lf_idx = np.logical_and(freqs >= 0.04, freqs <= 0.15)
        hrv['lf_power'] = np.trapz(psd[lf_idx], freqs[lf_idx])
        
        # HF power (0.15-0.4 Hz)
        hf_idx = np.logical_and(freqs >= 0.15, freqs <= 0.4)
        hrv['hf_power'] = np.trapz(psd[hf_idx], freqs[hf_idx])
        
        # LF/HF ratio
        hrv['lf_hf_ratio'] = hrv['lf_power'] / hrv['hf_power'] if hrv['hf_power'] > 0 else 0
    
    return hrv


def main():
    """Demonstration of ECG analysis."""
    
    # Generate synthetic ECG (30 seconds at 360 Hz sampling)
    fs = 360
    duration = 30
    t = np.linspace(0, duration, int(fs * duration))
    
    # Simulate ECG with varying heart rate (60-80 BPM)
    hr_mean = 70  # Mean heart rate
    hr_var = 10   # Heart rate variability
    
    ecg = np.zeros(len(t))
    current_time = 0
    r_peak_times = []
    
    while current_time < duration:
        # Variable RR interval
        rr_interval = 60.0 / (hr_mean + hr_var * np.random.randn())
        current_time += rr_interval
        
        if current_time < duration:
            idx = int(current_time * fs)
            if idx < len(ecg):
                # QRS complex (simplified Gaussian)
                qrs_width = int(0.06 * fs)  # 60 ms
                qrs_range = range(max(0, idx-qrs_width//2), 
                                 min(len(ecg), idx+qrs_width//2))
                ecg[qrs_range] += signal.gaussian(len(qrs_range), qrs_width/6)
                r_peak_times.append(idx)
    
    # Add noise
    ecg += 0.1 * np.random.randn(len(ecg))
    
    # Detect R-peaks
    detected_peaks = detect_r_peaks(ecg, fs)
    
    # Compute heart rate
    hr = compute_heart_rate(detected_peaks, fs)
    
    # Compute HRV metrics
    hrv = compute_hrv_metrics(detected_peaks, fs)
    
    print("ECG Analysis Results:")
    print(f"\nDetected {len(detected_peaks)} heartbeats in {duration} seconds")
    print(f"Average Heart Rate: {np.mean(hr):.1f} BPM")
    print(f"HR Range: {np.min(hr):.1f} - {np.max(hr):.1f} BPM")
    
    print("\nHRV Metrics:")
    print(f"  Mean RR:  {hrv['mean_rr']:.1f} ms")
    print(f"  SDNN:     {hrv['std_rr']:.1f} ms")
    print(f"  RMSSD:    {hrv['rmssd']:.1f} ms")
    print(f"  pNN50:    {hrv['pnn50']:.1f} %")
    
    if 'lf_hf_ratio' in hrv:
        print(f"  LF/HF:    {hrv['lf_hf_ratio']:.2f}")
    
    print("\nECG analysis complete!")


if __name__ == "__main__":
    main()
