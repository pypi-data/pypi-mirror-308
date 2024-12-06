from pydal import DAL

# noinspection PyUnresolvedReferences
# import is required, even though pacakge is not used, to set up rqlite:// for pyDAL
import pydal_rqlite

# db = DAL("rqlite://user:pass@localhost:4001", folder="database", driver_args={'https': False})
db = DAL("rqlite://localhost", folder="database")
# or with basic auth/custom port/https:
# db = DAL("rqlite://user:pass@localhost:4001", folder="database", driver_args={'https': True})
# db now works similarly to sqlite:
# db = DAL("sqlite://:memory:", folder="database")

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

print(
    db(db.person.name == "Henk").select().as_list()
)
