from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import mlflow

mlflow.set_experiment("sample-experiment")
with mlflow.start_run():
    ## Circuit
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])

    ## Execution
    simulator = AerSimulator(method="statevector", device="CPU")
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()

    mlflow.log_param("measurement_counts", counts)
    mlflow.log_metric("count_11", counts.get("11", 0))

    print("Measurement count:", counts)
    print(circuit)