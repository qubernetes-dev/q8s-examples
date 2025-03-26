# Introduction

This experiment facilitates running a simple Qiskit circuit in a Qubernetes cluster using the Qiskit Aer simulator. The simulator can run on CPU or on GPU.

## Prerequisites

- Docker installed
- Docker Hub account (update the username in `Q8Sproject`)
  ```yaml
  docker:
    username: your-dockerhub-username
  ```
- Kubeconfig file for a Qubernetes cluster (update the path in `Q8Sproject`)
  ```yaml
  kubeconfig: /path/to/your/kubeconfig
  ```

## Setup

1. Create virtual environment and install `q8sctl`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install q8s
```

2. Build the Docker images:

```bash
q8sctl build --init
```

3. Run the experiment:

```bash
q8sctl execute app.py
```

## Take it further

The circuit included in this experiment is a barebone quantum circuit. You can add more dependencies and make it more complex.
