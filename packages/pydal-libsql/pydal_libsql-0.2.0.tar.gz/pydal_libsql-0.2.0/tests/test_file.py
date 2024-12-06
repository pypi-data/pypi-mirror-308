import tempfile
from contextlib import chdir

from pydal import DAL

# noinspection PyUnresolvedReferences
# import is required, even though pacakge is not used, to set up libsql:// and sqld:// for pyDAL
import pydal_libsql


def test_file():
    with tempfile.TemporaryDirectory() as d, chdir(d):
        db = DAL("libsql://example.db")

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


def test_file_with_folder():
    with tempfile.TemporaryDirectory() as d:
        db = DAL("libsql://example.db", folder=d)

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
