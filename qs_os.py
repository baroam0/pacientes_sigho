
import sqlite3


from renaper import obtener_token, consulta_renaper, consulta_obrasocial


t = obtener_token()
response = consulta_obrasocial("31897498", "1", t)
print(response)

