# Introduction

This experiment demonstrates how to retrieve matplotlib plots from Qubernetes job runs.

## Prerequisites

- Docker installed
- Docker Hub account (update the username in `Q8Sproject`)
- Kubeconfig file for a Qubernetes cluster (update the path in `Q8Sproject`)

## Setup

1. Create virtual environment and install `q8sctl` and `jupyter`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install q8s jupyter
```

2. Build the Docker images:

```bash
q8sctl build --init
```

3. Run the experiment:

```bash
q8sctl jupyter --install
```
