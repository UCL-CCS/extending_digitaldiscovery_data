# extending_digitaldiscovery_data

This repository contains supplementary data for the publication "*Extending Quantum Computing through Subspace, Embedding and Classical Molecular Dynamics Techniques*", available on Digital Discovery and [arXiv](https://doi.org/10.48550/arXiv.2505.16796).

The data is structured as follows:
- `input/` - contains the input data and scripts required to run the QM/MM simulation presented in Section 5.
- `quantum/` - contains the Hamiltonian data from the QM/MM simulation and the the scripts for pre- and post-processing circuit executions.
- `plot/` - contains the data and scripts needed to plot Figure 9.
- `requirements.txt` - required python packages to run the scripts in `quantum/` and `plot/`. Set up a new virtual environment and run `pip install -r requirements.txt`. We used python `3.11.9`. For instructions to run the scripts for the QM/MM simulation please see `input/README.md`.
- `LICENSE` - this repository is distributed under the GNU General Public License v2 (GPLv2), because it incorporates code adapted from [LAMMPS](https://github.com/lammps/lammps). In particular, the file `input/run.py` is adapted from the LAMMPS source code. The full GPLv2 license for LAMMPS is included here.
