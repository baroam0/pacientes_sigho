
import os

from validapaciente import consultadb, renaperizar


datos = consultadb()

for i in datos:
   print(i)
   renaperizar(i, i[2])
   