from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

## Circuit
circuit = QuantumCircuit(2, 2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure([0, 1], [0, 1])

## Execution
simulator = AerSimulator(method="statevector", device="GPU")
compiled_circuit = transpile(circuit, simulator)
job = simulator.run(compiled_circuit, shots=1024)
result = job.result()
counts = result.get_counts()

print("Measurement count:", counts)
print(circuit)