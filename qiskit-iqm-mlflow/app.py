import json
import os
import json

import matplotlib.pyplot as plt
import requests
from iqm.iqm_client import IQMClient
from iqm.qiskit_iqm import IQMProvider

import mlflow

from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram


def get_calibration_data(
    client: IQMClient, calibration_set_id=None, filename: str = None
):
    """
    Return the calibration data and figures of merit using IQMClient.
    Optionally you can input a calibration set id (UUID) to query historical results
    Optionally save the response to a json file, if filename is provided
    """
    headers = {"User-Agent": client._signature}
    bearer_token = client._token_manager.get_bearer_token()
    headers["Authorization"] = bearer_token

    if calibration_set_id:
        url = os.path.join(
            client._api.iqm_server_url, "calibration/metrics/", calibration_set_id
        )
    else:
        url = os.path.join(client._api.iqm_server_url, "calibration/metrics/latest")

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # will raise an HTTPError if the response was not ok

    data = response.json()
    data_str = json.dumps(data, indent=4)

    if filename:
        with open(filename, "w") as f:
            f.write(data_str)
        print(f"Data saved to {filename}")

    return data


def plot_metrics(
    metric: str, title: str, ylabel: str, xlabel: str, data: dict, limits: list = []
):
    # Initialize lists to store the values and labels
    values = []
    labels = []

    # Iterate over the calibration data and collect values and labels based on the metric
    for key, metric_data in data["metrics"].items():
        if key.endswith(metric):
            for qb, qb_data in metric_data.items():
                if qb.startswith("QB"):
                    values.append(float(qb_data["value"]))
                    # Extract the qubit label from the key
                    labels.append(qb)

    # Check if values were found for the given metric
    if not values:
        return f"{metric} not in quality metrics set!"

    # Set the width and gap between the bars
    bar_width = 0.4
    # Calculate the positions of the bars
    positions = range(len(values))

    fig = plt.figure(figsize=(10, 7))

    # Plot the values with labels
    plt.bar(positions, values, width=bar_width, tick_label=labels)

    if len(limits) == 2:
        plt.ylim(limits)

    plt.grid(axis="y")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=90)

    plt.tight_layout()
    # plt.show()
    plt.close(fig)
    return fig


def demo_function(backend, shotsAmount=1000):
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
    return result


def main():
    # Create a new MLflow Experiment
    mlflow.set_experiment("Qx VTT IQM Demo")

    # Start a new MLflow run
    with mlflow.start_run():
        mlflow.set_tag("Training info", "Q8s Qiskit Demo")

        provider = IQMProvider("https://qx.vtt.fi/api/devices/demo")
        backend = provider.get_backend()

        shots = 500
        result = demo_function(backend, shots)
        mlflow.log_param("shots", shots)

        mlflow.log_figure(plot_histogram(result.get_counts()), "results.png")

        calibration_set_id = str(result.results[0].calibration_set_id)

        mlflow.log_text(calibration_set_id, "calibration_set_id.txt")

        calibration_data = get_calibration_data(backend.client, calibration_set_id)
        mlflow.log_dict(calibration_data, "calibration_data.json")

        measure_ssro_fidelity = plot_metrics(
            metric="measure_ssro_fidelity",
            title="Single Shot Readout Fidelities",
            xlabel="Qubits",
            ylabel="Success rate",
            data=calibration_data,
            limits=[0.85, 1],
        )
        mlflow.log_figure(measure_ssro_fidelity, "measure_ssro_fidelity.png")

        prx_rb_fidelity = plot_metrics(
            metric="prx_rb_fidelity",
            title="Single-qubit Gate Fidelities",
            xlabel="Qubits",
            ylabel="Fidelities",
            data=calibration_data,
            limits=[0.95, 1],
        )

        mlflow.log_figure(prx_rb_fidelity, "prx_rb_fidelity.png")

        cz_irb_fidelity = plot_metrics(
            metric="cz_irb_fidelity",
            title="CZ Gate Fidelities",
            xlabel="Qubit pairs",
            ylabel="Fidelities",
            data=calibration_data,
            limits=[0.8, 1],
        )
        mlflow.log_figure(cz_irb_fidelity, "cz_irb_fidelity.png")

        clifford_rb_fidelity = plot_metrics(
            metric="clifford_rb_fidelity",
            title="Two-qubit Gates Cliffords Averaged",
            xlabel="Qubits",
            ylabel="Fidelities",
            data=calibration_data,
            limits=[0.7, 1],
        )
        mlflow.log_figure(clifford_rb_fidelity, "clifford_rb_fidelity.png")


main()
