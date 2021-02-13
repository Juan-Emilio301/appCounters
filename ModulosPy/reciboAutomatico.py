import os
import mysql.connector
import xlsxwriter
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Tilacino1",
  database="jugando_con_basedatos"
)

def IdLimpioFunc(idpass, tipoConversion = "int"):
    Id_Limpio_Lista=[]
    id_Str = str(idpass)

    for IdFor in id_Str:
        if IdFor == "(":
            continue
        elif IdFor == ",":
            break
        Id_Limpio_Lista.append(IdFor)
        Idlimpio_str=''.join(Id_Limpio_Lista)

    if tipoConversion == "int":
      return int(Idlimpio_str)

    elif tipoConversion == "string":
      return Idlimpio_str

def listaVertical(lineaLugar, columna, listaIterable, estilo):
  for linea, informacion in enumerate(listaIterable):
    workSheet.write(linea + lineaLugar, columna, informacion, estilo)

def llamadaEspecifidaDB(objetivo, tabla, especificoDonde, variableEspecifica):
  myCursor.execute("SELECT %s FROM %s WHERE %s = %s" %(objetivo, tabla, especificoDonde, variableEspecifica,))
  return myCursor.fetchone()

def verificacion(nombrePass):
  nombreReformulado = nombrePass + ".xlsx"

  if os.path.exists(f"C:/Users/Usuario/Desktop/Escritorio/Trabajo Programacion/InterfazGrafica/Recibos/{nombreReformulado}"):
    sobreEscribir = input("El archivo existe, desea sobre escribirlo? y/n:")
    if sobreEscribir == "y":
      return nombreReformulado
    else:
      return verificacion(input("Inserte un nuevo nombre para el archivo: "))
  else:
    return nombreReformulado

def verificacionV2(nombre_Pass):
  nombre_xlsx = nombre_Pass + ".xlsx"
  if os.path.exists(f"C:/Users/Usuario/Desktop/Escritorio/Trabajo Programacion/InterfazGrafica/Recibos/{nombre_xlsx}"):
    
    print("Existe")

    rango = range(100)
    
    for x in rango:
      nuevo_nombre = nombre_Pass + str(x)
      print(nuevo_nombre)
      if os.path.exists(f"C:/Users/Usuario/Desktop/Escritorio/Trabajo Programacion/InterfazGrafica/Recibos/{nuevo_nombre}"):
        pass
      else:
        break
        print(f"Modificado y retornado: {nuevo_nombre}")
      return nuevo_nombre + ".xlsx"
  else:
    return nombre_Pass + ".xlsx"

nombre = verificacion(input("Inserte el nombre del archivo: "))
print(nombre)
tiempoHoy = datetime.date.today()
myCursor = mydb.cursor()
idPass = input("Pase un id: ")
idPassRecurso = input("Pase el id del recurso a cargo: ")
honorarioBase = IdLimpioFunc(llamadaEspecifidaDB("HonorarioBase", 'cliente', "idCliente", idPass))
pagoAfip = 100
pagoIngresos = 200
pagoGanancias = 100
totalCostos = pagoAfip + pagoGanancias + pagoIngresos + honorarioBase
totalCostosConvertido = "$"+ str(totalCostos)
recurso = IdLimpioFunc(llamadaEspecifidaDB("nombre", "recurso", "idRecurso", idPassRecurso), "string")

listaPuntos = ["EN CONCEPTO DE: " ,"1) PAGO AFIP/MONOTRIBUTO/AUTONOMO", "2) PAGO AFIP GANANACIAS", "3) PAGO INGRESOS BRUTOS", "4) HONORARIOS IMPOSITIVOS Y CONTABLES", "SIENDO UN TOTAL DE"]
listaCostos = [pagoAfip, pagoIngresos, pagoGanancias, honorarioBase, totalCostosConvertido]

workBook = xlsxwriter.Workbook(f"C:/Users/Usuario/Desktop/Escritorio/Trabajo Programacion/InterfazGrafica/Recibos/{nombre}", {'strings_to_numbers': True})
workSheet = workBook.add_worksheet("Recibo")
estiloBasico_Font8 = workBook.add_format({'bold': True, 'font_size': 8})
estiloBasico_Font10 = workBook.add_format({'bold': True, 'font_size': 10})
estiloDerecha_Font10 = workBook.add_format({'bold': True, 'font_size': 10})

estiloDerecha_Font10.set_align('right')

workSheet.set_column('A:A', 51)
workSheet.set_column('D:D', 23.5)
workSheet.set_column('E:E', 12)

workSheet.insert_image('A1', 'iconoNombreEstudio.png', {'x_scale': 1.22, 'y_scale': 1.12})
workSheet.insert_image('A20', 'contactoRecibo.JPG', {'x_scale':1.195, 'y_scale': 1.05})

workSheet.write("D7", "El dia de la Fecha", estiloBasico_Font10)
workSheet.write("E7", str(tiempoHoy), estiloDerecha_Font10)
workSheet.write("A9", "POR EL PRESENTE RECIBI Y ACEPTO CONFORME EL PAGO INTEGRO DEL SEÑOR/A:", estiloBasico_Font8)
workSheet.write("E9", "Lucero Osvaldo", estiloDerecha_Font10)

listaVertical(9 , 0, listaPuntos, estiloBasico_Font8)
listaVertical(10, 4, listaCostos, estiloBasico_Font10)

workSheet.write("D17", recurso, estiloDerecha_Font10)
workSheet.write("D18", "CPCEPSL Mat. 2234 U.N.S.L.", estiloDerecha_Font10)

workBook.close()