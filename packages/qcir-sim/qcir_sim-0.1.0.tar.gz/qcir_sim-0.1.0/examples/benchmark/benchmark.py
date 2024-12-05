import argparse

import numpy as np

import qcir_sim

np.random.seed(80)

QUANTUM_GATE_CHOICES = tuple(qcir_sim.GATE_CONFIG.keys())


def parse_args():
    parser = argparse.ArgumentParser(description="Benchmarking the simulation")
    parser.add_argument(
        "--sim-type",
        "-s",
        choices=["tensor", "vector"],
        default="tensor",
        help="Type of simulation",
    )
    parser.add_argument(
        "--disable-binary-lifting",
        "-d",
        action="store_true",
        help="Disable doubling of qubits on each iteration",
    )
    return parser.parse_args()


def get_random_state():
    choice = np.random.choice([0, 1])
    if choice == 0:
        return qcir_sim.zero()
    return qcir_sim.one()


def get_simulator(sim_type: str, qubits) -> qcir_sim.QuantumSimulation:
    if sim_type == "vector":
        return qcir_sim.VectorSimulation(qubits)
    elif sim_type == "tensor":
        return qcir_sim.TensorSimulation(qubits)
    else:
        raise ValueError("Invalid simulation type")


def main():
    args = parse_args()
    sim_type = args.sim_type
    print(f"Using {args.sim_type} simulation")

    try:
        num_qubit = 1
        while True:
            qubits = [get_random_state() for _ in range(num_qubit)]
            sim = get_simulator(sim_type, qubits)
            sim.add_gate("X", 1)

            print(f"Simulated {num_qubit} qubits using {sim_type} simulation")

            if args.disable_binary_lifting:
                num_qubit += 1
            else:
                num_qubit = num_qubit << 1

    except Exception as e:
        print(f"Failed to simulate {num_qubit} qubits using {sim_type} sim: {str(e)}")


if __name__ == "__main__":
    main()
