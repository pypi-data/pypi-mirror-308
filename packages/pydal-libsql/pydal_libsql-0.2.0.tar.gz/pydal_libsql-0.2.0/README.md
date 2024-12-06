# libSQL for pyDAL

Basic driver/adapter for using libSQL/sqld (Turso) with pyDAL.

More info:

- [pydal](https://github.com/web2py/pydal/)
- [libsql](https://github.com/tursodatabase/libsql)
- [libsql-client](https://github.com/tursodatabase/libsql-client-py)
- [sqld](https://github.com/tursodatabase/libsql/blob/main/docs/DESIGN.md)
- [Turso](https://docs.turso.tech/introduction)

## Examples:

### Basic Usage with a SQLite compatible Database

```python
from pydal import DAL
# import is required to set up libsql:// and sqld:// for pyDAL
import pydal_libsql

# Connecting to a libSQL/SQLite database
db = DAL("libsql://example.db")

# example pydal operations:

# Defining a 'person' table with some fields
db.define_table(
    "person",
    db.Field("name", "string"),
    db.Field("age", "integer"),
    db.Field("last_name", "string")
)

# Committing the changes to the database
db.commit()

# Inserting a record into the 'person' table
db.person.insert(name="Henk", age=33)

# Retrieving and printing the inserted record
print(db(db.person.name == "Henk").select().as_list())
```

### Connecting to a SQLd Server

```python
from pydal import DAL
# import is required to set up libsql:// and sqld:// for pyDAL:
import pydal_libsql

# Connect to a SQLd server running on localhost:8080
db = DAL("sqld://localhost:8080")

# ...
```

### Using Turso's SQL Service

```python
from dotenv import dotenv_values
from pydal import DAL
# import is required to set up libsql:// and sqld:// for pyDAL:
import pydal_libsql

# Load Turso credentials from .env file or replace with your values directly
env = dotenv_values()
uri = env.get("TURSO_DATABASE_URL")  # Example: "libsql://your-database-name.turso.io"
token = env.get("TURSO_AUTH_TOKEN")  # Example: "ey****"

# Set up the database connection with Turso's URI and authentication token
db = DAL(uri, driver_args={"auth_token": token})

# ...
```

### Disclaimer

This project is an unofficial tool and is not affiliated, endorsed, or sponsored by the maintainers of pyDAL or Turso.
All references to pyDAL and Turso are for compatibility and integration purposes only.
