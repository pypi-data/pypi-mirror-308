from dotenv import dotenv_values
from pydal import DAL

# noinspection PyUnresolvedReferences
# import is required to set up libsql:// and sqld:// for pyDAL
import pydal_libsql


# Example 1: Basic Usage with a libSQL-compatible SQLite Database
def example_libsql():
    print("Connecting to libSQL-compatible SQLite database...")
    db = DAL("libsql://example.db")

    db.define_table(
        "person",
        db.Field("name", "string"),
        db.Field("age", "integer"),
        db.Field("last_name", "string"),
    )

    db.commit()
    db.person.insert(name="Henk", age=33)
    result = db(db.person.name == "Henk").select().as_list()
    print("libSQL example result:", result)
    db.close()


# Example 2: Connecting to a SQLd Server
def example_sqld_server():
    print("Connecting to SQLd server on localhost:8080...")
    db = DAL("sqld://localhost:8080")

    db.define_table(
        "person",
        db.Field("name", "string"),
        db.Field("age", "integer"),
        db.Field("last_name", "string"),
    )

    db.commit()
    db.person.insert(name="Henk", age=33)
    result = db(db.person.name == "Henk").select().as_list()
    print("SQLd server example result:", result)
    db.close()


# Example 3: Using Turso's SQL Service
def example_turso():
    print("Connecting to Turso SQL service...")
    env = dotenv_values()  # Load credentials from .env file
    uri = env.get(
        "TURSO_DATABASE_URL"
    )  # Example: "libsql://your-database-name.turso.io"
    token = env.get("TURSO_AUTH_TOKEN")  # Example: "ey****"

    if not uri or not token:
        print(
            "Turso URI or token not found in .env file. Please add them and try again."
        )
        return

    db = DAL(uri, driver_args={"auth_token": token})

    db.define_table(
        "person",
        db.Field("name", "string"),
        db.Field("age", "integer"),
        db.Field("last_name", "string"),
    )

    db.commit()
    db.person.insert(name="Henk", age=33)
    result = db(db.person.name == "Henk").select().as_list()
    print("Turso example result:", result)
    db.close()


# Running all examples
if __name__ == "__main__":
    example_libsql()
    example_sqld_server()
    example_turso()
