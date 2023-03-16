import psycopg2
# Update connection string information

# host = 'mtp-db.postgres.database.azure.com'
# dbname = "postgres"
# user = "mtp038"
# password = "qwertY1!"
# sslmode = "require"
# conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
# Construct connection string

host = 'localhost'
dbname = "postgres"
user = "postgres"
password = "password"
# sslmode = "require"
conn_string = "host={0} user={1} dbname={2} password={3} ".format(host, user, dbname, password)


conn = psycopg2.connect(conn_string)
print("Connection established")
cursor = conn.cursor()

# For SQLAlchemy
sqlalchemy_conn_string = "postgresql://{0}:{1}@{2}/{3}".format(user, password, host, dbname)