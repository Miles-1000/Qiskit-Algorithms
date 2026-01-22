import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit.circuit.library import *

import matplotlib.pyplot as plt

qc = QuantumCircuit(3, 3)


# Main Circuit
qc.h(0)

csGate = SGate().control(1)
ctGate = TGate().control(1)

qc.append(csGate, [1, 0])
qc.append(ctGate, [2, 0])
qc.h(1)
qc.append(csGate, [2, 1])
qc.h(2)
qc.swap(0,2)


qc.draw(output="mpl", initial_state=True)

# Measure
for i in range(3):
    qc.measure(i, 2-i)

# Decompose into supported basis gates
qc_decomposed = transpile(qc, AerSimulator(), basis_gates=['u1','u2','u3','cx','id'])

# Testing
backend = AerSimulator()
result = backend.run(qc_decomposed, shots=1000).result()

counts = result.get_counts()

plot_histogram(counts)

plt.show()