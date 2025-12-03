# 📡 Signal Processing for Biosignals

> **Digital signal processing fundamentals for neural interface development**

Signal processing is essential for extracting meaningful information from noisy biosignals (EEG, EMG, ECG). This guide covers filtering, frequency analysis, and artifact removal techniques for real-time and offline processing.

---

## 📋 Table of Contents
- [Biosignal Characteristics](#biosignal-characteristics)
- [Digital Filters](#digital-filters)
- [Frequency Domain Analysis](#frequency-domain-analysis)
- [Artifact Removal](#artifact-removal)
- [Time-Frequency Analysis](#time-frequency-analysis)
- [Implementation Examples](#implementation-examples)

---

## 🧠 Biosignal Characteristics

### Common Biosignals

| Signal | Frequency Range | Amplitude | Use Case |
|--------|----------------|-----------|----------|
| **EEG** | 0.5-100 Hz | 10-100 µV | Brain activity, BCI |
| **EMG** | 20-500 Hz | 50 µV - 5 mV | Muscle activity, prosthetics |
| **ECG** | 0.5-150 Hz | 0.5-4 mV | Heart rate, HRV |
| **ECoG** | 0.5-200 Hz | 50-100 µV | Invasive brain recording |
| **LFP** | 1-300 Hz | 10-100 µV | Local field potentials |
| **Spikes** | 300 Hz - 5 kHz | 50-500 µV | Single neuron action potentials |

### Noise Sources
- **60 Hz / 50 Hz**: Power line interference
- **Motion artifacts**: Electrode movement, cable sway
- **EMG contamination**: Muscle activity (especially in EEG)
- **Eye blinks**: Large artifacts in frontal EEG channels
- **Cardiac artifacts**: ECG contamination in other signals
- **Thermal noise**: Amplifier and electrode impedance

---

## 🔧 Digital Filters

### Filter Types

#### 1. **Bandpass Filter**
Extract frequency band of interest.

```python
import numpy as np
from scipy import signal

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    """
    Apply bandpass filter to biosignal.
    
    Args:
        data: Input signal (1D array)
        lowcut: Low cutoff frequency (Hz)
        highcut: High cutoff frequency (Hz)
        fs: Sampling frequency (Hz)
        order: Filter order
    
    Returns:
        Filtered signal
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    
    # Butterworth filter (maximally flat passband)
    b, a = signal.butter(order, [low, high], btype='band')
    
    # Zero-phase filtering (filtfilt to avoid phase distortion)
    filtered = signal.filtfilt(b, a, data)
    
    return filtered

# Example: EEG alpha band (8-13 Hz)
fs = 250  # Hz
eeg_alpha = bandpass_filter(eeg_data, 8, 13, fs)
```

#### 2. **Notch Filter**
Remove power line interference (50/60 Hz).

```python
def notch_filter(data, freq, fs, Q=30):
    """
    Apply notch filter to remove specific frequency.
    
    Args:
        data: Input signal
        freq: Frequency to remove (Hz)
        fs: Sampling frequency (Hz)
        Q: Quality factor (higher = narrower notch)
    
    Returns:
        Filtered signal
    """
    nyq = 0.5 * fs
    w0 = freq / nyq
    
    b, a = signal.iirnotch(w0, Q)
    filtered = signal.filtfilt(b, a, data)
    
    return filtered

# Remove 60 Hz power line noise
eeg_clean = notch_filter(eeg_data, 60, fs)
```

#### 3. **High-Pass Filter**
Remove DC offset and slow drifts.

```python
def highpass_filter(data, cutoff, fs, order=4):
    """Remove low-frequency drift."""
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    
    b, a = signal.butter(order, normal_cutoff, btype='high')
    filtered = signal.filtfilt(b, a, data)
    
    return filtered

# Remove drift below 0.5 Hz
eeg_drift_removed = highpass_filter(eeg_data, 0.5, fs)
```

### Filter Design Considerations

**IIR vs FIR**:
- **IIR (Infinite Impulse Response)**: Butterworth, Chebyshev, Elliptic
  - Pros: Efficient (low order), less memory
  - Cons: Can be unstable, nonlinear phase
  - Use: Real-time embedded systems

- **FIR (Finite Impulse Response)**: Window method, Parks-McClellan
  - Pros: Always stable, linear phase
  - Cons: Higher order required, more computation
  - Use: Offline processing, when phase linearity critical

**Filter Order**:
- Higher order = sharper cutoff, more attenuation
- Trade-off: Computation cost, potential instability
- Typical: 2nd-4th order for real-time, up to 100+ taps for FIR

**Zero-Phase Filtering**:
- Use `filtfilt()` for offline: forward + backward pass
- Not possible for real-time (causal filtering only)
- Alternative: Use linear-phase FIR for real-time

---

## 📊 Frequency Domain Analysis

### Fast Fourier Transform (FFT)

```python
def compute_psd(data, fs, window='hann', nperseg=256):
    """
    Compute power spectral density using Welch's method.
    
    Args:
        data: Input signal
        fs: Sampling frequency (Hz)
        window: Window function
        nperseg: Length of each segment
    
    Returns:
        freqs: Frequency bins
        psd: Power spectral density
    """
    freqs, psd = signal.welch(data, fs, window=window, 
                              nperseg=nperseg, scaling='density')
    return freqs, psd

# Analyze EEG frequency content
freqs, psd = compute_psd(eeg_data, fs=250)

# Extract band power
def band_power(freqs, psd, low, high):
    """Calculate power in frequency band."""
    idx = np.logical_and(freqs >= low, freqs <= high)
    return np.trapz(psd[idx], freqs[idx])

alpha_power = band_power(freqs, psd, 8, 13)
beta_power = band_power(freqs, psd, 13, 30)
```

### Spectral Features

```python
def extract_spectral_features(data, fs):
    """
    Extract frequency domain features for ML.
    
    Returns:
        Dictionary of features
    """
    freqs, psd = signal.welch(data, fs, nperseg=256)
    
    features = {
        'delta_power': band_power(freqs, psd, 0.5, 4),   # Sleep
        'theta_power': band_power(freqs, psd, 4, 8),     # Drowsiness
        'alpha_power': band_power(freqs, psd, 8, 13),    # Relaxed
        'beta_power': band_power(freqs, psd, 13, 30),    # Alert
        'gamma_power': band_power(freqs, psd, 30, 100),  # Cognitive
        'mean_freq': np.average(freqs, weights=psd),
        'median_freq': freqs[np.argmax(np.cumsum(psd) >= np.sum(psd)/2)],
        'spectral_entropy': -np.sum(psd * np.log2(psd + 1e-10))
    }
    
    return features
```

---

## 🧹 Artifact Removal

### 1. **Moving Average Filter** (Simple Smoothing)

```python
def moving_average(data, window_size):
    """Simple moving average filter."""
    return np.convolve(data, np.ones(window_size)/window_size, mode='same')
```

### 2. **Median Filter** (Spike/Outlier Removal)

```python
from scipy.ndimage import median_filter

def remove_spikes(data, kernel_size=5):
    """Remove impulse noise using median filter."""
    return median_filter(data, size=kernel_size)
```

### 3. **Baseline Drift Removal**

```python
def remove_baseline_drift(data, window_size):
    """
    Remove slow baseline drift using high-pass filter or moving average.
    """
    # Method 1: Moving average subtraction
    baseline = moving_average(data, window_size)
    return data - baseline
    
    # Method 2: Polynomial detrending
    # return signal.detrend(data, type='linear')
```

### 4. **Independent Component Analysis (ICA)**
Remove eye blinks and muscle artifacts from EEG.

```python
from sklearn.decomposition import FastICA

def remove_artifacts_ica(data, n_components):
    """
    Apply ICA to remove artifacts from multi-channel EEG.
    
    Args:
        data: (n_samples, n_channels) EEG data
        n_components: Number of independent components
    
    Returns:
        cleaned: Artifact-removed EEG
    """
    # Apply ICA
    ica = FastICA(n_components=n_components, random_state=0)
    sources = ica.fit_transform(data)
    
    # Identify artifact components (manual or automated)
    # For demo, assume components 0 and 1 are artifacts
    artifact_components = [0, 1]
    
    # Zero out artifact components
    sources[:, artifact_components] = 0
    
    # Reconstruct cleaned signal
    cleaned = ica.inverse_transform(sources)
    
    return cleaned
```

---

## 🌊 Time-Frequency Analysis

### 1. **Short-Time Fourier Transform (STFT)**

```python
def compute_spectrogram(data, fs, window='hann', nperseg=256):
    """
    Compute spectrogram for time-varying frequency content.
    
    Returns:
        t: Time bins
        f: Frequency bins
        Sxx: Spectrogram (power)
    """
    f, t, Sxx = signal.spectrogram(data, fs, window=window, 
                                   nperseg=nperseg, scaling='density')
    return t, f, Sxx

# Visualize time-frequency representation
import matplotlib.pyplot as plt

t, f, Sxx = compute_spectrogram(eeg_data, fs=250)
plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.colorbar(label='Power [dB]')
```

### 2. **Wavelet Transform**

```python
import pywt

def wavelet_decomposition(data, wavelet='db4', level=5):
    """
    Multi-resolution analysis using discrete wavelet transform.
    
    Args:
        data: Input signal
        wavelet: Wavelet type ('db4', 'sym4', 'coif1', etc.)
        level: Decomposition level
    
    Returns:
        coeffs: List of wavelet coefficients [cA_n, cD_n, ..., cD_1]
    """
    coeffs = pywt.wavedec(data, wavelet, level=level)
    return coeffs

def wavelet_denoising(data, wavelet='db4', level=5):
    """
    Denoise signal using wavelet thresholding.
    """
    # Decompose
    coeffs = pywt.wavedec(data, wavelet, level=level)
    
    # Threshold detail coefficients
    sigma = np.median(np.abs(coeffs[-1])) / 0.6745
    threshold = sigma * np.sqrt(2 * np.log(len(data)))
    
    coeffs[1:] = [pywt.threshold(c, threshold, mode='soft') for c in coeffs[1:]]
    
    # Reconstruct
    denoised = pywt.waverec(coeffs, wavelet)
    
    return denoised[:len(data)]
```

---

## 💡 Implementation Examples

### Real-Time Embedded Filter (C)

```c
// Circular buffer for real-time FIR filter
#define FIR_ORDER 64
float fir_coeffs[FIR_ORDER];  // Precomputed filter coefficients
float fir_buffer[FIR_ORDER] = {0};
int fir_index = 0;

float fir_filter(float new_sample) {
    // Add new sample to circular buffer
    fir_buffer[fir_index] = new_sample;
    fir_index = (fir_index + 1) % FIR_ORDER;
    
    // Compute convolution
    float output = 0.0f;
    for (int i = 0; i < FIR_ORDER; i++) {
        int idx = (fir_index + i) % FIR_ORDER;
        output += fir_coeffs[i] * fir_buffer[idx];
    }
    
    return output;
}
```

### Efficient IIR Filter (C)

```c
// Biquad IIR filter (2nd order section)
typedef struct {
    float b0, b1, b2;  // Numerator coefficients
    float a1, a2;      // Denominator coefficients
    float x1, x2;      // Input history
    float y1, y2;      // Output history
} Biquad;

float biquad_filter(Biquad *bq, float input) {
    // Direct Form II Transposed
    float output = bq->b0 * input + bq->x1;
    
    bq->x1 = bq->b1 * input - bq->a1 * output + bq->x2;
    bq->x2 = bq->b2 * input - bq->a2 * output;
    
    return output;
}

// 4th order filter = 2 cascaded biquads
float bandpass_filter_4th_order(float input) {
    static Biquad bq1 = {/* coefficients */};
    static Biquad bq2 = {/* coefficients */};
    
    float stage1 = biquad_filter(&bq1, input);
    float stage2 = biquad_filter(&bq2, stage1);
    
    return stage2;
}
```

---

## 🎯 Best Practices

1. **Anti-Aliasing**: Always low-pass filter before downsampling (Nyquist theorem)
2. **Zero-Phase**: Use `filtfilt()` offline; avoid for real-time
3. **Filter Stability**: Check poles inside unit circle for IIR filters
4. **Boundary Effects**: Pad signals or use overlap-add for block processing
5. **Normalize**: Scale signals to [-1, 1] before filtering to avoid overflow

---

## 🔗 Related Topics

- [Embedded Systems](embedded-systems.md) - Implement filters on microcontrollers
- [Neural Networks for Biosignals](../artificial-intelligence/neural-networks-biosignals.md) - ML after preprocessing
- [Code Examples](../../code/biosignal-processing/) - Python implementations

**External References**:
- [J9ck/AI](https://github.com/J9ck/AI) - ML pipelines for classification

---

## 📚 Resources

- **Book**: "The Scientist and Engineer's Guide to Digital Signal Processing" by Steven W. Smith (free online)
- **Library**: SciPy Signal Processing (`scipy.signal`)
- **Library**: MNE-Python for EEG/MEG analysis
- **Tool**: MATLAB Signal Processing Toolbox

---

[⬅️ Back to CS Index](README.md) | [Next: Low-Power Computing →](low-power-computing.md)
