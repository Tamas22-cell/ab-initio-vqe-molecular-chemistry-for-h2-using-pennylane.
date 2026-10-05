import pennylane as qml
from pennylane import numpy as np
import matplotlib.pyplot as plt

symbols = ["H", "H"]

geometry = np.array(
    [
        [0.0, 0.0, -0.6992],
        [0.0, 0.0,  0.6992],
    ],
    requires_grad=False,
)

hamiltonian, qubits = qml.qchem.molecular_hamiltonian(
    symbols,
    geometry,
    charge=0,
    mult=1,
    basis="sto-3g",
)

electrons = 2
hf_state = qml.qchem.hf_state(electrons, qubits)
singles, doubles = qml.qchem.excitations(electrons, qubits)

dev = qml.device("default.qubit", wires=qubits)

num_params = len(singles) + len(doubles)
params = np.zeros(num_params, requires_grad=True)

@qml.qnode(dev)
def circuit(params):
    qml.BasisState(hf_state, wires=range(qubits))

    index = 0

    for wires in singles:
        qml.SingleExcitation(params[index], wires=wires)
        index += 1

    for wires in doubles:
        qml.DoubleExcitation(params[index], wires=wires)
        index += 1

    return qml.expval(hamiltonian)

optimizer = qml.GradientDescentOptimizer(stepsize=0.2)

max_iterations = 100
energies = []

for iteration in range(max_iterations):
    params, _ = optimizer.step_and_cost(circuit, params)
    energy = circuit(params)
    energies.append(float(energy))

plt.figure(figsize=(9, 5))
plt.plot(range(len(energies)), energies)
plt.xlabel("Iteration")
plt.ylabel("Energy (Hartree)")
plt.title("VQE Convergence for H2")
plt.grid(True)
plt.tight_layout()

plt.savefig("vqe_convergence.png", dpi=300)
plt.show()
