# 📖 Glossary

> **Comprehensive terminology for human-embedded technology**

Definitions spanning Computer Science, Artificial Intelligence, and Biomedical Engineering.

---

## A

**Action Potential**: Brief electrical signal propagated along neuron axon, fundamental unit of neural communication (~1 ms duration, 100 mV amplitude).

**ADC (Analog-to-Digital Converter)**: Converts continuous analog signals (e.g., neural voltage) to discrete digital values for processing.

**Artifact**: Unwanted signal component not originating from source of interest (e.g., eye blinks in EEG, motion artifacts).

**Attention Mechanism**: Neural network technique that weighs importance of different input elements, crucial for time-series biosignal analysis.

---

## B

**Bandpass Filter**: Filter passing frequencies within specific range while attenuating others (e.g., 8-30 Hz for EEG motor imagery).

**BCI (Brain-Computer Interface)**: Direct communication pathway between brain and external device, bypassing peripheral nerves and muscles.

**Biocompatibility**: Ability of material to perform with appropriate host response, critical for implants (tested per ISO 10993).

**BLE (Bluetooth Low Energy)**: Wireless protocol optimized for low power consumption, commonly used in implantable devices.

---

## C

**Closed-Loop System**: System with feedback where output influences input (e.g., responsive neurostimulation based on detected seizures).

**Common Spatial Patterns (CSP)**: Supervised spatial filtering technique for motor imagery BCI, maximizes variance difference between classes.

**Convolutional Neural Network (CNN)**: Deep learning architecture using convolution operations, effective for spatial patterns in multi-channel biosignals.

**Cortex**: Outer layer of brain, divided into motor, sensory, and association areas. Target for ECoG and some BCIs.

---

## D

**Deep Brain Stimulation (DBS)**: Implanted electrodes delivering electrical stimulation to specific brain regions, treats Parkinson's, epilepsy.

**DSP (Digital Signal Processing)**: Mathematical manipulation of discrete-time signals, fundamental for biosignal analysis.

**Duty Cycle**: Fraction of time device is active vs. sleeping, critical for implant power budgeting.

---

## E

**ECoG (Electrocorticography)**: Recording electrical activity from brain surface (subdural), higher resolution than scalp EEG.

**Edge ML**: Machine learning inference on edge devices (vs. cloud), essential for low-latency implants.

**EEG (Electroencephalography)**: Recording brain electrical activity from scalp, non-invasive, 10-100 µV amplitude.

**EMG (Electromyography)**: Recording muscle electrical activity, used for prosthetic control and rehabilitation.

**Epoch**: Fixed-length segment of continuous signal, typical unit for analysis (e.g., 2-second EEG epochs).

---

## F

**FDA (Food and Drug Administration)**: US regulatory agency overseeing medical device approval and safety.

**Feature Extraction**: Process of deriving informative measurements from raw signals (e.g., band power from EEG).

**FIR (Finite Impulse Response)**: Digital filter type with guaranteed stability and linear phase, used in offline processing.

---

## G

**Gait**: Walking pattern, analyzed via EMG or motion capture for neuroprosthetics and rehabilitation.

---

## H

**Hermetic Seal**: Airtight seal preventing fluid ingress, essential for implant longevity (IP68+ rating).

**HRV (Heart Rate Variability)**: Variation in time between heartbeats, indicator of autonomic nervous system function.

---

## I

**ICA (Independent Component Analysis)**: Blind source separation technique for removing artifacts from EEG (e.g., eye blinks, muscle).

**Impedance**: Opposition to current flow, important for electrode-tissue interface (target: <5 kΩ @ 1 kHz).

**IIR (Infinite Impulse Response)**: Efficient digital filter type, requires care to ensure stability (poles inside unit circle).

**Inductive Coupling**: Wireless power transfer via magnetic fields, common for implant charging (6.78 MHz, 13.56 MHz).

---

## L

**LFP (Local Field Potential)**: Extracellular recording of neural population activity (1-300 Hz), reflects synaptic activity.

**LSTM (Long Short-Term Memory)**: RNN variant handling long-term dependencies, effective for sequential biosignal data.

---

## M

**MAV (Mean Absolute Value)**: Time-domain EMG feature, indicates muscle activation level.

**MICS (Medical Implant Communication Service)**: 402-405 MHz band reserved for implant telemetry (25 µW max power).

**Motor Imagery (MI)**: Mental rehearsal of movement without execution, paradigm for BCI control.

---

## N

**Neural Dust**: Conceptual ultrasonic-powered sub-mm neural sensors for distributed brain recording.

**Neuroprosthetic**: Artificial device replacing or enhancing nervous system function (e.g., cochlear implant, prosthetic limb).

**NFC (Near-Field Communication)**: Short-range wireless protocol (<10 cm), used for passive implant tags.

---

## O

**Optogenetics**: Technique using light to control genetically modified neurons, promising for precise neuromodulation.

---

## P

**P300**: Event-related potential occurring ~300 ms after oddball stimulus, used in BCI spelling systems.

**Parylene**: Conformal polymer coating for implant encapsulation, excellent hermetic barrier (Parylene-C common).

**PMA (Premarket Approval)**: Most rigorous FDA device approval pathway, required for Class III high-risk devices.

**Pruning**: Model compression technique removing unnecessary weights, critical for edge deployment.

**PSD (Power Spectral Density)**: Frequency-domain representation of signal power distribution (µV²/Hz).

---

## Q

**Quantization**: Reducing numerical precision (float32 → int8), enables deployment on resource-constrained devices.

**QRS Complex**: Ventricular depolarization waveform in ECG, detected for heart rate measurement.

---

## R

**RMS (Root Mean Square)**: EMG feature indicating signal power, correlates with muscle force.

**RTOS (Real-Time Operating System)**: OS guaranteeing task execution within deadline, essential for closed-loop systems (e.g., FreeRTOS, Zephyr).

---

## S

**SaMD (Software as Medical Device)**: Software performing medical function independent of hardware, subject to FDA regulation.

**Spike Sorting**: Classifying action potentials by neuron of origin, enables single-unit recordings.

**SSVEP (Steady-State Visual Evoked Potential)**: Frequency-locked brain response to flickering stimulus, high-accuracy BCI paradigm.

---

## T

**TinyML**: Machine learning on microcontrollers (<1 MB memory), enables on-implant inference.

**Titanium (Ti)**: Biocompatible metal for implant housings, osseointegrates with bone, MRI-compatible.

**Transfer Learning**: Using pre-trained model as starting point, reduces training data requirements for medical AI.

---

## U

**Utah Array**: 100-electrode intracortical silicon array (Blackrock Neurotech), gold standard for high-channel-count recording.

---

## V

**VNS (Vagus Nerve Stimulation)**: Electrical stimulation of vagus nerve, treats epilepsy and depression.

---

## W

**Wavelet Transform**: Time-frequency analysis method, superior to STFT for non-stationary signals like ECG.

**WCET (Worst-Case Execution Time)**: Maximum time task can take, critical for hard real-time systems.

---

## Z

**Zero Crossing**: Point where signal crosses zero, EMG feature indicating frequency content.

---

## 📚 Further Reading

- **Computer Science**: [CS Section](../docs/computer-science/)
- **Artificial Intelligence**: [AI Section](../docs/artificial-intelligence/)
- **Biomedical Engineering**: [BME Section](../docs/biomedical-engineering/)

---

[⬅️ Back to Main](../README.md)
