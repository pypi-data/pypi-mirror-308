# QM Simulator as a Service

Run Quantum Machines Qua simulator instances at scale.

## Supported versions
 * v3_2_0 - requires qm-qua v1.2.1a2
 * v3_1_0 - requires qm-qua v1.2.1a1
 * v2_4_0 - requires qm-qua v1.1.7
 * v2_2_2 - requires qm-qua v1.1.3
 * v2_2_0 - requires qm-qua v1.1.2
 * v2_1_3 - requires qm-qua v1.1.0

# Configuration of v3_1_0

The simulated hardware provides 1 controller (con1) with 8 frontend modules (FEM).
The 8 FEMs are split into 4 low frequency (LF, FEM 1 to 4)  and 4 microwave (MW, FEM 5 to 8) modules.

# Authentication

Your QM representative provides you an email and password to access the service.
You can use these credentials to authenticate to the service the following way:

```python
client = QmSaas(email="your@email.com",
                 password="password")
```

# Running your program on a simulator

You can spawn simulators and directly connect to them with your Qua program.

```python
from qm import QuantumMachinesManager, SimulationConfig
from qm.qua import play, program

from qm_saas import QmSaas, QoPVersion

config = {
    # your Qua program configuration
}

client = QmSaas(email="john.doe@quantum-machines.co", password="secret")

with client.simulator(QoPVersion.v2_2_2) as instance:
    print(f"Expires at: {instance.expires_at}")
    
    qmm = QuantumMachinesManager(
        host=instance.host,
        port=instance.port,
        connection_headers=instance.default_connection_headers
    )

    with program() as prog:
        play("playOp", "qe1")

    qm = qmm.open_qm(config)
    job = qm.simulate(prog, SimulationConfig(int(1000)))
```

Wrapping your program in a `with` statement ensures that the simulator is properly cleaned up after the program is done running.