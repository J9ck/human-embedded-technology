# 🧠 Neural Networks for Biosignals

> **Deep learning architectures for EEG, EMG, and ECG classification**

Deep learning has revolutionized biosignal analysis, enabling automatic feature extraction and improved classification accuracy for neural interfaces.

---

## 📋 Architectures

### 1. Convolutional Neural Networks (CNNs)
**Best for**: Spatial patterns in multi-channel recordings

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class EEGNet(nn.Module):
    """Compact CNN for EEG classification (Lawhern et al., 2018)"""
    def __init__(self, channels=64, samples=128, num_classes=4):
        super(EEGNet, self).__init__()
        
        # Temporal convolution
        self.conv1 = nn.Conv2d(1, 8, (1, 64), padding=(0, 32))
        self.batchnorm1 = nn.BatchNorm2d(8)
        
        # Spatial convolution (depthwise)
        self.conv2 = nn.Conv2d(8, 16, (channels, 1), groups=8)
        self.batchnorm2 = nn.BatchNorm2d(16)
        self.pooling = nn.AvgPool2d((1, 4))
        
        # Separable convolution
        self.conv3 = nn.Conv2d(16, 16, (1, 16), padding=(0, 8))
        self.batchnorm3 = nn.BatchNorm2d(16)
        
        self.flatten = nn.Flatten()
        self.fc = nn.Linear(16 * (samples // 4), num_classes)
        
    def forward(self, x):
        x = F.elu(self.batchnorm1(self.conv1(x)))
        x = F.elu(self.batchnorm2(self.conv2(x)))
        x = self.pooling(F.dropout(x, 0.25))
        x = F.elu(self.batchnorm3(self.conv3(x)))
        x = self.pooling(F.dropout(x, 0.25))
        x = self.flatten(x)
        return self.fc(x)

# Training
model = EEGNet(channels=64, samples=128, num_classes=4)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```

### 2. Recurrent Neural Networks (RNNs)
**Best for**: Temporal dynamics in time-series

```python
class LSTM_EEG(nn.Module):
    """LSTM for sequential EEG analysis"""
    def __init__(self, input_size=64, hidden_size=128, num_layers=2, num_classes=4):
        super(LSTM_EEG, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, 
                           batch_first=True, dropout=0.3)
        self.fc = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        # x: (batch, seq_len, channels)
        lstm_out, _ = self.lstm(x)
        # Use last timestep
        out = self.fc(lstm_out[:, -1, :])
        return out
```

### 3. Attention Mechanisms

```python
class TransformerEEG(nn.Module):
    """Transformer for EEG classification"""
    def __init__(self, channels=64, seq_len=128, num_classes=4):
        super(TransformerEEG, self).__init__()
        self.embedding = nn.Linear(channels, 256)
        encoder_layer = nn.TransformerEncoderLayer(d_model=256, nhead=8)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=4)
        self.fc = nn.Linear(256, num_classes)
        
    def forward(self, x):
        # x: (batch, seq_len, channels)
        x = self.embedding(x)  # (batch, seq_len, 256)
        x = x.permute(1, 0, 2)  # (seq_len, batch, 256)
        x = self.transformer(x)
        x = x.mean(dim=0)  # Global average pooling
        return self.fc(x)
```

---

## 🔗 Related Topics

- [Edge ML for Implants](edge-ml-implants.md) - Deploy models on devices
- [BCI](brain-computer-interfaces.md) - BCI applications
- [J9ck/AI](https://github.com/J9ck/AI) - Deep learning fundamentals

---

[⬅️ Back to AI Index](README.md)
