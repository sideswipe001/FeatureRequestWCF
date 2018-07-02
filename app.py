from flask import Flask, jsonify, request, abort, render_template, Response
from sqlalchemy import create_engine, Table, MetaData
from create_db_tables import create_db_tables, drop_db_tables
import os

application = Flask(__name__)
name = os.environ['RDS_DB_NAME']
user = os.environ['RDS_USERNAME']
password = os.environ['RDS_PASSWORD']
host = os.environ['RDS_HOSTNAME']
port = os.environ['RDS_PORT']
engine = create_engine('mysql://' + user + ':' + password + '@' + host + ':' + port + '/' + name)

# If the DB exists, we want to drop everything, so we get a clean start every time.
if engine.dialect.has_table(engine, "Client"):
    drop_db_tables()
create_db_tables()


@application.route('/')
def index():
    return render_template('index.html')


# This endpoint requests all Clients. Returns a JSON list of Clients.
@application.route('/api/v1/Client', methods=['GET'])
def get_clients():

    connection = engine.connect()
    results = []
    for row in connection.execute('SELECT * FROM Client'):
        results.append({'id': row[0], 'name': row[1]})
    return jsonify(results)


# This endpoint requests all Areas. Returns a JSON list of Areas.
@application.route('/api/v1/Area', methods=['GET'])
def get_area():

    connection = engine.connect()
    results = []
    for row in connection.execute('SELECT * FROM Area'):
        results.append({'id': row[0], 'name': row[1]})
    return jsonify(results)


# This endpoint allows for adding new feature requests. POST with a JSON body containing a single FeatureRequest
@application.route('/api/v1/FeatureRequest', methods=['POST'])
def add_request():
    if not request.json:
        abort(400)

    values = request.json
    metadata = MetaData(engine)
    title = values['title']
    description = values['description']
    client = values['clientId']
    priority = values['priority']
    target = values['target']
    area = values['areaId']

    fr_table = Table('FeatureRequest', metadata, autoload=True)

    connection = engine.connect()
    insert = fr_table.insert().values(title=title, description=description, clientId=client, priority=priority,
                                      target=target, areaId=area)
    connection.execute(insert)
    return Response("", status=200, mimetype='text/html')


# This endpoint requests all existing feature requests for all clients. It returns a JSON list of FeatureRequests
@application.route('/api/v1/FeatureRequest/', methods=['GET'])
def get_all_requests():
    connection = engine.connect()
    results = []
    for row in connection.execute('SELECT * FROM FeatureRequest'):
        results.append({'id': row[0], 'title': row[1], 'description': row[2], 'clientId': row[3], 'priority': row[4],
                        'target': row[5], 'areaId': row[6]})
    return jsonify(results)


# This endpoint allows for updating a single feature request. The POST body contains a single FeatureRequest.
# Returns a 200 with blank text if successful.
@application.route('/api/v1/FeatureRequest/<int:feature_request_id>', methods=['POST'])
def update_request(feature_request_id):
    if not request.json:
        abort(400)

    values = request.json
    metadata = MetaData(engine)
    title = values['title']
    description = values['description']
    client = values['clientId']
    priority = values['priority']
    target = values['target']
    area = values['areaId']

    fr_table = Table('FeatureRequest', metadata, autoload=True)

    connection = engine.connect()

    update = fr_table.update().where(fr_table.c.id == feature_request_id).values(
        title=title, description=description, clientId=client, priority=priority,
        target=target, areaId=area)
    connection.execute(update)
    return Response("", status=200, mimetype='text/html')


# This endpoint requests all FeatureRequests for a single client.
# It returns a JSON list of all FeatureRequests for that client
@application.route('/api/v1/FeatureRequest/Client/<int:client_id>', methods=['GET'])
def get_requests(client_id):
    connection = engine.connect()
    results = []
    for row in connection.execute('SELECT * FROM FeatureRequest WHERE clientId = {}'.format(client_id)):
        results.append({'id': row[0], 'title': row[1], 'description': row[2], 'clientId': row[3], 'priority': row[4],
                        'target': row[5], 'areaId': row[6]})
    return jsonify(results)


if __name__ == '__main__':
    application.run(debug=True)
