# 🧠 Brain-Computer Interfaces (BCI)

> **Direct communication pathways between brain and external devices**

BCIs enable control of devices through brain activity, critical for assistive technology and human augmentation.

---

## 🎯 BCI Paradigms

### 1. Motor Imagery (MI-BCI)
**Imagining movement** activates motor cortex

```python
# Common Spatial Patterns (CSP) for MI classification
from mne.decoding import CSP
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# Train CSP filters
csp = CSP(n_components=4, reg=None, log=True)
X_csp = csp.fit_transform(X_train, y_train)

# Classify with LDA
lda = LinearDiscriminantAnalysis()
lda.fit(X_csp, y_train)

# Accuracy: 70-85% for 2-class MI
```

### 2. P300 Event-Related Potential
**Oddball paradigm** elicits P300 response at ~300 ms

### 3. SSVEP (Steady-State Visual Evoked Potentials)
**Flickering stimuli** induce frequency-locked brain response

---

## 🔗 Related Topics

- [Neural Networks](neural-networks-biosignals.md) - Deep learning for BCI
- [Code Examples](../../code/neural-interface-demos/) - BCI demo
- [J9ck/AI](https://github.com/J9ck/AI) - ML for time-series

---

[⬅️ Back to AI Index](README.md)
