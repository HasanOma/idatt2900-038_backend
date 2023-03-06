import psycopg2
# Update connection string information

host = 'mtp-db.postgres.database.azure.com'
dbname = "postgres"
user = "mtp038"
password = "qwertY1!"
sslmode = "require"
# Construct connection string

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")
cursor = conn.cursor()