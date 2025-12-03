# 🔬 Neural Electrode Arrays

> **Technologies for interfacing with neural tissue**

Neural electrodes enable recording brain activity and delivering stimulation for BCIs and neuroprosthetics.

---

## 📊 Electrode Types

| Type | Channels | Resolution | Invasiveness | Example |
|------|----------|------------|--------------|---------|
| **EEG** | 16-256 | Low (cm) | Non-invasive | Scalp electrodes |
| **ECoG** | 64-256 | Medium (mm) | Invasive | Subdural grid |
| **Utah Array** | 96-1024 | High (µm) | Highly invasive | Intracortical |
| **Neuropixels** | 384-5000 | Ultra-high | Acute | Silicon probe |

---

## 🔧 Utah Array
**Intracortical recording**

```
Specifications:
- 10×10 array = 100 electrodes
- 1 mm electrode length
- 400 µm spacing
- Platinum tips
- Silicon substrate
```

### Advantages
- High spatial resolution
- Single neuron recording
- Multi-unit activity

### Challenges
- Tissue damage during insertion
- Chronic inflammation
- Signal degradation over time (months-years)

---

## 🧠 ECoG (Electrocorticography)
**Subdural surface recording**

```
Specifications:
- 8×8 to 16×16 grids
- 4-10 mm electrode diameter
- Flexible substrate (silicone)
- Lower impedance than intracortical
```

---

## 🔗 Related Topics

- [Signal Processing](../computer-science/signal-processing.md) - Process neural signals
- [Implant Design](implant-design-principles.md) - Integration
- [BCI](../artificial-intelligence/brain-computer-interfaces.md) - Applications

---

[⬅️ Back to BME Index](README.md)
