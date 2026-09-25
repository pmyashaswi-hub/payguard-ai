"""
PyTorch RXT Model Architecture: ResNeXt 1D + GRU Sequence Model.
Combines grouped 1D convolutional feature extraction with Gated Recurrent Unit (GRU) temporal modeling.
"""

import torch
import torch.nn as nn

class ResNeXt1DBlock(nn.Module):
    """ResNeXt 1D Residual Block with Grouped Convolutions."""
    def __init__(self, in_channels: int, out_channels: int, groups: int = 4):
        super(ResNeXt1DBlock, self).__init__()
        cardinality_channels = out_channels // 2
        self.conv1 = nn.Conv1d(in_channels, cardinality_channels, kernel_size=1)
        self.bn1 = nn.BatchNorm1d(cardinality_channels)
        self.conv2 = nn.Conv1d(cardinality_channels, cardinality_channels, kernel_size=3, padding=1, groups=groups)
        self.bn2 = nn.BatchNorm1d(cardinality_channels)
        self.conv3 = nn.Conv1d(cardinality_channels, out_channels, kernel_size=1)
        self.bn3 = nn.BatchNorm1d(out_channels)
        self.relu = nn.ReLU(inplace=True)

        self.shortcut = nn.Sequential()
        if in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv1d(in_channels, out_channels, kernel_size=1),
                nn.BatchNorm1d(out_channels)
            )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = self.shortcut(x)
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        out += residual
        return self.relu(out)

class ResNeXtGRU(nn.Module):
    """
    RXT Model Architecture combining ResNeXt grouped feature extraction with GRU temporal modeling.
    """
    def __init__(self, input_dim: int = 16, hidden_dim: int = 64, num_gru_layers: int = 2):
        super(ResNeXtGRU, self).__init__()
        self.input_dim = input_dim
        
        # ResNeXt 1D Feature Extractor
        self.resnext_block = ResNeXt1DBlock(in_channels=1, out_channels=32, groups=4)
        
        # GRU Temporal Layer
        self.gru = nn.GRU(
            input_size=32,
            hidden_size=hidden_dim,
            num_layers=num_gru_layers,
            batch_first=True,
            dropout=0.2 if num_gru_layers > 1 else 0.0
        )
        
        # Risk Classifier Head
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x shape: (batch_size, input_dim)
        # Reshape for 1D convolution: (batch_size, 1, input_dim)
        x_conv = x.unsqueeze(1)
        feat = self.resnext_block(x_conv)  # (batch_size, 32, input_dim)
        
        # Transpose for GRU: (batch_size, sequence_length=input_dim, feature_dim=32)
        gru_in = feat.transpose(1, 2)
        gru_out, _ = self.gru(gru_in)       # (batch_size, seq_len, hidden_dim)
        
        # Pool last time step representation
        last_hidden = gru_out[:, -1, :]
        prob = self.classifier(last_hidden)  # (batch_size, 1)
        return prob.squeeze(-1)
