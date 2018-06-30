from flask import Flask, jsonify, request, abort, render_template
from sqlalchemy import create_engine, Table, Column, MetaData, Integer, String, Date
from create_db_tables import create_db_tables

application = Flask(__name__)
engine = create_engine('mysql://admin:passw0rd@aa1w9ri61a1hrx1.cepejztx2jqb.us-west-2.rds.amazonaws.com:3306/ebdb')
if not engine.dialect.has_table(engine, "Client"):
    create_db_tables(engine)


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

    metadata = MetaData(engine)
    title = request['title']
    description = request['description']
    client = request['client']
    priority = request['priority']
    target = request['target']
    area = request['area']

    fr_table = Table('FeatureRequest', metadata, autoload=True)

    connection = engine.connect()
    insert = fr_table.insert().values(title=title, description=description, client=client, priority=priority,
                                      target=target, area=area)
    connection.execute(insert)


if __name__ == '__main__':
    application.run(debug=True)
