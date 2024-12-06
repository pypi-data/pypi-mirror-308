import locale
import sys

from pydal.adapters import adapters, SQLite
from pyrqlite import dbapi2
from urllib.parse import urlparse


@adapters.register_for("rqlite")
class Rqlite(SQLite):
    drivers = ("pyrqlite",)

    def _initialize_(self):
        self.pool_size = 0
        # skip _initialize_ of SQLite, but do init it's super:
        super(SQLite, self)._initialize_()

        # self.dbpath = self.uri.split("://", 1)[1]

        if "detect_types" not in self.driver_args:
            self.driver_args["detect_types"] = self.driver.PARSE_DECLTYPES

    def find_driver(self):
        self.driver_name = self.drivers[0]
        self.driver = dbapi2

    def _extract_urlparts(self, conn_str):
        info = urlparse(conn_str)

        return {
            'host': info.hostname,
            'user': info.username,
            'password': info.password,
            'port': info.port or '4001',
        }

    def connector(self):
        args = self.driver_args
        if 'check_same_thread' in args:
            del args['check_same_thread']

        if 'https' in args:
            scheme = 'https' if args['https'] else 'http'
            del args['https']
        else:
            scheme = 'http'

        args.update(
            # split dbpath to schema, host, post etc
            self._extract_urlparts(self.uri)
        )

        return self.driver.Connection(
            scheme=scheme,
            **args)

    def after_connection(self):
        # self._register_extract()
        # self._register_regexp()
        if self.adapter_args.get("foreign_keys", True):
            self.execute("PRAGMA foreign_keys=ON;")
