import tempfile
import time

import pytest
from dotenv import dotenv_values
from pydal import DAL
from testcontainers.core.container import DockerContainer

# noinspection PyUnresolvedReferences
# import is required, even though pacakge is not used, to set up rqlite:// for pyDAL
import pydal_libsql

libsql_docker = DockerContainer("ghcr.io/tursodatabase/libsql-server:latest")


@pytest.fixture()
def sqld(request):
    libsql_docker.ports = {
        8080: 8080,
    }

    request.addfinalizer(libsql_docker.stop)
    libsql_docker.start()
    time.sleep(5)  # cursed alternative to health check
    return libsql_docker


def test_local_server(sqld: DockerContainer):
    with tempfile.TemporaryDirectory() as d:
        db = DAL("sqld://localhost:8080", folder=d)

        db.define_table(
            "person",
            db.Field("name", "string"),
            db.Field("age", "integer"),
            db.Field("last_name", "string"),
            # fake_migrate=True,
        )

        db.commit()

        db.person.truncate()

        db.person.insert(name="Henk", age=33)

        print(db(db.person.name == "Henk").select().as_list())


def test_turso():
    with tempfile.TemporaryDirectory() as d:
        env = dotenv_values()

        uri = env["TURSO_DATABASE_URL"]
        token = env["TURSO_AUTH_TOKEN"]

        db = DAL(
            uri,
            driver_args={
                # "sync_url": uri,
                "auth_token": token,
            },
            folder=d,
        )

        import uuid

        db.define_table(
            f"person",
            db.Field("name", "string"),
            db.Field("age", "integer"),
            db.Field("last_name", "string"),
            # fake_migrate=True,
            rname=f"person{int(uuid.uuid4())}",
        )

        db.commit()
        db.person.truncate()

        db.person.insert(name="Henk", age=33)
        db.commit()
        assert db(db.person).count()

        print(db(db.person.name == "Henk").select().as_list())

        db(db.person).delete()
        db.rollback()

        assert db(db.person).count()
