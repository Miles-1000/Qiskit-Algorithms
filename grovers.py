from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
from qiskit.providers.basic_provider import BasicSimulator
from qiskit.visualization import plot_histogram
from qiskit.providers.fake_provider import GenericBackendV2
import math as m
from qiskit_aer import AerSimulator


numBits = 5
qc = QuantumCircuit(numBits + 1, numBits)

mainBits = [i for i in range (numBits)]
allBits = mainBits + [numBits]

qc.x(numBits)
qc.h(allBits)

qc.barrier()

def oracle(key):
    zeros = []

    for i in range(len(key)):
        if key[i] == "0":
            zeros.append(i)
    
    if zeros: qc.x(zeros)
    qc.mcx(mainBits, numBits)
    if zeros: qc.x(zeros)

def EReflection():
    qc.h(mainBits)
    qc.x(mainBits)
    qc.mcx(mainBits, numBits)
    qc.x(mainBits)
    qc.h(mainBits)

for i in range(int(m.floor(m.pi/(4 * m.asin(1/m.sqrt(2**numBits)))))):
    oracle("01110")
    qc.barrier()
    EReflection()
    qc.barrier()

for i in range(numBits):
    qc.measure(i, numBits-i-1)

# print(qc)

qc.draw(output="mpl", initial_state=True)

backend = AerSimulator()
result = backend.run(qc, shots=10000).result()

counts = result.get_counts()

plot_histogram(counts)

plt.show()