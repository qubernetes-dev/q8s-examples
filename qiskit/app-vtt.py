from qiskit import QuantumCircuit, transpile
from iqm.qiskit_iqm import IQMProvider


def demo_function(shotsAmount=1000):
    provider = IQMProvider("https://qx.vtt.fi/api/devices/demo")
    backend = provider.get_backend()

    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])

    compiled_circuit = transpile(circuit, backend)
    job = backend.run(compiled_circuit, shots=shotsAmount)
    result = job.result()
    counts = result.get_counts()

    print("Total count for 00 and 11 are:", counts)
    print(circuit)


result = demo_function(1000)
