import warnings
from pathlib import Path

from libsql_client import dbapi2 as libsql_db2
from pydal.adapters import SQLite, adapters


@adapters.register_for("libsql")
class LibSQL(SQLite):
    drivers = ("libsql_db2",)

    def find_driver(self):
        self.driver_name = self.drivers[0]
        self.driver = libsql_db2

    def _create_function_not_supported(self, *a, **kw):
        warnings.warn("create_function used but sqld does not support this!")

    def connector(self) -> libsql_db2.types.Connection:
        args = self.driver_args
        uri: str = self.uri

        if "auth_token" in args:
            # not a local file
            return SQLd.connector(self)

        # sqlite3-like file
        uri = uri.removeprefix("libsql://").removeprefix("sqld://")
        folder = Path(self.folder) if self.folder else Path.cwd()
        uri_path = folder / uri
        print("file", uri_path)

        connection = self.driver.connect(uri_path, **args)

        return connection


@adapters.register_for("sqld")
class SQLd(LibSQL):
    def connector(self) -> libsql_db2.types.Connection:
        args = self.driver_args
        uri: str = self.uri

        # if uri has :// it's an uri, otherwise it's a file path (absolute or relative)
        uri = uri.removeprefix("libsql:").removeprefix("sqld:")
        uri_path = uri.replace("//", "ws://")  # todo: wss?

        connection = self.driver.connect(uri_path, **args)

        connection.create_function = self._create_function_not_supported

        return connection
