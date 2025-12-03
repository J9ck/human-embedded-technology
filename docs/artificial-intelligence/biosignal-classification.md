# 📊 Biosignal Classification

> **Feature extraction and ML pipelines for biosignal analysis**

Traditional ML approaches for biosignal classification using handcrafted features.

---

## 🔧 Feature Extraction

### Time-Domain Features

```python
import numpy as np

def extract_time_features(signal):
    """Extract time-domain features from EMG/EEG"""
    features = {
        'mean': np.mean(signal),
        'std': np.std(signal),
        'rms': np.sqrt(np.mean(signal**2)),
        'mav': np.mean(np.abs(signal)),  # Mean Absolute Value
        'var': np.var(signal),
        'zc': zero_crossings(signal),  # Zero Crossings
        'ssc': slope_sign_changes(signal),  # Slope Sign Changes
        'wl': waveform_length(signal)  # Waveform Length
    }
    return features

def zero_crossings(signal, threshold=0):
    """Count zero crossings"""
    return np.sum(np.diff(np.sign(signal - threshold)) != 0)
```

### Frequency-Domain Features

```python
from scipy import signal as sp_signal

def extract_freq_features(signal, fs=1000):
    """Extract frequency-domain features"""
    freqs, psd = sp_signal.welch(signal, fs, nperseg=256)
    
    features = {
        'mean_freq': np.average(freqs, weights=psd),
        'median_freq': freqs[np.argmax(np.cumsum(psd) >= np.sum(psd)/2)],
        'peak_freq': freqs[np.argmax(psd)],
        'total_power': np.trapz(psd, freqs),
        'spectral_entropy': -np.sum(psd * np.log2(psd + 1e-10))
    }
    
    # Band powers
    features['delta'] = band_power(freqs, psd, 0.5, 4)
    features['theta'] = band_power(freqs, psd, 4, 8)
    features['alpha'] = band_power(freqs, psd, 8, 13)
    features['beta'] = band_power(freqs, psd, 13, 30)
    
    return features
```

---

## 🤖 Classification Pipeline

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Build pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100))
])

# Train
pipeline.fit(X_train, y_train)

# Evaluate
accuracy = pipeline.score(X_test, y_test)
print(f"Accuracy: {accuracy:.2%}")
```

---

## 🔗 Related Topics

- [Signal Processing](../computer-science/signal-processing.md) - Preprocessing
- [Neural Networks](neural-networks-biosignals.md) - Deep learning alternative
- [J9ck/AI](https://github.com/J9ck/AI) - ML algorithms

---

[⬅️ Back to AI Index](README.md)
