

from renaper import obtener_token, consulta_renaper

t = obtener_token()

d =  consulta_renaper("93345039", "1", t)

print(d)