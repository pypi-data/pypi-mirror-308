## Benchmarking how far can we go simulating on classical computers

**Problem:** How about computing exact expectation values in the form `<Ψ| Op |Ψ>`?

### Instructions to run

This script tries to simulate a 3-qubit system (011) and applies three different gates on the three qubits. Then we take `Op` as the Hadamard gate on the first qubit.

```sh
python examples/benchmark/speed_test.py
```

Parameters:

1. `--sim-type <tensor | vector> (-s)`: Select the simulation type for the system. Default: vector

### Explanation

In quantum mechanics, the expectation value of any operator for any normalized vector `Ψ` is given by `<Ψ| Op |Ψ>`. Ref: [Expectation value](<https://en.wikipedia.org/wiki/Expectation_value_(quantum_mechanics)>)

So, first we need to normalize the state of the quantum system (tensor or vector states).

To measure the expectation values of the `<Ψ| Op |Ψ>`. We need to prepare `Op` for the 3-qubit system here where the other two qubits can be applied a quantum wire or Identity matrix. The given expression can be understood as two parts:

1. `<Ψ|` as the hermitian conjugate of `|Ψ>` -> complex conjugate of transpose of `|Ψ>`
2. `Op |Ψ>` as the `Op` multiplied with `psi` -> applying the operator on `|Ψ>` normally

Once we get these two, we take the inner product of these two matrices we get from the above steps to get the expectation value.
