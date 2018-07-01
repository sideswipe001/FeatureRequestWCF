from sqlalchemy import create_engine, Table, Column, MetaData, Integer, String, Date
import os


def create_db_tables():

    name = os.environ['RDS_DB_NAME']
    user = os.environ['RDS_USERNAME']
    password = os.environ['RDS_PASSWORD']
    host = os.environ['RDS_HOSTNAME']
    port = os.environ['RDS_PORT']
    engine = create_engine('mysql://' + user + ':' + password + '@' + host + ':' + port + '/' + name)
    metadata = MetaData(engine)
    Table("FeatureRequest", metadata,
          Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
          Column('title', String(64), nullable=False),
          Column('description', String(300), nullable=False),
          Column('clientId', Integer, nullable=False),
          Column('priority', Integer, nullable=False),
          Column('target', Date, nullable=False),
          Column('areaId', Integer, nullable=False)
          )

    client_table = Table("Client", metadata,
          Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
          Column('name', String(32), nullable=False)
          )

    area_table = Table("Area", metadata,
          Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
          Column('name', String(32), nullable=False)
          )

    metadata.create_all()
    conn = engine.connect()
    conn.execute(client_table.insert(), [
        {'name': 'Client A'},
        {'name': 'Client B'},
        {'name': 'Client C'},
    ])
    conn.execute(area_table.insert(), [
        {'name': 'Policies'},
        {'name': 'Billing'},
        {'name': 'Claims'},
        {'name': 'Reports'},
    ])