
import json, sys
import requests
import urllib.parse, urllib.request

def obtener_token():
    """Funcion para obenter el token del RENAPER
    """

    str_url = "https://federador.msal.gob.ar/masterfile-federacion-service/api/usuarios/aplicacion/login"
    nombre = "GA4AAxkcEw1dFQQEXQMVGh0PXQMfEx4cAwk="
    clave = "XihXCh4eNwMWLj9UJkpFWEQ="
    codDominio = "DOMINIOSINAUTORIZACIONDEALTA"

    headers = {'Content-type': 'application/json'}

    data = {
        "nombre": nombre,
        "clave": clave, 
        "codDominio": codDominio, 
    }

    peticion = requests.post(url=str_url, json=data, headers=headers, verify=False) 
    peticion_json = peticion.json()
    tkn = peticion_json["token"]
    return tkn


def consulta_renaper(dni, sexo, t):
    str_url = "https://federador.msal.gob.ar/masterfile-federacion-service/api/personas/renaper?nroDocumento="+ dni + "&idSexo=" + sexo
    headers = {"token": t, "codDominio": "DOMINIOSINAUTORIZACIONDEALTA" }
    peticion = requests.get(str_url, headers=headers, verify=False)
    peticion_json = peticion.json()
    return peticion_json


def consulta_obrasocial(dni, sexo, t):
    str_url = "https://federador.msal.gob.ar/masterfile-federacion-service/api/personas/cobertura?nroDocumento=" + dni + "&idSexo=" + sexo
    headers = {"token": t, "codDominio": "DOMINIOSINAUTORIZACIONDEALTA" }
    peticion = requests.get(str_url, headers=headers)
    peticion_json = peticion.json()
    return peticion_json


