from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
from qiskit.providers.basic_provider import BasicSimulator
from qiskit.visualization import plot_histogram
from qiskit.providers.fake_provider import GenericBackendV2
import math as m
from qiskit_aer import AerSimulator


numBits = 7
qc = QuantumCircuit(numBits + 1, numBits)

mainBits = [i for i in range (numBits)]
allBits = mainBits + [numBits]

qc.x(numBits)
qc.h(allBits)

qc.barrier()


def oracle():
    qc.x([1,3,4,5,6])
    qc.mcx([0,1,3,4,5,6], 7)
    qc.x(1)
    qc.mcx([1,2,3,4,5,6], 7)
    qc.x([3,4,5,6])

def EReflection():
    qc.h(mainBits)
    qc.x(mainBits)
    qc.mcx(mainBits, numBits)
    qc.x(mainBits)
    qc.h(mainBits)

for i in range(int(m.floor((m.pi/4) * m.sqrt(numBits/4)))):
    oracle()
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

reduced_counts = {}

for full_result, count in counts.items():
    firstBits = full_result[:3]

    if firstBits in reduced_counts:
        reduced_counts[firstBits] += count
    else:
        reduced_counts[firstBits] = count


plot_histogram(reduced_counts)

plt.show()