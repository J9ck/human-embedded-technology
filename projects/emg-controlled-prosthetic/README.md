# 🦾 EMG-Controlled Prosthetic Hand

> **Myoelectric control system for prosthetic devices**

---

## 🎯 Project Overview

Build a system that classifies EMG signals from forearm muscles to control a prosthetic hand.

### Skills Developed
- EMG signal acquisition
- Real-time feature extraction
- Machine learning classification
- Embedded systems integration

---

## 🔧 Hardware Required

- OpenBCI Cyton board or MyoWare EMG sensors
- Arduino or ESP32 microcontroller
- Servo motors (for prosthetic hand)
- 3D-printed prosthetic hand (optional)

---

## 📊 System Architecture

```
Forearm Muscles
      ↓
  EMG Electrodes (2-4 channels)
      ↓
  Amplifier + Filter
      ↓
  ADC (1 kHz sampling)
      ↓
  Feature Extraction (MAV, WL, ZC)
      ↓
  Classifier (SVM or Random Forest)
      ↓
  Servo Control (open/close/grasp)
```

---

## 💻 Implementation Steps

1. **Data Collection**: Record EMG for different gestures (rest, open, close, pinch)
2. **Preprocessing**: Bandpass filter (20-450 Hz), rectification
3. **Feature Extraction**: Extract time-domain features per 200 ms window
4. **Model Training**: Train classifier on collected data (accuracy >80%)
5. **Real-Time Control**: Deploy classifier for live prosthetic control

---

## 📚 Resources

- [EMG Feature Extraction Code](../../code/biosignal-processing/emg_feature_extraction.py)
- [OpenBCI Documentation](https://docs.openbci.com/)
- [MyoWare Sensor Guide](https://learn.adafruit.com/myoware-muscle-sensor)

---

[⬅️ Back to Projects](../README.md)
