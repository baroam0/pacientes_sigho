
import sqlite3

from renaper import obtener_token, consulta_renaper, consulta_obrasocial

pacientes_txt = open("bck_pacientes_sigho.txt", "r")
array_pacientes = pacientes_txt.readlines()


def consultatodo():
    cn = sqlite3.connect("datos.db")
    cursor = cn.cursor()
    sql_query = "SELECT * FRom pacientessigho WHERE obrasocial=NULL" 
    cursor.execute(sql_query)
    datos = cursor.fetchall()
    cn.commit()
    cursor.close()
    cn.close()
    return datos


pacientes = consultatodo()


for paciente in pacientes:
    t = obtener_token()
    dni = str(paciente[4])
    sexo = paciente[6]

    if sexo == "F":
        sexo = "1"
    else:
        sexo = "2"
    
    try:
        consulta_os = consulta_obrasocial(dni, sexo, t)
    except:
        

    print(consulta_os)
    

    