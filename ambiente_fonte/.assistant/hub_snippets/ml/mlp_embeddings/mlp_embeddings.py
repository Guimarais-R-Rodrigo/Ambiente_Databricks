"""
MLP com embeddings categóricas (PyTorch).

Uso:
    from hub_snippets.ml.mlp_embeddings import EmbeddingMLP, train_embedding_mlp

Autor: Rodrigo via assistente
Versão: 1.0
"""

from copy import deepcopy

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from typing import Dict, List, Tuple, Optional
from sklearn.metrics import roc_auc_score
try:
    import mlflow
except ImportError:
    mlflow = None


SEED = 42


class EmbeddingMLP(nn.Module):
    """MLP com embedding layers para features categóricas."""

    def __init__(
        self,
        n_numeric: int,
        cat_dims: List[int],
        emb_dims: Optional[List[int]] = None,
        hidden_layers: Optional[List[int]] = None,
        dropout: float = 0.3,
        task: str = "binary",
    ):
        """
        Args:
            n_numeric: Número de features numéricas.
            cat_dims: Lista com cardinalidade de cada feature categórica.
            emb_dims: Dimensão do embedding para cada categórica (default: min(50, (c+1)//2)).
            hidden_layers: Tamanhos das camadas ocultas.
            dropout: Taxa de dropout.
            task: 'binary' ou 'regression'.
        """
        super().__init__()

        hidden_layers = [256, 128, 64] if hidden_layers is None else list(hidden_layers)
        if task not in {"binary", "regression"}:
            raise ValueError("task must be 'binary' or 'regression'")
        if len(cat_dims) == 0 or any(value <= 0 for value in cat_dims):
            raise ValueError("cat_dims must contain positive cardinalities")
        if emb_dims is None:
            emb_dims = [min(50, (c + 1) // 2) for c in cat_dims]

        # Embedding layers
        self.embeddings = nn.ModuleList([
            nn.Embedding(cat_dim, emb_dim)
            for cat_dim, emb_dim in zip(cat_dims, emb_dims)
        ])

        # Input dimension
        total_emb_dim = sum(emb_dims)
        input_dim = n_numeric + total_emb_dim

        # Hidden layers
        layers = []
        prev_dim = input_dim
        for h_dim in hidden_layers:
            layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.BatchNorm1d(h_dim),
                nn.ReLU(),
                nn.Dropout(dropout),
            ])
            prev_dim = h_dim

        # Output
        if task == "binary":
            layers.append(nn.Linear(prev_dim, 1))
            layers.append(nn.Sigmoid())
        else:
            layers.append(nn.Linear(prev_dim, 1))

        self.network = nn.Sequential(*layers)
        self.task = task

    def forward(self, x_num: torch.Tensor, x_cat: List[torch.Tensor]) -> torch.Tensor:
        """Forward pass.

        Args:
            x_num: Tensor de features numéricas [batch, n_numeric].
            x_cat: Lista de tensores categóricos [batch] cada.

        Returns:
            Output [batch, 1].
        """
        emb_outputs = [emb(x_cat[i]) for i, emb in enumerate(self.embeddings)]
        x = torch.cat([x_num] + emb_outputs, dim=1)
        return self.network(x)


def train_embedding_mlp(
    X_num_train: np.ndarray,
    X_cat_train: List[np.ndarray],
    y_train: np.ndarray,
    X_num_val: np.ndarray,
    X_cat_val: List[np.ndarray],
    y_val: np.ndarray,
    cat_dims: List[int],
    epochs: int = 50,
    batch_size: int = 512,
    lr: float = 1e-3,
    patience: int = 10,
    log_mlflow: bool = True,
) -> Tuple[EmbeddingMLP, Dict[str, float]]:
    """Treina MLP com embeddings.

    Args:
        X_num_train: Features numéricas de treino.
        X_cat_train: Lista de arrays categóricos de treino.
        y_train: Target de treino.
        X_num_val: Features numéricas de validação.
        X_cat_val: Lista de arrays categóricos de validação.
        y_val: Target de validação.
        cat_dims: Cardinalidade de cada feature categórica.
        epochs: Máximo de epochs.
        batch_size: Tamanho do batch.
        lr: Learning rate.
        patience: Paciência do early stopping.
        log_mlflow: Se True, registra no MLflow.

    Returns:
        Tuple (modelo, métricas).
    """
    X_num_train = np.asarray(X_num_train, dtype=np.float32)
    X_num_val = np.asarray(X_num_val, dtype=np.float32)
    y_train = np.asarray(y_train, dtype=np.float32).reshape(-1)
    y_val = np.asarray(y_val, dtype=np.float32).reshape(-1)
    if X_num_train.ndim != 2 or X_num_val.ndim != 2 or X_num_train.shape[1] != X_num_val.shape[1]:
        raise ValueError("numeric train/validation arrays must be 2-D with matching columns")
    if len(X_num_train) != len(y_train) or len(X_num_val) != len(y_val) or len(y_train) < 2 or len(y_val) < 2:
        raise ValueError("features and labels must align and each split needs at least two rows")
    if len(X_cat_train) != len(cat_dims) or len(X_cat_val) != len(cat_dims):
        raise ValueError("one categorical array is required for each cat_dims entry")
    train_cat = np.column_stack([np.asarray(values).reshape(-1) for values in X_cat_train]).astype(np.int64)
    val_cat = np.column_stack([np.asarray(values).reshape(-1) for values in X_cat_val]).astype(np.int64)
    if len(train_cat) != len(y_train) or len(val_cat) != len(y_val):
        raise ValueError("categorical arrays must align with labels")
    for index, cardinality in enumerate(cat_dims):
        if (train_cat[:, index] < 0).any() or (train_cat[:, index] >= cardinality).any() or (val_cat[:, index] < 0).any() or (val_cat[:, index] >= cardinality).any():
            raise ValueError(f"categorical feature {index} has an index outside [0, {cardinality})")
    if not np.isin(y_train, [0, 1]).all() or np.unique(y_train).size != 2 or not np.isin(y_val, [0, 1]).all():
        raise ValueError("binary MLP requires labels 0/1 and both classes in training")
    if epochs <= 0 or batch_size <= 1 or patience <= 0 or lr <= 0:
        raise ValueError("epochs/patience/lr must be positive and batch_size > 1")
    if not np.isfinite(X_num_train).all() or not np.isfinite(X_num_val).all():
        raise ValueError("numeric features must be finite")
    torch.manual_seed(SEED)
    np.random.seed(SEED)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = EmbeddingMLP(
        n_numeric=X_num_train.shape[1],
        cat_dims=cat_dims,
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.BCELoss()
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5)

    best_auc = 0
    best_state = deepcopy(model.state_dict())
    patience_counter = 0

    train_dataset = TensorDataset(
        torch.from_numpy(X_num_train), torch.from_numpy(train_cat), torch.from_numpy(y_train)
    )
    effective_batch = min(batch_size, len(train_dataset))
    train_loader = DataLoader(
        train_dataset,
        batch_size=effective_batch,
        shuffle=True,
        drop_last=len(train_dataset) % effective_batch == 1,
    )

    for epoch in range(epochs):
        model.train()
        for x_num_t, x_cat_t, y_t in train_loader:
            x_num_t, x_cat_t, y_t = x_num_t.to(device), x_cat_t.to(device), y_t.to(device)
            optimizer.zero_grad()
            output = model(x_num_t, [x_cat_t[:, i] for i in range(x_cat_t.shape[1])]).reshape(-1)
            loss = criterion(output, y_t)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

        # Validation
        model.eval()
        with torch.no_grad():
            x_num_v = torch.from_numpy(X_num_val).to(device)
            x_cat_v = torch.from_numpy(val_cat).to(device)
            val_output = model(x_num_v, [x_cat_v[:, i] for i in range(x_cat_v.shape[1])]).reshape(-1).cpu().numpy()
            val_auc = roc_auc_score(y_val, val_output)

        scheduler.step(1 - val_auc)

        if val_auc > best_auc:
            best_auc = val_auc
            best_state = deepcopy(model.state_dict())
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping at epoch {epoch+1} (best AUC: {best_auc:.4f})")
                break

    model.load_state_dict(best_state)
    metrics = {"auc_val": best_auc, "gini_val": 2 * best_auc - 1, "epochs_trained": epoch + 1}

    if log_mlflow:
        if mlflow is None:
            raise ImportError("mlflow is required when log_mlflow=True")
        mlflow.log_params({"algorithm": "mlp_embeddings", "lr": lr, "epochs": epoch + 1})
        mlflow.log_metrics(metrics)

    return model, metrics
