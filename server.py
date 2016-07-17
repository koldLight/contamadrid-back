import bottle
import bottle_pgsql
import json

app = bottle.default_app()
app.config.load_config("conf/conf.ini")

plugin = bottle_pgsql.Plugin("dbname="    + app.config["db.database"] +
                             " user="     + app.config["db.user"] +
                             " password=" + app.config["db.pass"] +
                             " host="     + app.config["db.host"])
app.install(plugin)

@app.route("/stations")
def stations(db):
  rows = query_db(db, "SELECT * from station")
  return json.dumps(rows)

def query_db(db, query, args=(), one=False):
    db.execute(query, args)
    r = [dict((db.description[i][0], value) \
               for i, value in enumerate(row)) for row in db.fetchall()]
    return (r[0] if r else None) if one else r

app.run(host="localhost", port=8080, debug=True)
