
import sqlite3

from renaper import obtener_token, consulta_renaper

pacientes_txt = open("pacientes_sigho.txt", "r")
array_pacientes = pacientes_txt.readlines()


def cndb(apellido, nombre, tipodocumento, numerodocumento, fechanacimiento, sexo, renaper):
    cn = sqlite3.connect("datos.db")
    cursor = cn.cursor()
    sql_query = "INSERT INTO pacientessigho (apellido, nombre, tipodocumento, numerodocumento, fechanacimiento, sexo, renaper) VALUES (?, ?, ?, ?, ?, ?, ?)"
    data_tuple = (apellido, nombre, tipodocumento, numerodocumento, fechanacimiento, sexo, renaper)
    cursor.execute(sql_query, data_tuple)
    cn.commit()
    cursor.close()
    cn.close()


def consultadb(dni):
    cn = sqlite3.connect("datos.db")
    cursor = cn.cursor()
    sql_query = "SELECT * FROM pacientessigho WHERE numerodocumento = ?"
    data_tuple = (dni,)
    cursor.execute(sql_query, data_tuple)
    results = cursor.fetchall()

    if results:
        cursor.close()
        cn.close()
        return results
    else:
        cursor.close()
        cn.close()
        results = None
        return results


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