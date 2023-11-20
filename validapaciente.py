
import sqlite3

from renaper import obtener_token, consulta_renaper


def importcvs(parametro):
   cn = sqlite3.connect("datos.sqlite")
   cursor = cn.cursor()
   sql_query = "INSERT INTO paciente (migracionid, numerodocumento, sexoid, apellido, nombre, fechanacimiento) VALUES (?, ?, ?, ?, ?, ?)"
   cursor.executemany(sql_query, parametro)
   cn.commit()
   cursor.close()
   cn.close()


def consultadb():
    cn = sqlite3.connect("datos.sqlite")
    cursor = cn.cursor()
    sql_query = "SELECT * FROM paciente WHERE encontrado IS NULL"
    cursor.execute(sql_query)
    results = cursor.fetchall()
    return results


def renaperizar(datos, dni):    
    cn = sqlite3.connect("datos.sqlite")
    cursor = cn.cursor()

    tkn = obtener_token()

    try:
        print("***********************************************************************")
        print(str(datos[2]), str(datos[3]))
        datosrenaper = consulta_renaper(str(datos[2]), str(datos[3]),tkn)
        print(datosrenaper)
        tupla = (datosrenaper["apellido"], datosrenaper["nombres"] , datosrenaper["fechaNacimiento"], 1, str(dni))
        
        sqlstr = '''UPDATE paciente SET apellidorenaper = ?, nombrerenaper = ?, fechanacimientorenaper = ?, encontrado= ? WHERE numerodocumento = ?'''
        cursor.execute(sqlstr, tupla)
    except:
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        sql_query = '''UPDATE paciente SET encontrado=0 WHERE numerodocumento={}'''.format(str(dni))
        print(sql_query)
        cursor.execute(sql_query)

    cn.commit()
    cursor.close()
    cn.close()



"""
for i in array_pacientes:
    print("Inicio de proceso de registro...")
    array_i = i.split(";")
    array_apellido_nombre = array_i[1].split(",")
    apellido = array_apellido_nombre[0]
    nombre = array_apellido_nombre[1]
    nombre = nombre.strip()
    tipodocumento = array_i[2]

    sexo = str(array_i[5])
    sexo = sexo.rstrip()
  
    if sexo == "Femenino":
        sexo = "1"
        sexo_db = "F"
    if sexo == "Masculino":
        sexo = "2"
        sexo_db = "M"

    dni = str(array_i[3])
    
    array_fechanacimiento = array_i[4].split("/")
 
    tmp_fechanacimiento = array_fechanacimiento[2] + "/" + array_fechanacimiento[1] + "/" + array_fechanacimiento[0] 
    
    dict_db = {
        "apellido": apellido.upper(),
        "nombre": nombre.upper(),
        "sexo": sexo_db,
        "fechanacimiento": tmp_fechanacimiento
    }
    
    
    try:
        print("Consultando...")
        t = obtener_token()
        response = consulta_renaper(dni, sexo, t)
        renaper_apellido = response["apellido"]
        renaper_nombre = response["nombres"]
        renaper_sexo = response["sexo"]
        renaper_fechanacimiento = response["fechaNacimiento"].replace("-", "/")
    
        dict_renaper = {
            "apellido": renaper_apellido.upper(),
            "nombre": renaper_nombre.upper(),
            "sexo": renaper_sexo,
            "fechanacimiento": renaper_fechanacimiento,
        }

        resultado = consultadb(dni)

        if not resultado:
            print("Grabando....")
            print("################## DICT RENAPER #########################")
            print(dict_renaper)
            print("################## DICT db #########################")
            print(dict_db)
            if dict_db == dict_renaper:
                renaper = 1
                cndb(renaper_apellido, renaper_nombre, tipodocumento, dni, renaper_fechanacimiento, renaper_sexo, renaper)
            else:
                renaper = 0
                cndb(apellido.upper(), nombre.upper(), tipodocumento, int(dni), tmp_fechanacimiento, sexo_db, renaper)

        print("Procesando siguiente registro...")

    except Exception as e:
        print("Sin respuesta Renaper.....")
        print(e)
        renaper = 2
        cndb(renaper_apellido, renaper_nombre, tipodocumento, dni, renaper_fechanacimiento, renaper_sexo, renaper)
        pass
"""