## Benchmarking how far can we go simulating on classical computers

Machine Specs: Intel i5 10th Gen with 16GB RAM running on Linux

### Problem: Plot the runtime of your code as a function of the number of qubits.

#### Instructions to run

This script tries to simulate a n-qubit system and apply `2*n` random gates on it. The metrics measured is the time taken by the program to simulate each of these systems.

```sh
python examples/benchmark/speed_test.py
```

Parameters:

1. `--sim-type <tensor | vector> (-s)`: Select the simulation type for the system. Default: tensor
2. `--disable-binary-lifting (-d)`: Do not double the number of qubits on each iteration. Default: False
3. `--no-upper-limit (-u)`: Puts the program to an endless loop trying to simulation every qubit system. Default: False

#### Explanation

Time taken by **vector simulation** to simulate 2\*n random gates on n-qubit system (Not possible to simulate 32-qubit system on this machine):

![Vector Simulation](https://media.discordapp.net/attachments/1050645613114568726/1298715724545523795/image.png?ex=671a92c5&is=67194145&hm=7b75d089b4b8613cd70103bd54bbfb0c062d128102e33b7b9cf1ef38d65b58d2&=&format=webp&quality=lossless&width=254&height=179)

Time taken by **tensor simulation** to simulate 2\*n random gates on n-qubit system (Simulated till the execution time was < 10 sec):

![Tensor Simulation](https://media.discordapp.net/attachments/1050645613114568726/1298715884105502730/image.png?ex=671a92eb&is=6719416b&hm=77108e80145c9035c32a8cdc0e2c07c710170f5a12e233016c2f05b6ca37f159&=&format=webp&quality=lossless&width=271&height=318)

### Problem: How many qubits can you simulate this way?

#### Instructions to run

This script tries to simulate a n-qubit system and apply a single NOT gate on top of the first qubit to demonstrate that it can simulate that system.

```sh
python examples/benchmark/benchmark.py
```

Parameters:

1. `--sim-type <tensor | vector> (-s)`: Select the simulation type for the system. Default: tensor
2. `--disable-binary-lifting (-d)`: Do not double the number of qubits on each iteration. Default: False

#### Explanation

Machine Specs: Intel i5 10th Gen with 16GB RAM running on Linux

On running the **vector simulation**, the program could simulate upto **8 qubits** easily. After that, 16-qubit system could not be allocated due to memory constraints. (This is because for 16-qubits, simulating a not gate will require Kronecker product of 16 2x2 matrices, which roughly takes 32GB of memory).

Whereas, on running the **tensor simulation**, the program could simulate upto **131072 qubits** easily and apply a single NOT gate on the first qubit. Note that this number was measured in a feasible time frame. The number could go higher but will take more time to simulation. While this number seems impressive, introducing more gates will increase the runtime of the program and higher qubit systems may not be computationally feasible on such machine.
