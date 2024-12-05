from typing import Dict

import numpy as np


def zero():
    return np.array([1, 0])


def one():
    return np.array([0, 1])


GATE_CONFIG: Dict[str, np.ndarray] = {
    "X": np.array([[0, 1], [1, 0]]),
    "Y": np.array([[0, -1j], [1j, 0]]),
    "Z": np.array([[1, 0], [0, -1]]),
    "H": 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]]),
    "phase": np.array([[1, 0], [0, 1j]]),
    "T": np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]]),
}


GATE_CONFIG["not"] = GATE_CONFIG["X"]
GATE_CONFIG["hadamard"] = GATE_CONFIG["H"]
