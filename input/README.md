# input/

This folder contains the data and scripts required to run the QM/MM simulation presented in Section 5.

A prerequisite is the installation of LAMMPS with the `mdi`, `molecule`, and `kspace` flags switched on. Instructions for this can be found in the [LAMMPS documentation](https://github.com/lammps/lammps/blob/0d479cae298abb73ffd8b1460197a8a74c63bc5e/examples/QUANTUM/PySCF/README). We recommend that you set this up in a new virtual environment, with the required python version `>=3.8, <3.11`. You will also need to install Nbed version 0.0.7 after completing the LAMMPS installation via `pip install nbed==0.0.7`.

Then, the script `run.sh` should be executable and can be edited to run simulations for each of the starting geometries. The LAMMPS input geometries are found in the `data.*` files. For example, `data.19_200` corresponds to the geometry for $d_{\mathrm{OO}} = 1.9$ Å and $d_{\mathrm{OH}} = 0.200$, and similarly for the other files. The output from running the script will be the Hamiltonian data in a pickle file.
