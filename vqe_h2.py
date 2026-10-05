import pennylane as qml
from pennylane import numpy as np

# Molecular geometry: H2
symbols = ["H", "H"]
geometry = np.array([
    [0.0, 0.0, -0.6614],
    [0.0, 0.0,  0.6614],
])

# Build molecular Hamiltonian
hamiltonian, qubits = qml.qchem.molecular_hamiltonian(
    symbols,
    geometry,
    charge=0,
    mult=1,
    basis="sto-3g"
)

print("Number of qubits:", qubits)
print("Hamiltonian:")
print(hamiltonian)

# Quantum device
dev = qml.device("default.qubit", wires=qubits)

# Hartree-Fock reference state for H2
electrons = 2
hf_state = qml.qchem.hf_state(electrons, qubits)

# Excitations
singles, doubles = qml.qchem.excitations(electrons, qubits)

single_wires, double_wires = qml.qchem.excitations_to_wires(
    singles,
    doubles
)

n_params = len(singles) + len(doubles)

# Initial variational parameters
params = np.zeros(n_params, requires_grad=True)

@qml.qnode(dev)
def circuit(params):
    qml.BasisState(hf_state, wires=range(qubits))

    idx = 0

    for wires in single_wires:
        qml.SingleExcitation(params[idx], wires=wires)
        idx += 1

    for wires in double_wires:
        qml.DoubleExcitation(params[idx], wires=wires)
        idx += 1

    return qml.expval(hamiltonian)


# Optimizer
optimizer = qml.GradientDescentOptimizer(stepsize=0.4)

max_iterations = 100
conv_tol = 1e-7

energy = circuit(params)

print("\nStarting VQE optimization...")
print(f"Initial energy: {energy:.8f} Ha")

for iteration in range(max_iterations):
    params, prev_energy = optimizer.step_and_cost(circuit, params)

    energy = circuit(params)
    convergence = np.abs(energy - prev_energy)

    if iteration % 5 == 0:
        print(
            f"Iteration {iteration:3d} | "
            f"Energy = {energy:.8f} Ha | "
            f"ΔE = {convergence:.3e}"
        )

    if convergence <= conv_tol:
        break

print("\nVQE finished")
print(f"Final ground-state energy: {energy:.8f} Ha")
print("Optimized parameters:")
print(params)
