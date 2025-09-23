import numpy as np
import pickle
import json

files = [
    '19_200.pkl',
    '19_275.pkl',
    '19_350.pkl',
    '19_425.pkl',
    '19_500.pkl',
    '26_200.pkl',
    '26_275.pkl',
    '26_350.pkl',
    '26_425.pkl',
    '26_500.pkl',
    '33_200.pkl',
    '33_275.pkl',
    '33_350.pkl',
    '33_425.pkl',
    '33_500.pkl'
]

for file in files:
    with open(file, 'rb') as infile:
        data = pickle.load(infile)

    n_start = 3

    print(file)
    for index, step in enumerate(data):
        print(step, len(data[step]))
        if index == n_start:
            print('----------')

    start_qham = ''.join([str(n_start), '_ham'])

    all_coeffs = {}

    all_paulis_list = []

    for ham in data:
        for pauli in data[ham]:
            if pauli not in all_paulis_list:
                all_paulis_list.append(pauli)

    for pauli in all_paulis_list:
        all_coeffs[pauli] = []

    for i, ham in enumerate(data):
        if i > n_start:
            for pauli in all_paulis_list:
                if pauli in data[ham]:
                    all_coeffs[pauli].append(data[ham][pauli][0])
                else:
                    all_coeffs[pauli].append(0.0)

    mean_ham = {}

    for pauli in all_coeffs:
        real = np.array(all_coeffs[pauli])
        real_mean = np.mean(real)
        mean_ham[pauli] = (np.mean(real), 0.0)

    fname = file[:-4] + '_mean.json'

    with open(fname, 'w') as outfile:
        json.dump(mean_ham, outfile)
