from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Node:
    """Decision tree node."""
    feature: int = None
    threshold: float = None
    n_samples: int = None
    left: Node = None
    right: Node = None
    mse: float = None
    value: int = None