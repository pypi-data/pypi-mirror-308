import qcir_sim, argparse
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description="Benchmarking the simulation")
    parser.add_argument(
        "--sim-type",
        "-s",
        choices=["tensor", "vector"],
        default="vector",
        help="Type of simulation",
    )
    return parser.parse_args()


def get_random_state():
    choice = np.random.choice([0, 1])
    if choice == 0:
        return qcir_sim.zero()
    return qcir_sim.one()


def vector_expectation_value(sim: qcir_sim.VectorSimulation, gate: str, gate_idx: int):
    psi = sim.vector_state
    psi /= np.linalg.norm(psi)
    Op = sim._prepare_gate(gate, gate_idx)

    op_mul_psi = Op @ psi
    bra_notation = np.conjugate(np.transpose(psi))

    expectation_value = bra_notation @ op_mul_psi
    print(f"Expectation Value: {expectation_value}")


def tensor_expectation_value(sim: qcir_sim.TensorSimulation, gate: str, gate_idx: int):
    psi = sim.tensor_state
    psi /= np.linalg.norm(psi)
    Op = sim._prepare_gate(gate, gate_idx)

    op_mul_psi = np.einsum("ikj,ik->ij", Op, psi)
    bra_notation = np.conjugate(np.transpose(psi))

    expectation_value = np.einsum("ij,ji", bra_notation, op_mul_psi)
    print(f"Expectation Value: {expectation_value}")


if __name__ == "__main__":
    args = parse_args()
    simulation_type = args.sim_type
    print(f"Using {simulation_type} simulation")

    qubits = [qcir_sim.zero(), qcir_sim.one(), qcir_sim.one()]
    if args.sim_type == "tensor":
        sim = qcir_sim.TensorSimulation(qubits)
    else:
        sim = qcir_sim.VectorSimulation(qubits)

    sim.add_gate("H", 1)
    sim.add_gate("phase", 2)
    sim.add_gate("H", 3)

    if args.sim_type == "tensor":
        tensor_expectation_value(sim, "H", 1)
    else:
        vector_expectation_value(sim, "H", 1)
