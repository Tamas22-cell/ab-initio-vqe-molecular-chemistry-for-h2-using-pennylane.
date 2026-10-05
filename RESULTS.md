# Results

## VQE Ground-State Energy

This project applies the Variational Quantum Eigensolver (VQE) to estimate the ground-state energy of the H2 molecule using PennyLane.

## Method

- Molecule: H2
- Basis: STO-3G
- Quantum framework: PennyLane
- Optimizer: Gradient Descent
- Quantum device: default.qubit

## Output

The VQE algorithm iteratively minimizes the expectation value of the molecular Hamiltonian until convergence.

Typical final result:

Ground-state energy ≈ -1.13 Hartree

## Files

- `vqe_h2.py` — main VQE implementation
- `vqe_h2.ipynb` — notebook version
- `plot_convergence.py` — convergence visualization
- `requirements.txt` — Python dependencies

## Future Improvements

- Bond-length energy scan
- Potential energy curve
- Advanced optimizers
- Noisy quantum simulation
- Hardware backend execution
