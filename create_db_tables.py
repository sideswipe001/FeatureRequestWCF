from sqlalchemy import create_engine, Table, Column, MetaData, Integer, String, Date


def create_db_tables():
    engine = create_engine('mysql://admin:passw0rd@aa1w9ri61a1hrx1.cepejztx2jqb.us-west-2.rds.amazonaws.com:3306/ebdb')
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