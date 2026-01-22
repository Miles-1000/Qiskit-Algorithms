from collections import Counter
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

import matplotlib.pyplot as plt

q_reg = QuantumRegister(3, 'q')

c_reg = ClassicalRegister(3, 'c')

qc = QuantumCircuit(q_reg, c_reg)

# Choose your probability
desired_prob_1 = 0.3

# Compute the angle θ such that P(1) = sin²(θ/2) = desired_prob_1
theta = 2 * np.arcsin(np.sqrt(desired_prob_1))

# Apply Ry(θ) gate to rotate the qubit
qc.ry(theta, 0)


qc.barrier()

qc.h(1)
qc.cx(1,2)

qc.barrier()

qc.cx(0,1)

qc.measure(0,1)
qc.measure(1,0)

with qc.if_test((c_reg[0], 1)):
    qc.x(q_reg[2])

with qc.if_test((c_reg[1], 1)):
    qc.z(q_reg[2])

qc.measure(2, 2)

qc.draw(output="mpl", initial_state=True)

backend = AerSimulator()
result = backend.run(qc, shots=1000000).result()

counts = result.get_counts()

single_bit_counts = Counter(bitstring[0] for bitstring in counts for _ in range(counts[bitstring]))

plot_histogram(single_bit_counts)

plt.show()