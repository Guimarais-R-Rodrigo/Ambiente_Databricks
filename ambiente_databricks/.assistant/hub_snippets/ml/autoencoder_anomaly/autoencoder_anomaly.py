"""
Autoencoder para detecção de anomalias (PyTorch).

Uso:
    from hub_snippets.ml.autoencoder_anomaly import train_autoencoder_anomaly
    model, threshold, scores = train_autoencoder_anomaly(X_train_normal, X_test)

Autor: Rodrigo via assistente
Versão: 1.0
"""

from copy import deepcopy

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from typing import Dict, Tuple, Optional
try:
    import mlflow
except ImportError:
    mlflow = None


SEED = 42


class Autoencoder(nn.Module):
    """Autoencoder simétrico para detecção de anomalias."""

    def __init__(self, input_dim: int, encoding_dim: int = 16, hidden_dims: list = None) -> None:
        """
        Args:
            input_dim: Dimensão de entrada.
            encoding_dim: Dimensão do bottleneck.
            hidden_dims: Camadas intermediárias (default: [64, 32]).
        """
        super().__init__()

        if hidden_dims is None:
            hidden_dims = [64, 32]

        # Encoder
        encoder_layers = []
        prev_dim = input_dim
        for h_dim in hidden_dims:
            encoder_layers.extend([nn.Linear(prev_dim, h_dim), nn.ReLU(), nn.BatchNorm1d(h_dim)])
            prev_dim = h_dim
        encoder_layers.append(nn.Linear(prev_dim, encoding_dim))
        self.encoder = nn.Sequential(*encoder_layers)

        # Decoder (espelho)
        decoder_layers = []
        prev_dim = encoding_dim
        for h_dim in reversed(hidden_dims):
            decoder_layers.extend([nn.Linear(prev_dim, h_dim), nn.ReLU(), nn.BatchNorm1d(h_dim)])
            prev_dim = h_dim
        decoder_layers.append(nn.Linear(prev_dim, input_dim))
        self.decoder = nn.Sequential(*decoder_layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


def train_autoencoder_anomaly(
    X_train_normal: np.ndarray,
    X_test: np.ndarray,
    encoding_dim: int = 16,
    epochs: int = 100,
    batch_size: int = 256,
    lr: float = 1e-3,
    patience: int = 10,
    threshold_percentile: float = 95.0,
    log_mlflow: bool = True,
) -> Tuple[Autoencoder, float, np.ndarray]:
    """Treina autoencoder com dados normais e detecta anomalias por erro de reconstrução.

    Args:
        X_train_normal: Dados de treino (APENAS normais).
        X_test: Dados de teste (normais + anômalos).
        encoding_dim: Dimensão do bottleneck.
        epochs: Máximo de epochs.
        batch_size: Tamanho do batch.
        lr: Learning rate.
        patience: Paciência do early stopping.
        threshold_percentile: Percentil para definir threshold.
        log_mlflow: Se True, registra no MLflow.

    Returns:
        Tuple (modelo, threshold, scores do teste).
    """
    X_train_normal = np.asarray(X_train_normal, dtype=np.float32)
    X_test = np.asarray(X_test, dtype=np.float32)
    if X_train_normal.ndim != 2 or X_test.ndim != 2 or X_train_normal.shape[1] != X_test.shape[1]:
        raise ValueError("train and test must be 2-D arrays with the same feature count")
    if len(X_train_normal) < 2 or len(X_test) == 0 or not np.isfinite(X_train_normal).all() or not np.isfinite(X_test).all():
        raise ValueError("train needs at least two finite rows and test must be non-empty and finite")
    if epochs <= 0 or batch_size <= 1 or lr <= 0 or patience <= 0 or not 0 < threshold_percentile < 100:
        raise ValueError("epochs/patience must be positive, batch_size > 1, lr > 0, percentile in (0, 100)")
    torch.manual_seed(SEED)
    np.random.seed(SEED)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    input_dim = X_train_normal.shape[1]
    center = X_train_normal.mean(axis=0)
    scale = X_train_normal.std(axis=0)
    scale[scale == 0] = 1.0
    X_train_scaled = (X_train_normal - center) / scale
    X_test_scaled = (X_test - center) / scale

    model = Autoencoder(input_dim=input_dim, encoding_dim=encoding_dim).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss(reduction="none")

    # DataLoader
    train_tensor = torch.from_numpy(X_train_scaled)
    train_dataset = TensorDataset(train_tensor, train_tensor)
    effective_batch = min(batch_size, len(train_dataset))
    drop_last = len(train_dataset) % effective_batch == 1
    train_loader = DataLoader(train_dataset, batch_size=effective_batch, shuffle=True, drop_last=drop_last)

    # Training
    best_loss = float("inf")
    best_state = deepcopy(model.state_dict())
    patience_counter = 0

    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        for batch_x, _ in train_loader:
            batch_x = batch_x.to(device)
            optimizer.zero_grad()
            output = model(batch_x)
            loss = criterion(output, batch_x).mean()
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        epoch_loss /= len(train_loader)

        if epoch_loss < best_loss:
            best_loss = epoch_loss
            best_state = deepcopy(model.state_dict())
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping at epoch {epoch+1} (best loss: {best_loss:.6f})")
                break

    model.load_state_dict(best_state)
    model.input_center_ = center
    model.input_scale_ = scale
    # Calcular scores (erro de reconstrução) em lotes para limitar memória.
    model.eval()
    def reconstruction_errors(array: np.ndarray) -> np.ndarray:
        dataset = TensorDataset(torch.from_numpy(array))
        loader = DataLoader(dataset, batch_size=min(batch_size, len(dataset)), shuffle=False)
        errors = []
        with torch.no_grad():
            for (batch,) in loader:
                batch = batch.to(device)
                errors.append(criterion(model(batch), batch).mean(dim=1).cpu().numpy())
        return np.concatenate(errors)

    train_errors = reconstruction_errors(X_train_scaled)
    threshold = float(np.percentile(train_errors, threshold_percentile))
    test_errors = reconstruction_errors(X_test_scaled)

    n_anomalies = int((test_errors > threshold).sum())
    print(f"Autoencoder anomaly: threshold={threshold:.6f} (p{threshold_percentile})")
    print(f"  Anomalias no teste: {n_anomalies} ({n_anomalies/len(X_test)*100:.2f}%)")

    if log_mlflow:
        if mlflow is None:
            raise ImportError("mlflow is required when log_mlflow=True")
        mlflow.log_params({"algorithm": "autoencoder", "encoding_dim": encoding_dim, "epochs": epoch+1})
        mlflow.log_metrics({"threshold": threshold, "n_anomalies_test": n_anomalies})

    return model, threshold, test_errors
