from flask import Flask, request
import psycopg2
import os
from sys import stdout
app = Flask(__name__)


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    try:
        conn = db.cursor()
        conn.execute("SELECT * FROM ServiceStatus")
        result = conn.fetchall()
        return {'ip': ip, 'services': result}
    except:
        return {"error": "Database is unavailable"}



db = psycopg2.connect(dbname='healthchecks', user=os.environ.get("DB_USER"),
                      password=os.environ.get("DB_PASSWORD"), host=os.environ.get("DB_HOST"))
conn = db.cursor()
db.commit()

if False:
    conn.execute("""CREATE TYPE availability AS ENUM (
     'AVAILABLE', 
     'NOT AVAILABLE')""")


conn.execute("""CREATE TABLE IF NOT EXISTS ServiceStatus
                    (ip TEXT PRIMARY KEY, status availability)""")

ip = '10.130.0.15'

conn.execute("""DELETE FROM ServiceStatus WHERE ip = '%s'""" % ip)
conn.execute("INSERT INTO ServiceStatus VALUES ('%s', 'AVAILABLE')" % ip)
db.commit()

conn.close()
print("READY TO RUN")
app.run(host='0.0.0.0')
