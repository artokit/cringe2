from sqlalchemy import MetaData, Integer, Table, Column, String, Boolean, Double, ForeignKey

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
    Column('username', String, unique=True, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('admin', Boolean, default=False),
    Column('access_token', String),
    Column('refresh_token', String),
    Column('balance', Integer, default=0)
)

transports = Table(
    'transports',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True, nullable=False),
    Column('canBeRented', Boolean, nullable=False),
    Column('transportType', String, nullable=False),
    Column('model', String, nullable=False),
    Column('color', String, nullable=False),
    Column('identifier', String, nullable=False),
    Column('description', String, nullable=True),
    Column('latitude', Double, nullable=False),
    Column('longitude', Double, nullable=False),
    Column('minutePrice', Double, nullable=True),
    Column('dayPrice', Double, nullable=True),
    Column('owner_id', ForeignKey(users.c.id)),
)

# ('INSERT INTO payments VALUES (%s, %s, %s, %s)', (payment.uuid, payment.status, user_id, amount))
payments = Table(
    'payments',
    metadata,
    Column('uuid', String, primary_key=True, nullable=False),
    Column('status', String, nullable=False),
    Column('user_id', ForeignKey(users.c.id), nullable=False),
    Column('amount', Integer, nullable=False),

)

rents = Table(
    'rents',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('transport_id', Integer),
    Column('rent_type', String),
    Column('status', String)
)
