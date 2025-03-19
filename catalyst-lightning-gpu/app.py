import pennylane as qml
import jax.numpy as jnp

import jax

# Set number of wires
num_wires = 25

# Set a random seed
key = jax.random.PRNGKey(0)

dev = qml.device("lightning.gpu", wires=num_wires)


@qml.qjit(autograph=True)
@qml.qnode(dev)
def circuit(params):

    # Apply layers of RZ and RY rotations
    for i in range(num_wires):
        qml.RZ(params[3 * i], wires=[i])
        qml.RY(params[3 * i + 1], wires=[i])
        qml.RZ(params[3 * i + 2], wires=[i])

    return qml.expval(qml.PauliZ(0) + qml.PauliZ(num_wires - 1))


# Initialize the weights
weights = jax.random.uniform(key, shape=(3 * num_wires,), dtype=jnp.float32)

print(circuit(weights))


@qml.qjit(autograph=True)
def workflow(params):
    g = qml.grad(circuit)
    return g(params)


print(workflow(weights))
