import sqlite3
import pandas as pd

#Se crea una conexiòn a una BDD en memoria local
conn = sqlite3.connect(':memory:')

#Se crea la tabla aerolinea y se insertan los datos correspondientes
conn.execute("""CREATE TABLE aerolinea (id_aerolinea INT PRIMARY KEY, nombre_aerolinea TEXT);""")
conn.execute("""INSERT INTO aerolinea (id_aerolinea, nombre_aerolinea) VALUES (1, 'Volaris');""")
conn.execute("""INSERT INTO aerolinea (id_aerolinea, nombre_aerolinea) VALUES (2, 'Aeromar');""")
conn.execute("""INSERT INTO aerolinea (id_aerolinea, nombre_aerolinea) VALUES (3, 'Interjet');""")
conn.execute("""INSERT INTO aerolinea (id_aerolinea, nombre_aerolinea) VALUES (4, 'Aeromexico');""")
conn.commit()

#Se crea la tabla aeropuertos y se insertan los datos correspondientes
conn.execute("""CREATE TABLE aeropuertos (id_aeropuerto INT PRIMARY KEY, nombre_aeropuerto TEXT);""")
conn.execute("""INSERT INTO aeropuertos (id_aeropuerto, nombre_aeropuerto) VALUES (1, 'Benito Juarez');""")
conn.execute("""INSERT INTO aeropuertos (id_aeropuerto, nombre_aeropuerto) VALUES (2, 'Guanajuato');""")
conn.execute("""INSERT INTO aeropuertos (id_aeropuerto, nombre_aeropuerto) VALUES (3, 'La Paz');""")
conn.execute("""INSERT INTO aeropuertos (id_aeropuerto, nombre_aeropuerto) VALUES (4, 'Oaxaca');""")
conn.commit()

#Se crea la tabla movimientos y se insertan los datos correspondientes
conn.execute("""CREATE TABLE movimientos ( id_movimiento INT PRIMARY KEY, descripcion TEXT NOT NULL);""")
conn.execute("""INSERT INTO movimientos (id_movimiento, descripcion) VALUES (1, 'Salida');""")
conn.execute("""INSERT INTO movimientos (id_movimiento, descripcion) VALUES (2, 'Llegada');""")
conn.commit()

# Crear la tabla vuelos y se insertan los datos correspondientes
conn.execute("""
CREATE TABLE vuelos (
    id_aerolinea  INT,
    id_aeropuerto INT,
    id_movimiento INT,
    dia           TEXT,
    FOREIGN KEY (id_aeropuerto) REFERENCES aeropuertos (id_aeropuerto),
    FOREIGN KEY (id_movimiento) REFERENCES movimientos (id_movimiento),
    FOREIGN KEY (id_aerolinea) REFERENCES aerolinea (id_aerolinea)
);
""")
conn.execute("""INSERT INTO vuelos ( id_aerolinea, id_aeropuerto, id_movimiento, dia) VALUES (1, 1, 1, '2021-05-02');""")
conn.execute("""INSERT INTO vuelos ( id_aerolinea, id_aeropuerto, id_movimiento, dia) VALUES (2, 1, 1, '2021-05-02');""")
conn.execute("""INSERT INTO vuelos ( id_aerolinea, id_aeropuerto, id_movimiento, dia) VALUES (3, 2, 2, '2021-05-02');""")
conn.execute("""INSERT INTO vuelos ( id_aerolinea, id_aeropuerto, id_movimiento, dia) VALUES (4, 3, 2, '2021-05-02');""")
conn.execute("""INSERT INTO vuelos ( id_aerolinea, id_aeropuerto, id_movimiento, dia) VALUES (1, 3, 2, '2021-05-02');""")
conn.execute("""INSERT INTO vuelos ( id_aerolinea, id_aeropuerto, id_movimiento, dia) VALUES (2, 1, 1, '2021-05-02');""")
conn.execute("""INSERT INTO vuelos ( id_aerolinea, id_aeropuerto, id_movimiento, dia) VALUES (2, 3, 1, '2021-05-04');""")
conn.execute("""INSERT INTO vuelos ( id_aerolinea, id_aeropuerto, id_movimiento, dia) VALUES (3, 4, 1, '2021-05-04');""")
conn.execute("""INSERT INTO vuelos ( id_aerolinea, id_aeropuerto, id_movimiento, dia) VALUES (3, 4, 1, '2021-05-04');""")
conn.commit()

print("""1. ¿Cuál es el nombre aeropuerto que ha tenido mayor movimiento durante el año?""")
query = """
WITH conteo_movimientos as (
SELECT  id_aeropuerto,
        COUNT(id_aeropuerto) as conteo
FROM vuelos GROUP BY 1
)
SELECT ae.nombre_aeropuerto
FROM conteo_movimientos cm
LEFT JOIN aeropuertos   ae         ON ae.id_aeropuerto = cm.id_aeropuerto
WHERE conteo = (SELECT MAX(conteo) FROM conteo_movimientos)

 """
df = pd.read_sql(query, conn)
print(df)

# Consideraremos ambos tipos de movimiento ya que no tenemos la certeza de que la salidas estén relacionadas con las llegadas, sería útil teniendo un id_vuelo
print("""2. ¿Cuál es el nombre aerolínea que ha realizado mayor número de vuelos durante el año?""")
query = """
WITH conteo_vuelos as (
SELECT  id_aerolinea,
        COUNT(id_aerolinea) as conteo
FROM vuelos
GROUP BY 1
)
SELECT ae.nombre_aerolinea
FROM conteo_vuelos cv
LEFT JOIN aerolinea   ae         ON ae.id_aerolinea = cv.id_aerolinea
WHERE conteo = (SELECT MAX(conteo) FROM conteo_vuelos)

 """
df = pd.read_sql(query, conn)
print(df)

# En esta pregunta consideramos un vuelo como una salida, las llegadas no las consideramos como vuelo
print("""3. ¿En qué día se han tenido mayor número de vuelos?""")
query = """
WITH conteo_movimiento as (
SELECT  dia,
        COUNT(id_movimiento) as conteo
FROM vuelos
WHERE id_movimiento = 1
GROUP BY 1
)
SELECT dia FROM conteo_movimiento WHERE conteo = (SELECT MAX(conteo) FROM conteo_movimiento)

 """
df = pd.read_sql(query, conn)
print(df)
#En este caso ambos dìas tuvieron el mismo número de vuelos

#En este caso consideramos ambos tipos de movimiento, ya que se ve desde la perspectiva de aerolìnea
print("""4. ¿Cuáles son las aerolíneas que tienen mas de 2 vuelos por día? """)
query = """
WITH conteo_movimiento as (
SELECT  dia,
        id_aerolinea,
        COUNT(id_movimiento) as conteo
FROM vuelos
WHERE id_movimiento = 1
GROUP BY 1,2
)
SELECT nombre_aerolinea,
      dia,
      conteo as conteo_vuelos
FROM conteo_movimiento cm
LEFT JOIN aerolinea   ae         ON ae.id_aerolinea = cm.id_aerolinea
WHERE conteo > 1
 """
df = pd.read_sql(query, conn)
print(df)
#En este caso ninguna ha tenido más de dos salidas en los días establecidos, con WHERE conteo > 1 obtenemos que Aeromar e Interjet han tenido 2 vuelos esos dìas

conn.close()

conn.close()

