import argparse

import numpy as np

import qcir_sim

np.random.seed(8000)


def parse_args():
    parser = argparse.ArgumentParser(description="Benchmarking the simulation")
    parser.add_argument(
        "--num_samples", "-n", type=int, default=10, help="Number of samples"
    )
    parser.add_argument(
        "--tensor_simulation", "-t", action="store_true", help="Use tensor simulation"
    )
    return parser.parse_args()


def sample_vector_state(sim: qcir_sim.VectorSimulation, num_samples):
    """Sample the state vector of a quantum system"""

    state_vector = sim.vector_state
    # Vector state represents all possible states of a n-qubit system
    # psi^2 represents the probability of each state
    probabilities = np.abs(state_vector) ** 2
    # Each state can be understood as n-digit binary number
    states = np.arange(len(state_vector))
    print(f"Probabilities: {probabilities}")
    for _ in range(num_samples):
        # Draw a random sample with probabilities given by psi^2
        sample = np.random.choice(states, p=probabilities)
        # Binary string representation
        yield format(sample, f"0{sim.num_qubits}b")


if __name__ == "__main__":
    args = parse_args()
    print(f"Using tensor simulation: {args.tensor_simulation}")

    qubits = [qcir_sim.zero(), qcir_sim.one(), qcir_sim.one(), qcir_sim.one()]
    if args.tensor_simulation:
        sim = qcir_sim.TensorSimulation(qubits)
    else:
        sim = qcir_sim.VectorSimulation(qubits)

    # TODO: Playaround with quantum gates by adding here
    sim.add_gate("H", 1)
    sim.add_gate("Z", 2)
    sim.add_gate("phase", 2)
    sim.add_gate("H", 2)
    sim.add_gate("X", 3)

    if args.tensor_simulation:
        # Since the tensor simulation does not describe the probabilities for each state,
        # we need to convert to vector state to get the probabilities
        sim = qcir_sim.VectorSimulation(sim.tensor_state)

    sample_generator = sample_vector_state(sim, args.num_samples)
    for index, sample in enumerate(sample_generator):
        print(f"Sampling {index + 1}/{args.num_samples}: State = {sample}")
