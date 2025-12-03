#!/usr/bin/env python3
"""
Simple Motor Imagery BCI Demo
==============================

Demonstrates a basic motor imagery brain-computer interface using
Common Spatial Patterns (CSP) and Linear Discriminant Analysis (LDA).

Author: Jack Doyle (J9ck)
"""

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_score


class CSP:
    """Common Spatial Patterns for motor imagery classification."""
    
    def __init__(self, n_components=4):
        self.n_components = n_components
        self.filters = None
        
    def fit(self, X, y):
        """
        Learn CSP filters from training data.
        
        Parameters:
        -----------
        X : array, shape (n_trials, n_channels, n_samples)
            EEG epochs
        y : array, shape (n_trials,)
            Labels (binary: 0 or 1)
        """
        # Compute covariance matrices for each class
        cov_1 = np.mean([np.cov(X[i]) for i in range(len(X)) if y[i] == 0], axis=0)
        cov_2 = np.mean([np.cov(X[i]) for i in range(len(X)) if y[i] == 1], axis=0)
        
        # Solve generalized eigenvalue problem
        eigenvalues, eigenvectors = np.linalg.eig(cov_1 @ np.linalg.inv(cov_2))
        
        # Sort by eigenvalues
        idx = np.argsort(eigenvalues)[::-1]
        eigenvectors = eigenvectors[:, idx]
        
        # Select top and bottom n_components/2 filters
        n_half = self.n_components // 2
        self.filters = np.concatenate([
            eigenvectors[:, :n_half],
            eigenvectors[:, -n_half:]
        ], axis=1)
        
        return self
    
    def transform(self, X):
        """
        Apply CSP filters to extract features.
        
        Parameters:
        -----------
        X : array, shape (n_trials, n_channels, n_samples)
            EEG epochs
            
        Returns:
        --------
        features : array, shape (n_trials, n_components)
            Log-variance features
        """
        # Apply spatial filters
        X_filtered = np.array([self.filters.T @ epoch for epoch in X])
        
        # Compute log-variance features
        features = np.log(np.var(X_filtered, axis=2))
        
        return features


def generate_synthetic_mi_data(n_trials=100, n_channels=22, n_samples=250):
    """
    Generate synthetic motor imagery EEG data.
    
    Parameters:
    -----------
    n_trials : int
        Number of trials per class
    n_channels : int
        Number of EEG channels
    n_samples : int
        Samples per trial (1 second at 250 Hz)
        
    Returns:
    --------
    X : array, shape (n_trials*2, n_channels, n_samples)
        EEG data
    y : array, shape (n_trials*2,)
        Labels (0: left hand, 1: right hand)
    """
    X = []
    y = []
    
    for class_label in [0, 1]:
        for _ in range(n_trials):
            # Generate EEG with class-specific spatial pattern
            spatial_pattern = np.random.randn(n_channels, 1)
            if class_label == 0:
                # Left hand: enhance C3 region (channels 8-10)
                spatial_pattern[8:10] *= 3
            else:
                # Right hand: enhance C4 region (channels 12-14)
                spatial_pattern[12:14] *= 3
            
            # Temporal signal (alpha/beta band modulation)
            t = np.linspace(0, 1, n_samples)
            temporal = (np.sin(2 * np.pi * 10 * t) +  # Alpha
                       0.5 * np.sin(2 * np.pi * 20 * t))  # Beta
            
            # Combine spatial and temporal
            trial = spatial_pattern @ temporal.reshape(1, -1)
            trial += 0.3 * np.random.randn(n_channels, n_samples)
            
            X.append(trial)
            y.append(class_label)
    
    return np.array(X), np.array(y)


def main():
    """Demonstration of motor imagery BCI."""
    
    print("Simple Motor Imagery BCI Demo")
    print("=" * 50)
    
    # Generate synthetic data
    print("\nGenerating synthetic motor imagery data...")
    X, y = generate_synthetic_mi_data(n_trials=100, n_channels=22, n_samples=250)
    
    print(f"Data shape: {X.shape}")
    print(f"Classes: 0 (left hand), 1 (right hand)")
    print(f"Samples per class: {np.sum(y==0)}, {np.sum(y==1)}")
    
    # Train CSP + LDA classifier
    print("\nTraining CSP + LDA classifier...")
    
    # Common Spatial Patterns
    csp = CSP(n_components=4)
    csp.fit(X, y)
    X_csp = csp.transform(X)
    
    # Linear Discriminant Analysis
    lda = LinearDiscriminantAnalysis()
    
    # Cross-validation
    scores = cross_val_score(lda, X_csp, y, cv=5, scoring='accuracy')
    
    print(f"\nCross-Validation Accuracy: {np.mean(scores)*100:.1f}% (+/- {np.std(scores)*100:.1f}%)")
    
    # Train final model
    lda.fit(X_csp, y)
    
    print("\nBCI classifier trained successfully!")
    print("\nIn a real BCI system:")
    print("  1. User imagines left/right hand movement")
    print("  2. EEG is recorded (1-2 seconds)")
    print("  3. CSP features are extracted")
    print("  4. LDA predicts intended movement")
    print("  5. External device (cursor, prosthetic) responds")
    
    # Demo prediction
    print("\nDemo prediction on new trial:")
    test_trial = X[0:1]  # Take first trial
    test_features = csp.transform(test_trial)
    prediction = lda.predict(test_features)[0]
    confidence = lda.predict_proba(test_features)[0]
    
    print(f"  Predicted class: {prediction} ({'left' if prediction==0 else 'right'} hand)")
    print(f"  Confidence: {confidence[prediction]*100:.1f}%")


if __name__ == "__main__":
    main()
