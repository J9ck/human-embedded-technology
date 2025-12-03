# 🤖 Machine Learning for Medical Devices

> **FDA SaMD considerations for AI/ML medical devices**

---

## FDA Software as Medical Device (SaMD)

### Risk Classification

| Risk Level | Description | Example | Approval |
|------------|-------------|---------|----------|
| **Level I** | Inform clinical management | Fitness tracker | General controls |
| **Level II** | Drive clinical management | ECG analyzer | 510(k) clearance |
| **Level III** | Treat/diagnose, critical | Seizure prediction | PMA (most rigorous) |

---

## ML Model Validation Requirements

### 1. **Training Data**
- Representative of target population
- Balanced classes
- Documented sources and annotations
- Privacy compliance (HIPAA)

### 2. **Performance Metrics**
- Sensitivity (true positive rate)
- Specificity (true negative rate)
- PPV/NPV (positive/negative predictive value)
- ROC-AUC curve
- Confusion matrix

### 3. **Clinical Validation**
- Prospective clinical trial
- Independent test set
- Multiple sites (generalization)
- Statistical power analysis

### 4. **Bias and Fairness**
- Performance across demographics
- Subgroup analysis (age, sex, ethnicity)
- Fairness metrics

### 5. **Interpretability**
- Explainable AI (XAI) techniques
- Feature importance
- Clinician-readable outputs

---

## Continuous Learning and Updates

### FDA Guidance on "Locked" vs. "Adaptive" Algorithms

- **Locked**: Algorithm fixed after approval
- **Adaptive**: Continues learning from new data
  - Requires pre-specified modification plan
  - Performance monitoring
  - Re-validation triggers

---

## Best Practices

1. **Version Control**: Track all model versions
2. **Reproducibility**: Seed random number generators
3. **Testing**: Independent test set (never seen during training)
4. **Documentation**: Comprehensive technical file
5. **Risk Management**: ISO 14971 risk analysis
6. **Quality System**: ISO 13485 compliance

---

## Useful Resources

- FDA Guidance: "Software as a Medical Device (SaMD): Clinical Evaluation"
- FDA Guidance: "Artificial Intelligence/Machine Learning (AI/ML)-Based SaMD"
- IEC 62304: Medical device software lifecycle
- ISO 13485: Quality management systems

---

[⬅️ Back to Cheatsheets](README.md)
