# 🧠 EEG Brain-Computer Interface Demo

> **Motor imagery BCI for cursor control**

---

## 🎯 Project Overview

Build a motor imagery BCI that detects imagined left/right hand movements from EEG.

### Skills Developed
- EEG signal processing
- Common Spatial Patterns (CSP)
- Real-time classification
- BCI paradigm design

---

## 🔧 Hardware Required

- OpenBCI Ultracortex or Emotiv EPOC
- Computer with Python
- Optional: Stimulus presentation software

---

## 📊 BCI Protocol

```
1. Calibration Phase (5-10 minutes)
   - User imagines left/right hand movement
   - Record 20-40 trials per class
   - Train CSP + LDA classifier

2. Online Phase
   - Real-time classification every 1 second
   - Control cursor or external device
   - Achieve 70-85% accuracy
```

---

## 💻 Implementation

See [Simple BCI Demo](../../code/neural-interface-demos/simple_bci_demo.py) for complete implementation.

---

[⬅️ Back to Projects](../README.md)
