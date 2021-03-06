import psycopg2
from flask import Flask, request, Response
app = Flask(__name__)

@app.route('/')
def root():
    return app.send_static_file('map.html')


@app.route('/parking')
def hello_park():
    lat = float(request.args.get("lat", 54))
    lng = float(request.args.get("lng", 10))

    # Connect to an existing database
    conn = psycopg2.connect("""dbname=parking
                               user=carsten""")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Query the database and obtain data as Python objects
    cur.execute("""SELECT id, vejnavn, ST_AsGeoJSON(geom)
                   FROM phus
                   ORDER BY geom <-> 'SRID=4326;POINT(%s %s)'::geometry
                   LIMIT 1;""", (lng, lat))
    row = cur.fetchone()

    output = '''{
          "type": "Feature",
          "properties": {
              "id": '''+str(row[0])+''',
              "streetname": "'''+row[1]+'''"},
          "geometry": '''+row[2]+'''
        }'''

    cur.close()
    conn.close()

    return Response(response=output,
                    status=200,
                    mimetype="application/json")
