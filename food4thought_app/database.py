import psycopg2

class db():
    conn = psycopg2.connect(dbname="aj8641", user="aj8641", password="h03wfa49", host="pgserver.mah.se")
    cursor = conn.cursor()
