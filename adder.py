from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
from qiskit.providers.basic_provider import BasicSimulator
from qiskit.visualization import plot_histogram
from qiskit.providers.fake_provider import GenericBackendV2

qc = QuantumCircuit(4, 2)

toAdd = [1, 0]

if toAdd[0]: qc.x(0)
if toAdd[1]: qc.x(1)

qc.barrier()

qc.cx(0,2)
qc.cx(1,2)
qc.ccx(0,1,3)

qc.barrier()

qc.measure(2,0)
qc.measure(3,1)

qc.draw(output="mpl", initial_state=True)

backend = GenericBackendV2(num_qubits=4)
transpiled_circuit = transpile(qc, backend)

result = backend.run(transpiled_circuit).result()

counts = result.get_counts()
plot_histogram(counts)

plt.show()