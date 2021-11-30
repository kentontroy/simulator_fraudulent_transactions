import phoenixdb
import phoenixdb.cursor
import warnings

warnings.filterwarnings("ignore")

dbUrl = "https://kdavis-pse-webinar-worker0.se-sandb.a465-9q4k.cloudera.site:8765"
conn = phoenixdb.connect(dbUrl, autocommit=True, verify=False, authentication="SPNEGO")

cur = conn.cursor()
cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username VARCHAR)")
cur.execute("UPSERT INTO users VALUES (?, ?)", (1, 'admin'))
cur.execute("SELECT * FROM users")

print(cur.fetchall())
