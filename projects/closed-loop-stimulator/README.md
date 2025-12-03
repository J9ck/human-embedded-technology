# 🔁 Closed-Loop Neuromodulation System

> **Responsive brain stimulation for epilepsy or Parkinson's**

---

## 🎯 System Overview

Detect pathological brain activity and deliver therapeutic stimulation.

### Applications
- Epilepsy (RNS-like responsive neurostimulation)
- Parkinson's disease (adaptive DBS)
- Chronic pain management
- Depression treatment

---

## 🏗️ System Architecture

```
Recording Electrodes (ECoG or LFP)
      ↓
  Amplifier (gain: 1000-10000)
      ↓
  Bandpass Filter (1-100 Hz)
      ↓
  ADC (1-2 kHz sampling)
      ↓
  Real-Time Processor
    - Seizure detection algorithm
    - Power spectral analysis
    - Threshold detection
      ↓
  Decision Logic
      ↓
  Stimulation Generator
    - Biphasic pulses
    - 1-200 Hz, 0-10 mA
      ↓
  Stimulation Electrodes
```

---

## ⚡ Key Requirements

- **Latency**: <10 ms from detection to stimulation
- **Sensitivity**: >90% detection rate
- **Specificity**: <1 false positive per hour
- **Safety**: Charge-balanced stimulation only
- **Power**: <50 mW total system power

---

## 📚 References

- NeuroPace RNS System
- Medtronic Percept PC (adaptive DBS)
- Research: Closed-loop optogenetics

---

[⬅️ Back to Projects](../README.md)
