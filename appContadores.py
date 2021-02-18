import sys
from PyQt5 import QtWidgets 
from PyQt5 import *
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer,QEventLoop
############################ Conectamos Base de  Datos
import mysql.connector 
############################ Importamos para disponer de "sleep"
import time
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Tilacino1",
  database="jugando_con_basedatos"
)
############################ Creamos Cursor para manipular Base de Datos
myCursor = mydb.cursor()
############################ Creamos Funcion para limpiar los IDs retornados por la "DB"
def IdLimpioFunc(idpass):
    Id_Limpio_Lista=[]
    id_Str = str(idpass)

    for IdFor in id_Str:
        if IdFor == "(":
            continue
        elif IdFor == ",":
            break
        Id_Limpio_Lista.append(IdFor)
        Idlimpio_str=''.join(Id_Limpio_Lista)
        Idlimpio=int(Idlimpio_str)

    return Idlimpio
############################ Variable "global" la cual contiene la fecha del momento en el que es llamado
tiempoHoy = datetime.date.today()

ui_direccion = "C:/Users/Usuario/Desktop/Escritorio/Trabajo Programacion/App/UIs/"

class  Presentacion(QDialog):
        def __init__(self):
            super(Presentacion,self).__init__()
            ############################ Cargamos la interfaz
            loadUi(ui_direccion + "Presetacion.ui",self) 
            self.Registrarse_boton.clicked.connect(self.Registrarse)
            self.Iniciar_sesion_boton.clicked.connect(self.IniciarSesion)
        ############################ Funcion para cambiar de ventana a Registro
        def Registrarse(self): 
            reg = Registrarse_Widgtet()
            widget.addWidget(reg)
            widget.setCurrentIndex(widget.currentIndex()+1)
        ############################ Funcion para ir a Inicio de Sesion
        def IniciarSesion(self):
            ing = Iniciar_Sesion_Widgtet()
            widget.addWidget(ing)
            widget.setCurrentIndex(widget.currentIndex()+1)

############################ Definimos la clase de la ventana
class Registrarse_Widgtet(QDialog):
        def __init__(self):
            super(Registrarse_Widgtet,self).__init__()
            ############################ Cargamos su interfaz
            loadUi(ui_direccion + "Registro.ui",self) 
            ############################ Conectamos botones a las funciones correspondientes
            self.Ing_Boton.clicked.connect(self.IniciarSesion)
            self.Registrarse_boton.clicked.connect(self.CrearCuenta)
            self.Error_Label_Registro.hide()
            self.GmailCrear.setPlaceholderText("GMAIL")
            self.ContrasenaCrear.setPlaceholderText("CONTRASEÑA")
            self.ContrasenaConfirmar.setPlaceholderText("CONFIRMAR")
            self.NombreText.setPlaceholderText("NOMBRE")
            self.checkBoxMostrarContra.stateChanged.connect(self.OcultarContrasena)

        def OcultarContrasena(self):
            estado = self.checkBoxMostrarContra.checkState()

            if estado == 0:
                self.ContrasenaCrear.setEchoMode(0)
                self.ContrasenaConfirmar.setEchoMode(0)
            elif estado == 2:
                self.ContrasenaCrear.setEchoMode(2)
                self.ContrasenaConfirmar.setEchoMode(2)
            else:
                print("OCURRIO UN ERROR!!!")

        ############################ Creamos funcion para crear cuenta
        def CrearCuenta(self): 
            Email =  str(self.GmailCrear.text())
            Contrasena = str(self.ContrasenaCrear.text())
            ConfirmarContra = str(self.ContrasenaConfirmar.text())
            Nombre = str(self.NombreText.text())

            myCursor.execute("SELECT gmail FROM recurso WHERE gmail = %s",(Email,))
            myResultado = myCursor.fetchall()
            ############################ Preparamos el insert en la "DB"
            sql = "INSERT INTO recurso (nombre, gmail, pass) VALUES (%s, %s, %s)"
            val = (Nombre, Email, Contrasena)
            ############################ Si la clave insertada es igual a la clave de confirmacion creamos cuenta
            for iteracion in (Nombre, Email, Contrasena):
                pass
            if iteracion == "":
                self.Error_Label_Registro.show()
                self.Error_Label_Registro.setText("INSERTE TODOS LOS DATOS")
                loop = QEventLoop()
                QTimer.singleShot(2500, loop.quit)
                loop.exec_()
                self.Error_Label_Registro.hide()
            elif myResultado == []:
                if Contrasena == ConfirmarContra:
                    try: 
                        myCursor.execute(sql, val)
                        mydb.commit()
                        inicairSesion = Iniciar_Sesion_Widgtet()
                        widget.addWidget(inicairSesion)
                        widget.setCurrentIndex(widget.currentIndex()+1)
                    except:
                        print("Error en CrearCuenta")
                elif Contrasena != ConfirmarContra:
                    self.Error_Label_Registro.show()
                    self.Error_Label_Registro.setText("LAS CONTRASEÑAS DEBEN SER IGUALES")
                    loop = QEventLoop()
                    QTimer.singleShot(2500, loop.quit)
                    loop.exec_()
                    self.Error_Label_Registro.hide()
            else:
                self.Error_Label_Registro.show()
                self.Error_Label_Registro.setText("ESTE EMAIL YA EXISTE")
                loop = QEventLoop()
                QTimer.singleShot(2500, loop.quit)
                loop.exec_()
                self.Error_Label_Registro.hide()
                
        ############################ Repetimos funcion para poder cambiar a inicio de sesion, hay que solucionar esto
        def IniciarSesion(self):
            ing = Iniciar_Sesion_Widgtet()
            widget.addWidget(ing)
            widget.setCurrentIndex(widget.currentIndex()+1)

############################ Creamos la clase "Iniciar_Sesion_Widgtet"
class Iniciar_Sesion_Widgtet(QDialog):
    def __init__(self):
        super(Iniciar_Sesion_Widgtet,self).__init__()
        loadUi(ui_direccion + "Iniciar_Sesion.ui",self)
        self.Registrarse_boton.clicked.connect(self.Registrarse)
        self.Ing_Final.clicked.connect(self.Ing_Ver)
        self.Error_Label_Registro.hide()
        self.GmailIniciar.setPlaceholderText("GMAIL")
        self.ContrasenaIniciarSesion.setPlaceholderText("CONTRASEÑA")
        self.checkBoxMostrarContra.stateChanged.connect(self.OcultarContrasena)
    ############################ Funcion para cambiar de ventana a Registro

    def OcultarContrasena(self):
        estado = self.checkBoxMostrarContra.checkState()

        if estado == 0:
            self.ContrasenaIniciarSesion.setEchoMode(0)
        elif estado == 2:
            self.ContrasenaIniciarSesion.setEchoMode(2)
        else:
            print("OCURRIO UN ERROR!!!")

    def Registrarse(self): 
            reg = Registrarse_Widgtet()
            widget.addWidget(reg)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def Ing_Ver(self): 
        Gmail_Ing = str(self.GmailIniciar.text())
        Contra_Ing = str(self.ContrasenaIniciarSesion.text())
        ############################ Hacemos select de las claves
        myCursor.execute("SELECT pass FROM recurso WHERE gmail = %s ",(Gmail_Ing,))
        ############################ Comparamos clave insertada con las claves retorndadas de la DB
        Gmail_Result =str(myCursor.fetchone())
        Contrasena_Sucia = '('+"'"+Contra_Ing+"'"+',)'
        ############################ Si son iguales confirmamos el usuario
        if Gmail_Result == Contrasena_Sucia:
            #try:
                ############################ Avanzamos a la "Pantalla principal"
                mainW = Pantalla_Principal()
                widget.addWidget(mainW)
                widget.setCurrentIndex(widget.currentIndex()+1)
            #except:
                ################################ Aparecen los carteles de error, podriamos mejorar esto, cambiandolo por un .show y utilizando una sola etiqueta que se modifique
                self.Error_Label_Registro.show()
                self.Error_Label_Registro.setText("OCURRIO UN ERROR, REINICIA LA APLICACION")
                loop = QEventLoop()
                QTimer.singleShot(2500, loop.quit)
                loop.exec_()
                self.Error_Label_Registro.hide()
        else:
            self.Error_Label_Registro.show()
            self.Error_Label_Registro.setText("LOS DATOS NO COINCIDEN")
            loop = QEventLoop()
            QTimer.singleShot(2500, loop.quit)
            loop.exec_()
            self.Error_Label_Registro.hide()
            
class Pantalla_Principal(QMainWindow):
    def __init__(self):
        super(Pantalla_Principal,self).__init__()
        loadUi(ui_direccion + "MainTitle.ui", self)
        ############################# Cargamos las personas en el "ComboBoxTipoPersona"
        listaTipoPersona = ["Fisica", "Juridica"]
        self.ComboBoxTipoPersona.addItems(listaTipoPersona)
        ############################ Cargamos datos en "ComboBoxCondicionFrenteFisco"
        listaCondicionesFrenteFisco = ["Monotributista", "Responsable Inscripto"]
        self.ComboBoxCondicionFrenteFisco.addItems(listaCondicionesFrenteFisco)
        ############################ Cargamos datos en "ComboBoxActividadCliente"
        listaActividadClientes = ["ACTIVO", "INACTIVO"]
        self.ComboBoxActividadCliente.addItems(listaActividadClientes)
        ############################# Conectamos el boton para generar el cliente
        self.GenerarClienteBoton.clicked.connect(self.OnCliente)
        ############################# Redimensionamos la pantalla
        widget.setFixedHeight(800)
        widget.setFixedWidth(1275)
        ############################ Ocultamos el cuadro para generar cliente
        self.MarcoClienteBloq.hide()
        ############################ Definimos el boton para generar el cliente
        self.EnviarBotonBloq_2.clicked.connect(self.CrearCliente)
        self.ClienteInsertadoLabel.hide()
        ############################ Definimos el boton para cancelar al cliente
        self.CancelarBotonBloq_2.clicked.connect(self.OffCliente)
        ############################ Establecemos el ancho de las columnas
        self.TablaClientes.setColumnWidth(0, 250)
        self.TablaClientes.setColumnWidth(1, 125)
        self.TablaClientes.setColumnWidth(3, 125)
        self.TablaClientes.setColumnWidth(4, 116)
        ############################ Cargamos los datos
        self.pedidaDatos("Cliente")
        ############################ Boton para añadir datos de contacto
        self.BotonDatosDeContacto.clicked.connect(self.prepararContacto)
        self.BotonDatosDeContacto_State2.hide()
        ############################ Enviamos los datos
        self.BotonDatosDeContacto_State2.clicked.connect(self.ClienteContacto)
        ############################ Ocultamos las partes que no queremos que se vean por defecto
        self.ComboBoxIDcliente.hide()
        self.EditarClienteBotonForm.hide()
        ############################ Insertamos un boton para mostrarlas
        self.EditarClienteBoton.clicked.connect(lambda: self.PrepararEditarCliente(1))
        ############################
        self.EditarClienteBotonForm.clicked.connect(self.EnviarEdicion)
        ############################ Llenamos los ID
        self.IdComboBox()
        ############################ Eliminamos el ID seleccionado
        self.ComboBoxIdEliminar.activated.connect(self.EliminarCliente)
        ############################ Cargamos las opciones de tabla en el "ComboBoxTablasElegir"
        ListaTablas=["Cliente","Cuenta Corriente"]
        self.ComboBoxTablasElegir.addItems(ListaTablas)
        ############################ Conectamos el "ComboBox" para generar las funcionalidades
        self.ComboBoxTablasElegir.activated.connect(self.CambiarTabla)
        ############################ Conectamos el "CheckBox" a la barra lateral y al boton que lo activa
        self.checkBox_SideBar.stateChanged.connect(self.SideBar)
        self.checkBox_SideBar.hide()
        self.SideBarBoton.clicked.connect(self.CambioEstado)
        ############################ Ocultamos por defecto de "BarraLateral"
        self.BarraLateral.hide()
        ############################ Conectamos boton para cerrar sesion
        self.CerraSesionBoton.clicked.connect(self.IniciarSesion)
        ############################ Establecemos el "placeHolderText"
        self.devengadoLineEdit.setPlaceholderText("Devengado")
        ############################ Conectamos boton para mostrar los campos necesarios para percibir al cliente
        self.PercibirClienteBoton.clicked.connect(self.prepararPercibirCliente)
        ############################ Conectamos el boton que enviara los datos para percibir al cliente
        self.PercibirClieteBotonForm_2.clicked.connect(self.percibirCliente)

    def idRecursos(self):
        myCursor.execute("SELECT nombre FROM recurso")
        resultado=[]
        listaRecursos=[]
        resultado = myCursor.fetchall()

        self.ComboBoxRecursos.clear()

        for elemento in resultado:
            elemento_str= "RECURSO" + "" + str(elemento) 
            listaRecursos.append(elemento_str)

        self.ComboBoxRecursos.addItems(listaRecursos)

    ############################ Funcion que se conecta a la funcion "cuentaCorriente" para percibir al cliente
    def percibirCliente(self):
        montoPercibido=self.NombreCampTextBloq_2.text()
        try:
            idCliente=IdLimpioFunc(self.ComboBoxIDcliente.currentText())
        except:
            self.ClienteInsertadoLabel.show()
            self.ClienteInsertadoLabel.setText("CREE UN CLIENTE")
            loop = QEventLoop()
            QTimer.singleShot(5000, loop.quit)
            loop.exec_()
            self.ClienteInsertadoLabel.hide()
        
        if montoPercibido == "":
            self.ClienteInsertadoLabel.show()
            self.ClienteInsertadoLabel.setText("INSERTE UN MONTO")
            loop = QEventLoop()
            QTimer.singleShot(5000, loop.quit)
            loop.exec_()
            self.ClienteInsertadoLabel.hide()
        else:
            try:
                self.cuentaCorriente(0, montoPercibido, idCliente, "PercibirCliente")
                self.pedidaDatos("Cuenta Corriente")
            except:
                self.NombreCampTextBloq_2.clear()
                self.ClienteInsertadoLabel.show()
                self.ClienteInsertadoLabel.setText("OCURRIO UN ERROR CON LA CUENTA CORRIENTE")
                loop = QEventLoop()
                QTimer.singleShot(5000, loop.quit)
                loop.exec_()
                self.ClienteInsertadoLabel.hide()
    ############################ Funcion que se utiliza para crear datos en la cuenta corriente y editar los existentes
    def cuentaCorriente(self, devengadopass = 0, percibidopass = 0, idCLientepass = 0, accion = "CrearCliente"):
        devengadoInt=int(devengadopass)
        percibidoInt=int(percibidopass)
        ############################ Creamos condicional para saber si debemos crear los datos del cliente o editarlos 
        if idCLientepass == 0 and devengadopass != 0 and accion == "CrearCliente":
            try:
                totalDeuda = devengadoInt - percibidoInt
                myCursor.execute("SELECT MAX(idCliente) FROM cliente")
                ############################ Limpiamos el "id" que nos retorno la "DB"
                idLimpio = IdLimpioFunc(str(myCursor.fetchone()))
                ############################ Insertamos los datos en la "DB", tabla "cuentacorriente"
                sql_Insert = "INSERT INTO cuentacorriente (idCliente, Devengado, Percibido, Total_Deuda) VALUES (%s, %s, %s, %s)"
                val_Insert = (idLimpio, devengadoInt,percibidoInt, totalDeuda)
                ############################ Enviamos los datos a la "DB"
                myCursor.execute(sql_Insert, val_Insert)
                mydb.commit()
            except:
                self.ClienteInsertadoLabel.show()
                self.ClienteInsertadoLabel.setText("OCURRIO UN ERROR CON LA CUENTA CORRIENTE CREANDO")
                loop = QEventLoop()
                QTimer.singleShot(5000, loop.quit)
                loop.exec_()
                self.ClienteInsertadoLabel.hide()

        elif idCLientepass != 0 and devengadopass != 0 and accion == "EditarCliente":
            try:
                myCursor.execute("SELECT Percibido FROM cuentacorriente WHERE idCliente = %s ",(idCLientepass,))
                percibidoDB=IdLimpioFunc(myCursor.fetchone())

                deudaRecalculada = devengadoInt - percibidoDB

                updatePercibir = "UPDATE `cuentacorriente` SET `Devengado` = %s, `Total_Deuda` = %s WHERE idCliente = %s"
                valoresPercibir = (devengadoInt, deudaRecalculada, idCLientepass)

                myCursor.execute(updatePercibir, valoresPercibir)
                mydb.commit()

            except:
                self.ClienteInsertadoLabel.resize(540, 71)

                self.ClienteInsertadoLabel.show()
                self.ClienteInsertadoLabel.setText("OCURRIO UN ERROR CON LA CUENTA CORRIENTE EDITANDO")
                loop = QEventLoop()
                QTimer.singleShot(5000, loop.quit)
                loop.exec_()
                self.ClienteInsertadoLabel.hide()
                self.ClienteInsertadoLabel.resize(350, 71)

        elif idCLientepass != 0 and percibidopass != 0 and accion == "PercibirCliente":
            try:
                ############################ Tomamos los datos de "devengado" del cliente a traves del "id"
                pago_afip = self.CuitCampTextBloq_2.text()
                pago_ingresos_brutos = self.ClaveFiscalCampTextBloq_2.text()
                afip_monotributo_autonomo = self.HonorarioBaseCampTextBloq_2.text()

                myCursor.execute("SELECT Devengado FROM cuentacorriente WHERE idCliente = %s ",(idCLientepass,))
                devengadoDB = IdLimpioFunc(myCursor.fetchone())
                ############################ Calculamos la deuda nuevamente con los datos obtenidos
                deudaRecalculada = devengadoDB-percibidoInt
                ############################ Actualizamos los datos a insertar del cliente
                editarDevengar = "UPDATE `cuentacorriente` SET `Percibido` = %s, `Total_Deuda` = %s, `Fecha` = %s, `Pago_Afip_Monotributo_Autonomo` = %s, `Ingresos_Brutos` = %s, `Pago_Afip_Ganancias` = %s WHERE idCliente = %s"
                valoresEditar = (percibidoInt, deudaRecalculada, tiempoHoy, pago_afip, pago_ingresos_brutos, afip_monotributo_autonomo,idCLientepass)
                ############################ Insertamos los nuevos datos
                myCursor.execute(editarDevengar, valoresEditar)
                mydb.commit()
                ############################ Limpiamos el "lineText" correspondiente y mostramos una etique que notifica la insercion
                self.NombreCampTextBloq_2.clear()
                self.CuitCampTextBloq_2.clear()
                self.ClaveFiscalCampTextBloq_2.clear()
                self.HonorarioBaseCampTextBloq_2.clear()
                ############################ Mostramos la etiqueta que muestra la insercion
                self.ClienteInsertadoLabel.show()
                self.ClienteInsertadoLabel.setText("SE PERCIBIO CORRECTAMENTE")
                ############################ Seteamos un loop para desaparecer la etiqueta antes mostrada
                loop = QEventLoop()
                QTimer.singleShot(2500, loop.quit)
                loop.exec_()
                self.ClienteInsertadoLabel.hide()
            except:
                self.ClienteInsertadoLabel.resize(540, 71)
                self.NombreCampTextBloq_2.clear()
                self.ClienteInsertadoLabel.show()
                self.ClienteInsertadoLabel.setText("OCURRIO UN ERROR CON LA CUENTA CORRIENTE")
                loop = QEventLoop()
                QTimer.singleShot(5000, loop.quit)
                loop.exec_()
                self.ClienteInsertadoLabel.hide()
                self.ClienteInsertadoLabel.resize(350, 71)

    ############################
    def prepararPercibirCliente(self):
        self.prepararContacto()
        self.MarcoClienteBloq.show()
        ############################
        self.NombreCampTextBloq_2.setPlaceholderText("MONTO HONORARIO A PERCIBIR")
        self.CuitCampTextBloq_2.setPlaceholderText("AFIP GANANCIAS")
        self.ClaveFiscalCampTextBloq_2.setPlaceholderText("PAGO INGRESOS BRUTOS")
        self.HonorarioBaseCampTextBloq_2.setPlaceholderText("AFIP/MONOTRIBUTO/AUTONOMO")
        ############################
        self.PercibirClieteBotonForm_2.show()
        ############################
        self.BotonDatosDeContacto_State2.hide()

    def IniciarSesion(self):
        Pres = Presentacion()
        widget.addWidget(Pres)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setFixedHeight(620)
        widget.setFixedWidth(400)
    ############################
    def SideBar(self):
        estado = self.checkBox_SideBar.checkState()
        ############################
        if estado == 0:
            self.BarraLateral.hide()
            self.SideBarBoton.resize(40,41)
        elif estado == 2:
            self.BarraLateral.show()
            self.SideBarBoton.resize(181,40)
        else:
            print("ALGO SALIO MAL!!!")
    ############################
    def CambioEstado(self):
        self.checkBox_SideBar.nextCheckState()
    ############################
    def CambiarTabla(self):
        ############################ Titulos tabla "Cliente"
        Titulo_Nombre=QtWidgets.QTableWidgetItem("Nombre y apellido/denominacion")
        Titulo_TipoPersona=QtWidgets.QTableWidgetItem("Tipo de Persona")
        Titulo_Cuit=QtWidgets.QTableWidgetItem("Cuit")
        Titulo_Recurso=QtWidgets.QTableWidgetItem("Recurso")
        Titulo_Condicion=QtWidgets.QTableWidgetItem("Condicion")
        ############################ Titulos tabla "Cuenta Corriente"
        Titulo_Cliente=QtWidgets.QTableWidgetItem("Cliente")
        Titulo_Devengado=QtWidgets.QTableWidgetItem("Devengado")
        Titulo_Percibido=QtWidgets.QTableWidgetItem("Percibido")
        Titulo_Fecha=QtWidgets.QTableWidgetItem("Fecha")
        Titulo_TotalDeuda=QtWidgets.QTableWidgetItem("Total Deuda")
        Titulo_TotalPercibido=QtWidgets.QTableWidgetItem("Total Percibido")
        ############################ Medimos cual es la tabla elegida
        TablaElegida=self.ComboBoxTablasElegir.currentText()
        ############################ Cambiamos la tabla en funcion de la que se eligio
        if TablaElegida == "Cuenta Corriente":
            ############################ Modificamos el tamano de la tabla
            self.TablaClientes.resize(850, 531)
            self.TablaClientes.move(0, 140)
            ############################ Agregamos otra columna
            self.TablaClientes.setColumnCount(6)
            ############################ Cambiamos el tamaño de la primera columna
            self.TablaClientes.setColumnWidth(0, 150)
            ############################ Cambiamos los titulos
            self.TablaClientes.setHorizontalHeaderItem(0, Titulo_Cliente)
            self.TablaClientes.setHorizontalHeaderItem(1, Titulo_Devengado)
            self.TablaClientes.setHorizontalHeaderItem(2, Titulo_Percibido)
            self.TablaClientes.setHorizontalHeaderItem(3, Titulo_Fecha)
            self.TablaClientes.setHorizontalHeaderItem(4, Titulo_TotalDeuda)
            self.TablaClientes.setHorizontalHeaderItem(5, Titulo_TotalPercibido)

        elif TablaElegida == "Cliente":
            ############################ Modificamos el tamano de la tabla
            self.TablaClientes.resize(731, 531)
            self.TablaClientes.move(110, 140)
            ############################ Restablecemos la cantidad de columnas
            self.TablaClientes.setColumnCount(5)
            ############################ Cambiamos el tamaño de la primera columna
            self.TablaClientes.setColumnWidth(0, 250)
            ############################ Cambiamos los titulos
            self.TablaClientes.setHorizontalHeaderItem(0, Titulo_Nombre)
            self.TablaClientes.setHorizontalHeaderItem(1, Titulo_TipoPersona)
            self.TablaClientes.setHorizontalHeaderItem(2, Titulo_Cuit)
            self.TablaClientes.setHorizontalHeaderItem(3, Titulo_Recurso)
            self.TablaClientes.setHorizontalHeaderItem(4, Titulo_Condicion)

        self.pedidaDatos(TablaElegida)
    ################################ Creamos el metodo "EliminarCliente"
    def EliminarCliente(self):
        idSeleccionado=self.ComboBoxIdEliminar.currentText()
        ################################ Llamamos a la funcion "IdLimpioFunc", la cual nos retorna el valor limpio
        IdEliminarCliente=IdLimpioFunc(idSeleccionado)
        ################################ Preparamos el DELETE de la "DB"
        sql = "DELETE FROM cliente WHERE idCliente = %s"
        ################################ Ejecutamos el DELETE
        myCursor.execute(sql, (IdEliminarCliente,))
        mydb.commit()
        ################################ Actualizamos la tabla de clientes y los IDs
        self.pedidaDatos("Cliente")
        self.IdComboBox()
    ################################ Metodo para cargar los IDs en los "ComboBox" pertinentes
    def IdComboBox(self):
        ################################ Hago select para retornar los IDs desde la "DB"
        myCursor.execute("SELECT idCliente ,Nombre_Apellido_Denominacion FROM cliente")
        listaId=[]
        myResultado=[]
        ################################ Limpio los "ComboBox" y asi evitar la repeticion de datos
        self.ComboBoxIDcliente.clear()
        self.ComboBoxIdEliminar.clear()
        ################################ Retornamos todos los IDs
        myResultado = myCursor.fetchall()
        ################################ Iteramos los elementos retornados por la DB, los convertimos a
        ################################ string y los añadimos a una lista.
        for elemento in myResultado:
            elemento_str=str(elemento)
            listaId.append(elemento_str)
        ################################ Agregamos las listas a los "ComboBox" pertinentes
        self.ComboBoxIDcliente.addItems(listaId)
        self.ComboBoxIdEliminar.addItems(listaId)

    def PrepararEditarCliente(self, valorVerificacion=0):
        ############################
        self.OnCliente()
        ############################ Motramos los campos
        idCliente = self.ComboBoxIDcliente.currentText()
        ############################ Mostramos solo los campos elegidos
        self.ComboBoxIDcliente.show()
        self.EditarClienteBotonForm.show()
        ############################ Preparamos los ID de los clinetes para rellenar el "Combo Box"
        if idCliente == "":
            self.IdComboBox()
        ############################ Redimensionamos y ubicamos el "IDComboBox"
        self.ComboBoxIDcliente.resize(150, 40)
        self.ComboBoxIDcliente.move(250, 90)
        ############################ Redimensionamos y ubicamos el "LineText" de nombre
        self.NombreCampTextBloq_2.resize(240, 40)

        if valorVerificacion == 1:
            self.ComboBoxIDcliente.activated.connect(lambda: self.PrepararEditarCliente(1))
            idClienteEditado = IdLimpioFunc(self.ComboBoxIDcliente.currentText())

            self.NombreCampTextBloq_2.clear()
            self.CuitCampTextBloq_2.clear()
            self.ClaveFiscalCampTextBloq_2.clear()
            self.HonorarioBaseCampTextBloq_2.clear()

            myCursor.execute("SELECT Nombre_Apellido_Denominacion, Cuit, ClaveFiscalAfip, HonorarioBase FROM cliente WHERE idcliente = %s",(idClienteEditado,))
            resultado = []
            resultado = myCursor.fetchall()

            for x in resultado:
                self.NombreCampTextBloq_2.setText(x[0])
                self.CuitCampTextBloq_2.setText(x[1])
                self.ClaveFiscalCampTextBloq_2.setText(x[2])
                self.HonorarioBaseCampTextBloq_2.setText(str(x[3]))

    def EnviarEdicion(self):
        ############################ Convertimos los tipos de datos y definimos las variables
        Tipo_Persona=self.ComboBoxTipoPersona.currentText()
        Nombre=str(self.NombreCampTextBloq_2.text())
        Cuit=str(self.CuitCampTextBloq_2.text())
        Clave_Fiscal=str(self.ClaveFiscalCampTextBloq_2.text())
        Condicion_Frente_Fisco=self.ComboBoxCondicionFrenteFisco.currentText()
        Recurso_Responsable=self.ComboBoxRecursos.currentText()
        Horario_Base=str(self.HonorarioBaseCampTextBloq_2.text())
        Estado_Actividad=self.ComboBoxActividadCliente.currentText()
        ############################ Variable que contiene el texto del "ComboBox"
        idSeleccionado=self.ComboBoxIDcliente.currentText()
        ############################ Valor de verificacion
        valor=0
        ############################ For que nos permite  verificar que todos los datos allan sido incertados
        for iteracion in (Tipo_Persona, Nombre, Cuit, Clave_Fiscal, Condicion_Frente_Fisco, Recurso_Responsable, Horario_Base, Estado_Actividad):
            pass
        ############################ Guardamos el valor retornado por la funcion
        try:
            IdEnviarEdicion=IdLimpioFunc(idSeleccionado)
            ############################ Realizamos el Update en la "DB"
            sql = """UPDATE cliente SET Tipo_Persona = %s, Nombre_Apellido_Denominacion = %s, 
            Cuit = %s, ClaveFiscalAfip = %s, CondicionFrenteAlFisco = %s, 
            RecursoResponsable = %s, HonorarioBase = %s WHERE idCliente = %s"""
            valorEdicion = (Tipo_Persona, Nombre, Cuit, Clave_Fiscal, Condicion_Frente_Fisco, Recurso_Responsable, Horario_Base, IdEnviarEdicion)
            ############################ Verificamos si todo esta listo para incertar los datos en la "DB"
            if iteracion == "":
                self.ClienteInsertadoLabel.show()
                self.ClienteInsertadoLabel.setText("INSERTE TODOS LOS DATOS")
            else:
                try:
                    myCursor.execute(sql, valorEdicion)
                    mydb.commit()
                    valor=+1
                except:
                    self.ClienteInsertadoLabel.setText("ALGO SALIO MAL EN LA INSERSION DE DATOS")
            ############################ Verificamos que todo se haya insertado correctamente y lo reflejamos
            if myCursor.rowcount == 1 and valor == 1:
                 try:  
                     self.ClienteInsertadoLabel.show()
                     self.ClienteInsertadoLabel.setText(Nombre + " " + "FUE INSERTADO")
                     ############################ Limpiamos las "LineEdit"
                     self.NombreCampTextBloq_2.clear()
                     self.CuitCampTextBloq_2.clear()
                     self.ClaveFiscalCampTextBloq_2.clear()
                     self.HonorarioBaseCampTextBloq_2.clear()
                 except:
                     self.ClienteInsertadoLabel.setText("NO SE PUDO INSERTAR")
            elif myCursor.rowcount != 1 and valor == 1 :
                self.ClienteInsertadoLabel.setText("OCURRIO UN ERROR, REINICIE")
            ############################ Cargamos el cliente y actulizamos la tabla
            self.pedidaDatos("Cliente")
            self.IdComboBox()
            
            ############################ Establecemos un sleep de 2 segundos y medio, posteriormente ocultamos la alerta
            loop = QEventLoop()
            QTimer.singleShot(2500, loop.quit)
            loop.exec_()
            self.ClienteInsertadoLabel.hide()
            self.cuentaCorriente(Horario_Base, 0, IdEnviarEdicion, "EditarCliente")
        except:
            self.ClienteInsertadoLabel.show()
            self.ClienteInsertadoLabel.setText("CREE UN CLIENTE")
            loop = QEventLoop()
            QTimer.singleShot(5000, loop.quit)
            loop.exec_()
            self.ClienteInsertadoLabel.hide()       

    def cargarDatos(self, resultadoRecorrer, conteoDatos):
        self.TablaClientes.clearContents()
        ############################ Hacemos SELECT de los datos necesarios para la tabla
        celdaTabla = 0
        self.TablaClientes.setRowCount(conteoDatos)
        ############################ Hacemos un row que recorre todas las "rows" correspondientes e inserta los datos
        for row in resultadoRecorrer:
            if row == "" or row == None or resultadoRecorrer == "" or resultadoRecorrer == None or row == [] or resultadoRecorrer == []:
                self.TablaClientes.clearContents()
            else:
                self.TablaClientes.setItem(celdaTabla, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                self.TablaClientes.setItem(celdaTabla, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                self.TablaClientes.setItem(celdaTabla, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                self.TablaClientes.setItem(celdaTabla, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                self.TablaClientes.setItem(celdaTabla, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                celdaTabla+=1

    def pedidaDatos(self, tablaSeleccionada):
        if tablaSeleccionada == "Cliente":
            try:
                myCursor.execute("SELECT Nombre_Apellido_Denominacion, Tipo_Persona, Cuit, RecursoResponsable, CondicionFrenteAlFisco FROM cliente")
                resultado = myCursor.fetchall()
                conteoResultado = len(resultado)

                self.cargarDatos(resultado, conteoResultado)
            except:
                self.ClienteInsertadoLabel.show()
                self.ClienteInsertadoLabel.setText("OCURRIO UN ERROR EN LA PEDIDA DE DATOS")

        elif tablaSeleccionada == "Cuenta Corriente":
            try:
                sql = "SELECT \
                    cliente.Nombre_Apellido_Denominacion AS nombre, \
                    cuentacorriente.Devengado AS devengado, \
                    cuentacorriente.Percibido AS percibido, \
                    cuentacorriente.Fecha as fecha, \
                    cuentacorriente.Total_Deuda as deudaTotal, \
                    cuentacorriente.Total_Percibido as percibidoTotal \
                    FROM cliente \
                    INNER JOIN cuentacorriente ON cliente.idCliente = cuentacorriente.idCliente"
                
                myCursor.execute(sql)                
                resultado = myCursor.fetchall()
                conteoResultado = len(resultado)

                self.cargarDatos(resultado, conteoResultado)
            except:
               self.ClienteInsertadoLabel.show()
               self.ClienteInsertadoLabel.setText("OCURRIO UN ERROR EN LA PEDIDA DE DATOS")
    def OnCliente(self):
        ############################ Volvemos todo a la normalidad por si se hubiera pulsado el boton de "Contacto"
        self.NombreCampTextBloq_2.clear()
        self.CuitCampTextBloq_2.clear()
        self.ClaveFiscalCampTextBloq_2.clear()
        self.HonorarioBaseCampTextBloq_2.clear()
        ############################ Definimos los nombres de los campos por defecto
        self.NombreCampTextBloq_2.setPlaceholderText("NOMBRE")
        self.CuitCampTextBloq_2.setPlaceholderText("CUIT")
        self.ClaveFiscalCampTextBloq_2.setPlaceholderText("CLAVE FISCAL")
        self.HonorarioBaseCampTextBloq_2.setPlaceholderText("HONORARIO BASE")
        ############################ Ocultamos la partes de "Editar Cliente"
        self.ComboBoxIDcliente.hide()
        self.BotonDatosDeContacto_State2.hide()
        self.EditarClienteBotonForm.hide()
        self.PercibirClieteBotonForm_2.hide()
        ############################ Reaparecemos las cosas que habrian desaparecido en caso de "Editar Cliente"
        self.NombreCampTextBloq_2.show()
        self.CuitCampTextBloq_2.show()
        self.MarcoClienteBloq.show()
        self.ComboBoxTipoPersona.show()
        self.ClaveFiscalCampTextBloq_2.show()
        self.BotonDatosDeContacto.show()
        self.ComboBoxActividadCliente.show()
        self.ComboBoxCondicionFrenteFisco.show()
        self.HonorarioBaseCampTextBloq_2.show()
        self.PercibirClienteBoton.show()
        self.ComboBoxRecursos.show()
        ############################ Reajustamos el tamano de el "LineText" nombre
        self.NombreCampTextBloq_2.move(5, 90)
        self.CuitCampTextBloq_2.move(5, 210)
        self.ClaveFiscalCampTextBloq_2.move(5, 270)
        self.NombreCampTextBloq_2.resize(300, 40)
        self.idRecursos()

    def OffCliente(self):
        ############################ Boton ocultar "generar cliente"
        self.MarcoClienteBloq.hide()

    def CrearCliente(self):
        ############################Convertimos en string todos los datos de los "Line edits"
        Tipo_Persona=self.ComboBoxTipoPersona.currentText()
        Nombre=str(self.NombreCampTextBloq_2.text())
        Cuit=str(self.CuitCampTextBloq_2.text())
        Clave_Fiscal=str(self.ClaveFiscalCampTextBloq_2.text())
        Condicion_Frente_Fisco=self.ComboBoxCondicionFrenteFisco.currentText()
        Recurso_Responsable=self.ComboBoxRecursos.currentText()
        Honorario_Base=str(self.HonorarioBaseCampTextBloq_2.text())
        Estado_Actividad=self.ComboBoxActividadCliente.currentText()
        ############################ Creamos un valor de verificacion
        valor=0
        ############################ Iteramos los "Line Edit" para averiguar si es que hay alguno vacio
        for iteracion in (Tipo_Persona, Nombre, Cuit, Clave_Fiscal, Condicion_Frente_Fisco, Recurso_Responsable, Honorario_Base, Estado_Actividad):
            None
        ############################ Preparamos los datos para enviarlos a la base de datos
        sql = """INSERT INTO cliente (Tipo_Persona, Nombre_Apellido_Denominacion, Cuit, 
        ClaveFiscalAfip, CondicionFrenteAlFisco, RecursoResponsable, HonorarioBase, 
        Estado_Actividad) Values (%s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (Tipo_Persona, Nombre, Cuit, Clave_Fiscal, Condicion_Frente_Fisco, Recurso_Responsable, Honorario_Base, Estado_Actividad)
        ############################ Verificamos si se han insertado todos los datos para ejecutar el cursor
        if iteracion == "":
            self.ClienteInsertadoLabel.show()
            self.ClienteInsertadoLabel.setText("INSERTE TODOS LOS DATOS")
            loop = QEventLoop()
            QTimer.singleShot(2500, loop.quit)
            loop.exec_()
            self.ClienteInsertadoLabel.hide()
        elif isinstance(Honorario_Base, str) == True:
            try:
                int(Honorario_Base)
                myCursor.execute(sql, val)
                mydb.commit()
                valor=+1
            except:
                self.ClienteInsertadoLabel.show()
                self.ClienteInsertadoLabel.setText("INSERTE UN NUMERO EN HONORARIO")
                loop = QEventLoop()
                QTimer.singleShot(2500, loop.quit)
                loop.exec_()
                self.ClienteInsertadoLabel.hide()
        ############################ Verificamos que todo se haya insertado correctamente y lo reflejamos
        if myCursor.rowcount == 1 and valor == 1:
             try:  
                 self.ClienteInsertadoLabel.show()
                 self.ClienteInsertadoLabel.setText(Nombre + " " + "FUE INSERTADO")
                 ############################ Limpiamos las "LineEdit"
                 self.NombreCampTextBloq_2.clear()
                 self.CuitCampTextBloq_2.clear()
                 self.ClaveFiscalCampTextBloq_2.clear()
                 self.HonorarioBaseCampTextBloq_2.clear()
                 ############################ Cargamos el cliente y actulizamos la tabla
                 if self.ComboBoxTablasElegir.currentText() == "Cliente":
                    self.pedidaDatos("Cliente")
                 elif self.ComboBoxTablasElegir.currentText() == "Cuenta Corriente":
                    self.pedidaDatos("Cuenta Corriente")
                 self.IdComboBox()
                 ############################ Establecemos un sleep de 2 segundos y medio, posteriormente ocultamos la alerta
                 loop = QEventLoop()
                 QTimer.singleShot(2500, loop.quit)
                 loop.exec_()
                 self.ClienteInsertadoLabel.hide()
                 self.cuentaCorriente(Honorario_Base)
             except:
                 self.ClienteInsertadoLabel.setText("NO SE PUDO INSERTAR")
        elif myCursor.rowcount != 1 and valor == 1 :
            self.ClienteInsertadoLabel.setText("OCURRIO UN ERROR, REINICIE")

    def prepararContacto(self):
        self.OnCliente()
        self.BotonDatosDeContacto_State2.show()
        self.ComboBoxIDcliente.show()
        ############################ Quitamos los campos de texto inutil
        self.ComboBoxTipoPersona.hide()
        self.BotonDatosDeContacto.hide()
        self.ComboBoxCondicionFrenteFisco.hide()
        self.ComboBoxActividadCliente.hide()
        self.ComboBoxRecursos.hide()
        ############################ Renombramos los que vamos a utilizar
        self.NombreCampTextBloq_2.setPlaceholderText("NOMBRE DE CONTACTO")
        self.CuitCampTextBloq_2.setPlaceholderText("TELEFONO")
        self.ClaveFiscalCampTextBloq_2.setPlaceholderText("MAIL")
        self.HonorarioBaseCampTextBloq_2.setPlaceholderText("DIRECCION")
        ############################ Acomodamos los campos existentes para hacer que se vea mas elegante
        self.ComboBoxIDcliente.resize(300, 40)
        self.ComboBoxIDcliente.move(5, 90)
        self.IdComboBox()

        self.NombreCampTextBloq_2.move(5, 330)
        self.NombreCampTextBloq_2.resize(300, 40)
        self.CuitCampTextBloq_2.move(5, 390)
        self.ClaveFiscalCampTextBloq_2.move(5, 450)
        
    def ClienteContacto(self):
        ############################ Convertimos en string todos los datos insertados
        Telefono=str(self.CuitCampTextBloq_2.text())
        Mail=str(self.ClaveFiscalCampTextBloq_2.text())
        Direccion=str(self.HonorarioBaseCampTextBloq_2.text())
        Nombre_Contacto=str(self.NombreCampTextBloq_2.text())
        idSeleccionado=self.ComboBoxIDcliente.currentText()
        try:
            IdContacto=IdLimpioFunc(idSeleccionado)
            ############################ Creamos un valor de verificacion
            valor=0
            ############################ Iteramos los "Line Edit" para averiguar si es que hay alguno esta vacio
            for iteracion in (Telefono, Mail, Direccion):
                pass
            ############################ Preparamos los datos para enviarlos a la base de datos
            sql_ClienteContacto = "INSERT INTO datosdecontacto (idCliente, Telefono, Nombre_Contacto, Mail, Direccion) Values (%s, %s, %s, %s, %s)"
            val_ClienteContacto = (IdContacto, Telefono, Nombre_Contacto, Mail, Direccion)
            ############################ Verificamos si se han insertado todos los datos para ejecutar el cursor
            if iteracion == "":
                self.ClienteInsertadoLabel.show()
                self.ClienteInsertadoLabel.setText("INSERTE TODOS LOS DATOS")
            else:
                try:
                    myCursor.execute(sql_ClienteContacto, val_ClienteContacto)
                    mydb.commit()
                    valor=+1
                except:
                    self.ClienteInsertadoLabel.setText("EL ID DEL CLIENTE NO COINCIDE")   
            ############################ Verificamos que todo se haya insertado correctamente y lo reflejamos
            if myCursor.rowcount == 1 and valor == 1:
                try:  
                 self.ClienteInsertadoLabel.show()
                 self.ClienteInsertadoLabel.setText("DATOS DE CONTACTO INSERTADOS")
            ############################ Limpiamos las "LineEdit"
                 self.NombreCampTextBloq_2.clear()
                 self.CuitCampTextBloq_2.clear()
                 self.HonorarioBaseCampTextBloq_2.clear()
                 self.ClaveFiscalCampTextBloq_2.clear()
                except:
                     self.ClienteInsertadoLabel.setText("NO SE PUDO INSERTAR")
            elif myCursor.rowcount != 1 and valor == 1 :
                self.ClienteInsertadoLabel.setText("OCURRIO UN ERROR, REINICIE")
            ############################ Establecemos un sleep de 2 segundos y medio, posteriormente ocultamos la alerta
            loop = QEventLoop()
            QTimer.singleShot(2500, loop.quit)
            loop.exec_()
            ############################ Ocultamos las partes de la interfaz pertinentes
            self.ClienteInsertadoLabel.hide()
            self.BotonDatosDeContacto_State2.hide()
            ############################ Mostramos las partes de la interfaz pertinentes
            self.BotonDatosDeContacto.show()
        except:
            self.ClienteInsertadoLabel.show()
            self.ClienteInsertadoLabel.setText("CREE UN CLIENTE")
            loop = QEventLoop()
            QTimer.singleShot(5000, loop.quit)
            loop.exec_()
            self.ClienteInsertadoLabel.hide()
        

app=QApplication(sys.argv)
mainwindow=Presentacion()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(620)
widget.setFixedWidth(400)
widget.show()
app.exec_()