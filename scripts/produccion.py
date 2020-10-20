import psycopg2

# estableciendo la conexión de base de datos 
conn = psycopg2.connect(
   user='postgres', password='admin', host='127.0.0.1', port= '5432'
)
conn.autocommit = True

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

cursor.execute("SELECT datname FROM pg_database;")

list_database = cursor.fetchall()
database_name = 'produccion'

if (database_name,) in list_database:
  sql = '''DROP database produccion''';
  cursor.execute(sql)
else:
# Preparando la sentencia SQL para crear base de datos 
  sql = '''CREATE database produccion''';
  cursor.execute(sql) # Creando base de datos para entorno de produccion
  print("=== Base de datos en produccion creado satisfactoriamente! ===")

#Closing the connection 
conn.close() 

