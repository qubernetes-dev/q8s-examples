import dynamiqs as dq
import jax.numpy as jnp

# initial state
psi0 = dq.fock(2, 0)

# Hamiltonian
delta = 0.3  # detuning
Omega = 1.0  # Rabi frequency
H = delta * dq.sigmaz() + Omega * dq.sigmax()

print(f"State of type {type(psi0)} and shape {psi0.shape}.")
print(f"Hamiltonian of type {type(H)} and shape {H.shape}.")

# define sampling times
sim_time = 10.0  # total time of evolution
num_save = 101  # number of time slots to save
tsave = jnp.linspace(0.0, sim_time, num_save)  # can also be a list or a NumPy array

# define list of observables
exp_ops = [dq.sigmaz()]  # expectation value of sigma_z

# define method (Dormand-Prince method of order 5)
method = dq.method.Dopri5(rtol=1e-6, atol=1e-8)

# run simulation
result = dq.sesolve(H, psi0, tsave, exp_ops=exp_ops, method=method)

# print some information
print(f"`result` is of type {type(result)}.")
print(f"`result` has the following attributes:")
print(f"{[attr for attr in dir(result) if not attr.startswith('__')]}\n")
print(result)
