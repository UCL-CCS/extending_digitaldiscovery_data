###
# 1. Read in Hamiltonian and calculate HF energy and FCI energy
# 2. Run DMRG
# 3. Generate QSCI circuits via MPS to circuit mapping
# 4. Run QSCI to get QSCI energies
###

import json
from collections import Counter
import numpy as np
from typing import List
from symmer.operators import PauliwordOp, QuantumState
from symmer.utils import exact_gs_energy
from tn4qa.dmrg import DMRG
from tn4qa.mpo import MatrixProductOperator
from tn4qa.mps import MatrixProductState
from tn4qa.quantum_algorithms.backend.qiskit_simulator import QiskitSimulatorBackend
from mps_to_circuit import MPSAnalyticDecomposition

def read_ham(filename):
    with open(filename, "r") as f:
        ham_dict = json.load(f)
    
    ham_dict = {k:v[0]+1j*v[1] for k,v in ham_dict.items()}
    return ham_dict

def calc_hf_energy(ham_dict, hf_bitstring):
    ham_mpo = MatrixProductOperator.from_hamiltonian(ham_dict)
    hf_mps = MatrixProductState.from_bitstring(hf_bitstring)
    hf_energy = hf_mps.compute_expectation_value(ham_mpo)
    return hf_energy.real

def calc_fci_energy(ham):
    sparse_ham = ham.to_sparse_matrix
    fci_energy, _ = exact_gs_energy(sparse_ham)
    return fci_energy

def run_dmrg(ham, hf_state):
    ham_dict = ham.to_dictionary
    hf_mps = MatrixProductState.from_bitstring(hf_state)
    hf_mps = hf_mps.expand_bond_dimension_list(1, list(range(1, hf_mps.num_sites)))
    dmrg = DMRG(ham_dict, max_mps_bond=2, initial_state=hf_mps)
    energy, mps = dmrg.run(maxiter=10)
    return energy, mps

def build_qsci_circuit(mps):
    circ_builder = MPSAnalyticDecomposition(mps, max_layers=1, target_fidelity=1.0)
    circ = circ_builder.bond_dim_2_to_qc_exact(mps)
    return circ

def simulate_qsci_circuits(qsci_circ, num_samples):
    """Here we provide a simulator but this can be replaced by execution on a real backend."""
    backend = QiskitSimulatorBackend()
    counts = backend.run(qsci_circ, num_samples)
    return counts

def qsci_postprocessing(counts, max_subspace_size, hf_state, ham):

    counts = dict(sorted(counts.items(), key=lambda x:x[1])[::-1])
    configurations, _ = zip(*counts.items())
    configurations = list(configurations[:max_subspace_size])
    if not hf_state in configurations:
        configurations.append(hf_state)

    # Project and diagonalise Hamiltonian
    def matrix_element(hamiltonian: PauliwordOp, i_str: str, j_str: str) -> float:
        psi_i = QuantumState.from_dictionary({i_str:1})
        psi_j = QuantumState.from_dictionary({j_str:1})
        return (psi_i.dagger * hamiltonian * psi_j).real

    def get_selected_configuration_matrix(hamiltonian: PauliwordOp, configs: List[str]) -> np.ndarray[float]:
        """ Constructs the interaction matrix H_ij = <i|H|j>
        """
        matrix = np.zeros((len(configs),len(configs)),dtype=float)
        # this matrix is symmetric, so only build the upper triangle and then mirror
        for i,i_str in enumerate(configs):
            for j,j_str in enumerate(configs[i:]):
                matrix[i,j+i] = matrix_element(hamiltonian, i_str, j_str)
        matrix[np.tril_indices(len(configs), -1)] = matrix.T[np.tril_indices(len(configs), -1)]
        return matrix

    selected_subspace_matrix = get_selected_configuration_matrix(ham, configurations)
    eigvals, _ = np.linalg.eigh(selected_subspace_matrix)
    e0 = eigvals[0]
    return e0


# Example usage
filename = "19_200_mean.json"
ham_dict = read_ham(filename)

hf_state = "1111110000000000"
hf_energy = calc_hf_energy(ham_dict, hf_state)

symmer_ham = PauliwordOp.from_dictionary(ham_dict)
fci_energy = calc_fci_energy(symmer_ham)

dmrg_energy, dmrg_sol = run_dmrg(symmer_ham, hf_state)

qc = build_qsci_circuit(dmrg_sol)

shots = 10**5
counts = simulate_qsci_circuits(qc, shots)
print(counts)

max_subspace_size = 10**3
qsci_energy = qsci_postprocessing(counts, max_subspace_size, hf_state, symmer_ham)

print(filename)
print("HF energy", hf_energy)
print("DMRG energy", dmrg_energy)
print("FCI energy", fci_energy)
print("QSCI energy", qsci_energy)