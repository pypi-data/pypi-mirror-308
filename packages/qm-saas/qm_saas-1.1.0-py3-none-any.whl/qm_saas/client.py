import datetime

import deprecation
from enum import Enum
import logging
import re

from qm_saas.api import Client

_AUTHORIZATION_TOKEN_HEADER_NAME = "simulation-auth"
_AUTHORIZATION_ID_HEADER_NAME = "simulation-id"
_FEM_MIN_SLOT = 1
_FEM_MAX_SLOT = 8


class QoPVersion(Enum):
    """
    Quantum Operating Platform (QoP) versions.
    """
    # An enum of the available QoP Versions
    v3_2_0 = "v3_2_0"
    v3_1_0 = "v3_1_0"
    v2_4_0 = "v2_4_0"
    v2_2_2 = "v2_2_2"
    v2_2_0 = "v2_2_0"
    v2_1_3 = "v2_1_3"


class FemType(Enum):
    """
    Front-End Module (FEM) types.
    """
    MW_FEM = "MW_FEM"
    LF_FEM = "LF_FEM"


class ControllerConfig:
    def __init__(self):
        self._slots = dict()

    """
    Add LF FEMs to numbered slots in the cluster configuration.
    """
    def lf_fems(self, *slots: int):
        for slot in slots:
            self._add_slot(slot, FemType.LF_FEM)
        return self

    """
    Add MW FEMs to numbered slots in the cluster configuration.
    """
    def mw_fems(self, *slots: int):
        for slot in slots:
            self._add_slot(slot, FemType.MW_FEM)
        return self

    def _add_slot(self, slot: int, fem_type: FemType):
        key = f"{slot}"
        if key in self._slots.keys():
            raise ValueError(f"Slot number {key} is already configured as {self._slots[key]}")

        if _FEM_MIN_SLOT <= slot <= _FEM_MAX_SLOT:
            self._slots[key] = fem_type.value
        else:
            raise ValueError(f"Invalid slot number {key}, must be [{_FEM_MIN_SLOT}, {_FEM_MAX_SLOT}]")

    @property
    def slots(self) -> dict:
        return self._slots


class ClusterConfig:
    def __init__(self):
        self._controllers = dict()

    def controller(self) -> ControllerConfig:
        if len(self._controllers) != 0:
            raise ValueError("Only one controller is supported")
        con = f"con{len(self._controllers) + 1}"

        pattern = re.compile("^con(\\d+)$")
        match = pattern.fullmatch(con)
        if match is None:
            raise ValueError(f"Invalid controller name {con}; expecting 'con\\d+'")

        return self._controller(con)

    def _controller(self, con: str) -> ControllerConfig:
        if con in self._controllers.keys():
            raise ValueError(f"Controller {con} already exists")
        controller_config = ControllerConfig()
        self._controllers[con] = controller_config
        return controller_config

    @property
    def controllers(self) -> dict:
        return self._controllers

    def to_dict(self) -> dict:
        return {
            "controllers": {k: {"slots": v.slots} for k, v in self._controllers.items()}
        }


class QmSaasInstance:
    """
    Represents the simulator instance on the cloud.
    """

    def __init__(self, client: Client, version: QoPVersion, cluster_config=None, auto_cleanup: bool = True, log: logging.Logger = None):
        self._client = client
        self._version = version
        self._cluster_config = cluster_config
        self._spawned = False
        self._auto_cleanup = auto_cleanup
        self._port = None
        self._host = None
        self._expires_at = None
        self._id = None
        self._token = None
        self._log = log or logging.getLogger(__name__)

    def __enter__(self):
        self.spawn()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self._auto_cleanup:
            self._log.debug("Skipping close as auto_cleanup is disabled")
            return
        self.close()

    def spawn(self):
        """
        Spawns the simulator instance on the QoPSaaS platform.
        This is a blocking operation.

        The simulator is spawned only once, subsequent calls to this method
        will not spawn a new simulator.
        """
        if not self._spawned:
            self._create_simulator(self._version, self._cluster_config)
            self._spawned = True

    def close(self):
        """
        Destroy the remote simulator and close the session.
        This operation is idempotent and can be called multiple times.
        """
        if not self._spawned:
            self._log.debug("Simulator was not spawned, nothing to close")
            return

        self._log.debug(f"Closing simulator with ID {self._id}")
        self._client.close_simulator(self._id)

        self._log.info("Simulator closed successfully")
        self._spawned = False
        self._host = None
        self._port = None
        self._expires_at = None
        self._id = None
        self._token = None

    def _create_simulator(self, version: QoPVersion, cluster_config=None):
        if version is None:
            raise ValueError("Version must be provided")

        self._log.debug(f"Creating simulator with version {self._version}")
        response = self._client.launch_simulator(version.value, cluster_config.to_dict() if cluster_config else {})

        self._id = response["id"]
        self._token = response["token"]
        self._host = response["host"]
        self._port = response["port"]
        self._expires_at = datetime.datetime.fromisoformat(response["expires_at"])
        self._log.info(f"Simulator created with id {self._id} at {self._host}:{self._port}")

    @property
    @deprecation.deprecated(details="Will be remove in the next version.")
    def qm_manager_parameters(self):
        if not self._spawned:
            raise ValueError("Simulator is not spawned")
        return dict(host=self._host, port=self._port, sim_id=self._id, sim_token=self._token)

    @property
    def default_connection_headers(self):
        return {
            _AUTHORIZATION_ID_HEADER_NAME: self._id,
            _AUTHORIZATION_TOKEN_HEADER_NAME: self._token
        }

    @property
    @deprecation.deprecated(details="Use 'token' instead")
    def sim_token(self):
        return self._token

    @property
    @deprecation.deprecated(details="Use 'id' instead")
    def sim_id(self):
        return self._id

    @property
    @deprecation.deprecated(details="Use 'host' instead")
    def sim_host(self):
        return self._host

    @property
    @deprecation.deprecated(details="Use 'port' instead")
    def sim_port(self):
        return self._port

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def id(self) -> str:
        return self._id

    @property
    def token(self) -> str:
        return self._token

    @property
    def expires_at(self) -> datetime.datetime:
        return self._expires_at

    @property
    def is_alive(self) -> bool:
        now = datetime.datetime.utcnow()
        if self._expires_at is None:
            return False
        else:
            return now < self._expires_at

    @property
    def is_spawned(self) -> bool:
        return self._spawned

    @property
    def cluster_config(self):
        return self._cluster_config.controllers if self._cluster_config else None


@deprecation.deprecated(details="Use qm_saas.QmSaasInstance instead")
class QoPSaaSInstance(QmSaasInstance):
    def __init__(self, client: Client, version: QoPVersion, cluster_config=None, auto_cleanup: bool = True, log: logging.Logger = None):
        super().__init__(client, version, cluster_config, auto_cleanup, log)


class QmSaas:
    """
    Create a simulator instance on the cloud platform.

    host: host of the endpoint of the cloud platform api
    port: port of the endpoint of the cloud platform api
    version: the QOP version of the simulator to use
    email: the email of the user
    password: the password of the user
    auto_cleanup: automatically delete the simulator instance when the context manager exits
                 otherwise it will be left running and timeout after a configurable lifetime
    """

    def __init__(
        self,
        host: str = "qm-saas.quantum-machines.co",
        port: int = 443,
        email: str = None,
        password: str = None,
        auto_cleanup: bool = True,
        log: logging.Logger = None,
    ):
        self.log = log or logging.getLogger(__name__)
        self.auto_cleanup = auto_cleanup
        self._client = Client(
            protocol="https",
            host=host,
            port=port,
            email=email,
            password=password,
            log=self.log
        )

    def simulator(self, version: QoPVersion, cluster_config=None) -> QmSaasInstance:
        """
        version: the QOP version of the simulator to use
        cluster_config: the FEM configuration of the cluster for QoP v3.x.x
        """
        if cluster_config is not None and version is not QoPVersion.v3_1_0:
            raise ValueError("Cluster configuration is only supported for QoP v3.x.x")

        return QoPSaaSInstance(
            auto_cleanup=self.auto_cleanup,
            client=self._client,
            version=version,
            cluster_config=cluster_config,
            log=self.log,
        )

    """
    Close all simulators of the authenticated user.
    """
    def close_all(self):
        self._client.close_all_simulators()

    @property
    def port(self):
        return self._client.port

    @property
    def host(self):
        return self._client.host


@deprecation.deprecated(details="Use qm_saas.QmSaas instead")
class QoPSaaS(QmSaas):
    def __init__(
        self,
        host: str = "qm-saas.quantum-machines.co",
        port: int = 443,
        email: str = None,
        password: str = None,
        auto_cleanup: bool = True,
        log: logging.Logger = None,
    ):
        super().__init__(host, port, email, password, auto_cleanup, log)
