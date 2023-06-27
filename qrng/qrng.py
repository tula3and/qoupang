from qiskit import *

# from qiskit import IBMQ
# IBMQ.save_account('<API Token>')
# provider = IBMQ.load_account()
# backend = IBMQ.get_provider(hub='ibm-q-kaist', group='internal', project='default').backends.ibmq_manhattan
backend = Aer.get_backend('qasm_simulator')

q = QuantumRegister(48)
c = ClassicalRegister(48)

circuit = QuantumCircuit(q,c)
circuit.h(q)

for i in range(47):
    circuit.cx(q[i], q[47])

circuit.measure(q,c)

import string
table = string.ascii_uppercase + string.ascii_lowercase + string.digits

def hash8():
    hash_result = ''
    result = execute(circuit, backend, shots=1).result()
    count = result.get_counts(circuit)
    bits = max(count, key=lambda i: count[i])
    start = 0
    end = 6
    while (end <= 48):
        rand = int(bits[start:end], 2) % len(table)
        start += 6
        end += 6
        hash_result += table[rand]
    return hash_result
