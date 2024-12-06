# rqlite for pyDAL

From the [rqlite](https://rqlite.io) docs:
> rqlite is an easy-to-use, lightweight, distributed relational database, which uses SQLite as its storage engine.

See [their GitHub page](https://github.com/rqlite/rqlite) for more info about deploying and managing an rqlite cluster, interacting with the cli or the HTTP
API directly.

## Example usage:

```python
from pydal import DAL

# required to register rqlite://
import pydal_rqlite

db = DAL("rqlite://localhost", folder="database")
# or with basic auth/custom port/https:
# db = DAL("rqlite://user:pass@localhost:4001", folder="database", driver_args={'https': True})
```

`db` should now support the same features the `sqlite3` driver
for [pyDAL](http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer) does.

## Limitations

As specified in the [docs](https://github.com/rqlite/pyrqlite#limitations) of `pyrqlite` (which is the driver behind
this
adapter):
> Transactions are not supported

This is due to the fact rqlite does not really support transactions.
`db.commit()` and `db.rollback()` will not raise an exception, but do nothing instead (`pass`).