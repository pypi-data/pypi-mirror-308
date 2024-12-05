import logging
from abc import ABC, abstractmethod
from typing import List

import numpy as np

from qcir_sim.exceptions import (
    GateNotImplemented,
    InsufficientQubitCount,
    InvalidQubitIndex,
)
from qcir_sim.utils import GATE_CONFIG

logger = logging.getLogger("qcir_sim")


class QuantumSimulation(ABC):
    @abstractmethod
    def add_gate(self, gate: str, gate_index: int): ...


class VectorSimulation(QuantumSimulation):
    def __init__(self, qubits: List):
        self.num_qubits = len(qubits)
        self.vector_state = None
        for qubit in qubits:
            qubit_state: np.ndarray = np.array(qubit)
            if self.vector_state is None:
                self.vector_state = qubit_state
            else:
                self.vector_state = np.kron(self.vector_state, qubit_state)  # type: ignore

        if self.vector_state is None:
            error_str = f"Expected atleast one qubit in input. Got {self.num_qubits}"
            raise InsufficientQubitCount(error_str)

        logger.info(f"{self.vector_state=}")

    def add_gate(self, gate: str, gate_index: int):
        if gate_index <= 0 or gate_index > self.num_qubits:
            raise InvalidQubitIndex("Index must be between 1 and self.num_qubits")

        gate_index -= 1
        gate_matrix = self._prepare_gate(gate, gate_index)
        self._execute_gate(gate_matrix)

    def _prepare_gate(self, gate: str, gate_index: int) -> np.ndarray:
        if gate not in GATE_CONFIG:
            error_str = f"Invalid gate name: {gate}. Choices = {GATE_CONFIG.keys()}"
            raise GateNotImplemented(error_str)

        kron_product = GATE_CONFIG[gate] if gate_index == 0 else np.eye(2)
        for i in range(1, self.num_qubits):
            matrix = GATE_CONFIG[gate] if gate_index == i else np.eye(2)
            kron_product = np.kron(kron_product, matrix)

        return kron_product

    def _execute_gate(self, gate_matrix: np.ndarray):
        identity_matrix = np.eye(2)

        if (gate_matrix.shape == identity_matrix).all() and (
            identity_matrix == gate_matrix
        ).all():
            # Single qubit system with quantum wire
            # No need to matrix multiplication
            return

        self.vector_state = np.matmul(gate_matrix, self.vector_state)


class TensorSimulation(QuantumSimulation):
    def __init__(self, qubits) -> None:
        super().__init__()

        match qubits:
            case list():
                self.num_qubits = len(qubits)
                self.tensor_state = np.array(qubits)

            case np.ndarray():
                self.num_qubits = qubits.shape[0]
                self.tensor_state = qubits

            case _:
                logger.error("Invalid qubit type")

        if self.num_qubits < 1:
            error_str = f"Expected atleast one qubit in input. Got {self.num_qubits}"
            raise InsufficientQubitCount(error_str)

    def add_gate(self, gate: str, gate_index: int):
        if gate_index <= 0 or gate_index > self.num_qubits:
            raise InvalidQubitIndex("Index must be between 1 and self.num_qubits")

        gate_index -= 1
        gate_matrix = self._prepare_gate(gate, gate_index)
        self._execute_gate(gate_matrix)

    def _prepare_gate(self, gate: str, gate_index: int) -> np.ndarray:
        if gate not in GATE_CONFIG:
            error_str = f"Invalid gate name: {gate}. Choices = {GATE_CONFIG.keys()}"
            raise GateNotImplemented(error_str)

        expanded_gate = np.empty((0, 2, 2))
        for i in range(0, self.num_qubits):
            matrix = GATE_CONFIG[gate] if gate_index == i else np.eye(2)
            if expanded_gate is None:
                expanded_gate = np.array([expanded_gate])
            else:
                expanded_gate = np.append(expanded_gate, [matrix], axis=0)
            # expanded_gate = np.array([expanded_gate, matrix])

        if expanded_gate is None:
            error_str = "Insufficient qubit count to prepare a Quantum gate"
            raise InsufficientQubitCount(error_str)
        return expanded_gate

    def _execute_gate(self, gate_matrix: np.ndarray):
        identity_matrix = np.eye(2)

        if (gate_matrix.shape == np.array((1, 2, 2))).all() and (
            identity_matrix == gate_matrix
        ).all():
            # Single qubit system with quantum wire
            # No need to matrix multiplication
            return

        # print(self.tensor_state.shape, gate_matrix.shape)
        self.tensor_state = np.einsum("ikj,ik->ij", gate_matrix, self.tensor_state)
