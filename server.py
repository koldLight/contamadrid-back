import bottle
import bottle_pgsql
import json
import decimal

###############################################################################
# Initialization                                                              #
###############################################################################

app = application = bottle.Bottle()
app.debug = True
app.config.load_config("conf/conf.ini")

plugin = bottle_pgsql.Plugin("dbname=" + app.config["db.database"] +
                             " user=" + app.config["db.user"] +
                             " password=" + app.config["db.pass"] +
                             " host=" + app.config["db.host"])
app.install(plugin)

###############################################################################
# Utils                                                                       #
###############################################################################


class number_str(float):

  def __init__(self, o):
    self.o = o

  def __repr__(self):
    return str(self.o)


def decimal_serializer(o):
  if isinstance(o, decimal.Decimal):
    return number_str(o)
  raise TypeError(repr(o) + " is not JSON serializable")


def query_db(db, query, args=(), one=False):
  db.execute(query, args)
  return db.fetchall()


def to_json(rows):
  return json.dumps(rows, default=decimal_serializer)

###############################################################################
# Controllers                                                                 #
###############################################################################


@app.route("/stations")
def stations(db):
  rows = query_db(db, "SELECT * from station")
  return to_json(rows)

###############################################################################
# Launch the server                                                           #
###############################################################################

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)
