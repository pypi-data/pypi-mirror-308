import logging

from typing import Any, Dict, Type

from snowflake.core import Root
from snowflake.core.database import Database
from snowflake.core.schema import Schema
from snowflake.core.warehouse import Warehouse
from snowflake.demos._constants import (
    DEMO_DATABASE_NAME,
    DEMO_SCHEMA_NAME,
    DEMO_WAREHOUSE_NAME,
)
from snowflake.demos._telemetry import ApiTelemetryClient
from snowflake.snowpark.session import Session


logger = logging.getLogger(__name__)


class SingletonMeta(type):
    _instances: Dict[Type[Any], Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DemoConnection(metaclass=SingletonMeta):
    def __init__(self):
        self._root = None
        self._telemetry_client = None
        self._organization = None
        self._account = None

    def setup(self):
        if not self._root:
            self._root = self._create_root()
            cursor = self._root.connection.cursor()
            logger.info("Creating new database, schema and warehouse for demo setup")
            cursor.execute("USE ROLE ACCOUNTADMIN").fetchone()
            self._root.databases.create(
                Database(name=DEMO_DATABASE_NAME, comment="Database created for Snowflake demo setup"),
                mode="or_replace",
            )
            self._root.databases[DEMO_DATABASE_NAME].schemas.create(
                Schema(name=DEMO_SCHEMA_NAME, comment="Schema created for Snowflake demo setup"), mode="or_replace"
            )
            warehouse = Warehouse(
                name=DEMO_WAREHOUSE_NAME,
                comment="Warehouse created for Snowflake demo setup",
                warehouse_size="SMALL",
                auto_suspend=500,
            )
            self._root.warehouses.create(warehouse, mode="or_replace")
            self._organization = (
                self._root.connection.cursor().execute("SELECT CURRENT_ORGANIZATION_NAME()").fetchone()[0]
            )
            self._account = self._root.connection.cursor().execute("SELECT CURRENT_ACCOUNT_NAME()").fetchone()[0]

    def get_root(self):
        return self._root

    def teardown(self):
        # scenario where teardown is called without load_demo being called first
        if self._root is None:
            self._root = self._create_root()
        logger.info("Deleting database, schema and warehouse created for demo setup")
        cursor = self._root.connection.cursor()
        cursor.execute("USE ROLE ACCOUNTADMIN").fetchone()
        self._root.databases[DEMO_DATABASE_NAME].drop(if_exists=True)
        self._root.warehouses[DEMO_WAREHOUSE_NAME].drop(if_exists=True)
        self._root = None

    def _create_root(self):
        logger.info("Creating a new root connection")
        root = Root(Session.builder.create())
        self._telemetry_client = ApiTelemetryClient(root.connection)
        return root

    def get_account(self):
        return self._account

    def get_organization(self):
        return self._organization

    def get_telemetry_client(self):
        return self._telemetry_client
