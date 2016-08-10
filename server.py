import bottle
from bottle import request, response
import bottle_pgsql
import json
import decimal
from datetime import datetime

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


class EnableCors(object):
  name = 'enable_cors'
  api = 2

  def apply(self, fn, context):
    def _enable_cors(*args, **kwargs):
      # set CORS headers
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers[
          'Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
      response.headers[
          'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

      if bottle.request.method != 'OPTIONS':
        # actual request; reply with the actual response
        return fn(*args, **kwargs)

    return _enable_cors


def date_serializer(o):
  if hasattr(obj, 'isoformat'):
    return obj.isoformat()


def decimal_serializer(o):
  if isinstance(o, decimal.Decimal):
    return str(o)
  elif hasattr(o, 'isoformat'):
    return o.isoformat()
  raise TypeError(repr(o) + " is not JSON serializable")


def query_db(db, query, args=(), one=False):
  db.execute(query, args)
  return db.fetchall()


def to_json(rows, status=200, message="OK"):
  result = {"status": status, "message": message, "data": rows}
  return json.dumps(result, default=decimal_serializer)

###############################################################################
# Controllers                                                                 #
###############################################################################


@app.route("/stations")
def stations(db):
  rows = query_db(db, "SELECT * from station")
  return to_json(rows)


@app.route("/measures")
def measures(db):
  from_date = datetime.strptime(request.query.start, '%Y-%m-%d')
  to_date = datetime.strptime(request.query.end, '%Y-%m-%d')
  rows = query_db(db, '''SELECT * from measure
                         WHERE variable_id = 8
                         AND date >= %s
                         AND date <= %s''',
                  (from_date, to_date))
  return to_json(rows)

###############################################################################
# Launch the server                                                           #
###############################################################################

app.install(EnableCors())

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)
