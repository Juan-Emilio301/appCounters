import mysql.connector 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Tilacino1",
  database="jugando_con_basedatos"
)

myCursor = mydb.cursor()

def select_multiple(objetivo, tabla, especificoDonde, variable_especifica):
  lista = []

  for objetivos in objetivo:
    myCursor.execute("SELECT %s FROM %s WHERE %s = %s" %(objetivos, tabla, especificoDonde, variable_especifica,))
    resultado = myCursor.fetchone()
    lista.append(resultado)

  return lista

def update_multiple(actualizar,  nuevo_valor, tabla, especificoDonde, variable_especifica):

  for index, nuevo_valores in enumerate(nuevo_valor):
    sql_edit = f"UPDATE `{tabla}` SET `{actualizar[index]}` = %s WHERE {especificoDonde} = %s"
    val_edit = (nuevo_valores, variable_especifica)
    myCursor.execute(sql_edit, val_edit)
    mydb.commit()
  

#def llamada_multiple_1param(parametros_busqueda, ejecuciones_extras = 0):
#  lista_resultado = []
#  i = 0
#
#  if len(parametros_busqueda) < 4:
#   return print("Inserte 4 paramtros minimo") 
#  elif len(parametros_busqueda) >= 4 and ejecuciones_extras == 0:
#      myCursor.execute("SELECT %s FROM %s WHERE %s = %s" %(parametros_busqueda[0], parametros_busqueda[1], parametros_busqueda[2], parametros_busqueda[3],))
#      resultado = myCursor.fetchone()
#      return resultado
#  else:
#    while i == ejecuciones_extras:
#      myCursor.execute("SELECT %s FROM %s WHERE %s = %s" %(parametros_busqueda[i], parametros_busqueda[i + 1], parametros_busqueda[i + 2], parametros_busqueda[i + 3],))
#      resultado = myCursor.fetchone()
#      i+=1


llamada = select_multiple(["Devengado", "Percibido", "Fecha"], "cuentacorriente", "idCliente", 4)
print(llamada)

update_multiple(["Percibido", "Devengado"], [3000, 200], "cuentacorriente", 'idCliente', 4)