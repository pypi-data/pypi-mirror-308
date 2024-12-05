import argparse
import time

import numpy as np
import pandas as pd

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
    parser.add_argument(
        "--no-upper-limit",
        "-u",
        action="store_true",
        help="No upper limit on qubit count",
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


def simulate_system(sim_type, num_qubit):
    try:
        qubits = [get_random_state() for _ in range(num_qubit)]
        sim = get_simulator(sim_type, qubits)

        # We will add 2*num_qubit gates to the system
        for _ in range(num_qubit << 1):
            gate = np.random.choice(QUANTUM_GATE_CHOICES)
            qubit_index = np.random.randint(1, num_qubit + 1)

            sim.add_gate(gate, qubit_index)

    except Exception as e:
        print(f"Failed to simulate {num_qubit} qubits using {sim_type} sim: {str(e)}")
        return


def main():
    run_times = []
    args = parse_args()

    sim_type = args.sim_type
    print(f"Using {args.sim_type} simulation")

    max_qubits = 1
    while True:
        start_time = time.time()
        simulate_system(sim_type, max_qubits)
        end_time = time.time()

        time_diff = end_time - start_time
        run_times.append({"num qubit": max_qubits, "time_sec": time_diff})
        print(f"{max_qubits} qubits using {sim_type} sim in {time_diff} seconds")

        if not args.no_upper_limit and time_diff > 10:
            break

        if args.disable_binary_lifting:
            max_qubits += 1
        else:
            max_qubits = max_qubits << 1

    metrics = pd.DataFrame(run_times).set_index("num qubit")
    print(metrics)
    metrics.to_csv(f"{sim_type}_{max_qubits}_qubits.csv")


if __name__ == "__main__":
    main()
