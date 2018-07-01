from flask import Flask, jsonify, request, abort, render_template, Response
from sqlalchemy import create_engine, Table, MetaData
from create_db_tables import create_db_tables
import os

application = Flask(__name__)
name = os.environ['RDS_DB_NAME']
user = os.environ['RDS_USERNAME']
password = os.environ['RDS_PASSWORD']
host = os.environ['RDS_HOSTNAME']
port = os.environ['RDS_PORT']
engine = create_engine('mysql://' + user + ':' + password + '@' + host + ':' + port + '/' + name)
if not engine.dialect.has_table(engine, "Client"):
    create_db_tables()


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/api/v1/Client', methods=['GET'])
def get_clients():

    connection = engine.connect()
    results = []
    for row in connection.execute('SELECT * FROM Client'):
        results.append({'id': row[0], 'name': row[1]})
    return jsonify(results)


@application.route('/api/v1/Area', methods=['GET'])
def get_area():

    connection = engine.connect()
    results = []
    for row in connection.execute('SELECT * FROM Area'):
        results.append({'id': row[0], 'name': row[1]})
    return jsonify(results)


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
    return Response("", status=201, mimetype='text/html')


@application.route('/api/v1/FeatureRequest/Client/<int:client_id>', methods=['GET'])
def get_requests(client_id):
    connection = engine.connect()
    results = []
    for row in connection.execute('SELECT * FROM FeatureRequest WHERE clientId = {}'.format(client_id)):
        results.append({'id': row[0], 'name': row[1], 'description': row[2], 'clientId': row[3], 'priority': row[4],
                        'target': row[5], 'areaId': row[6]})
    return jsonify(results)


if __name__ == '__main__':
    application.run(debug=True)
