import json
from datetime import datetime
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(level=logging.INFO , event_level=logging.ERROR)

sentry_sdk.init(
    dsn="https://83f8a0c480c3c0d7cf76ce8db73c4278@o4511974951550976.ingest.us.sentry.io/4511974976782336",
    integrations=[sentry_logging],
    send_default_pii=True,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)


def leerJson(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Archivo no encontrado en {path}")
        return []
    except json.JSONDecodeError:
        logging.error(f"Error al decodificar JSON en el archivo {path}")
        return []

def guardarJson(path, data):
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        logging.error(f"Error al guardar JSON en el archivo {path}: {e}")
        return False

#usuarios

def leerUsuarios():
    return leerJson("datos/users.json")

def agregarUsuario(nombre, rut, apellido, contrasena, tipoUsuario):
    usuariosActuales=leerUsuarios()
    nuevoId = usuariosActuales[-1]["id"] + 1
    nuevoUsuario = {"id": nuevoId, "rut":rut, "nombre":nombre, "apellido":apellido, "password":contrasena,"tipoUsuario":tipoUsuario}
    usuariosActuales.append(nuevoUsuario)
    if guardarJson("datos/users.json", usuariosActuales):
        logging.info(f"Usuario registrado exitosamente con el id: {nuevoId}")

#Herramientas

def leerHerramientas():
    return leerJson("datos/tools.json")

def mostrarHerramientas():
    data = leerHerramientas()
    if not data:
        logging.info("No hay herramientas registradas.")
        return
    
    print("Lista de herramientas registradas: \n")
    for i in data:
        print(f"Id herramienta: {i["id"]}" )
        print(f"Nombre herramienta: {i["nombre"]}")
        print(f"Tipo herramienta: {i["tipo"]}")
        print("---------------o---------------")

def agregarHerramienta(nombre, tipo):
        herramientasActuales=leerHerramientas()
        nuevoId = herramientasActuales[-1]["id"] + 1
        nuevaHerramienta = {"id": nuevoId, "nombre":nombre, "tipo":tipo}
        herramientasActuales.append(nuevaHerramienta)
        print(nuevoId)
        if guardarJson("datos/tools.json", herramientasActuales):
            logging.info(f"Herramienta {nombre} registrada exitosamente con el id: {nuevoId}")

def herramientasDisponibles(fechaConsulta):
    listaHerramientas = leerHerramientas()
    listaReservas = leerReservas()
    idReservados = []

    estadosOcupados = ["Solicitud Realizada", "Aprobada", "Entregado", "Atraso"]

    for i in listaReservas:
        if i["fecha"] == fechaConsulta and i["estadoSolicitud"] in estadosOcupados:
            idReservados.append(i["idHerramienta"])

    disponibles = []
    for j in listaHerramientas:
        if j["id"] not in idReservados:
            disponibles.append(j)

    if not disponibles:
        logging.warning(f"No existe disponibilidad de herramientas para la fecha: {fechaConsulta}")
        return None
    else:
        print("A continuacion se presentan las herramienta disponibles para prestamo en la fecha seleccionada: ")
        for herramienta in disponibles:
            print(f"Id herramienta: {herramienta["id"]}" )
            print(f"Nombre herramienta: {herramienta["nombre"]}")
            print(f"Tipo herramienta: {herramienta["tipo"]}")
            print("---------------o---------------")
    return disponibles

#Reservas

def leerReservas():
    return leerJson("datos/bookings.json")

def actualizarAtrasos():
    data= leerReservas()
    modificado = False
    hoy = datetime.now()
    valorMulta = 5000

    for i in data:
        if i["estadoSolicitud"] in ["Entregado", "Atraso"]:
            try:
                fechaLimite = datetime.strptime(i["fechaEntregaEsperada"], "%d-%m-%Y")
                if hoy > fechaLimite:
                    diasAtraso = (hoy - fechaLimite).days
                    if diasAtraso > 0:
                        i["estadoSolicitud"] = "Atraso"
                        i["penalizacion"] = diasAtraso * valorMulta
                        modificado = True
            except ValueError:
                continue
    if modificado:
        guardarJson("datos/bookings.json", data)
    return data

def mostrarReservas():
    data = actualizarAtrasos()
    for i in data:
        nombreHerramienta = busqueda(leerHerramientas(),"id",i["idHerramienta"])
        print(f"Id Reserva: {i["idReserva"]}" )
        print(f"Id Herramienta: {i["idHerramienta"]}" )
        print(f"Nombre herramienta: {nombreHerramienta["nombre"]}")
        print(f"Rut solicitante: {i["rutSolicitante"]}")
        print(f"Fecha reserva: {i["fecha"]}")
        print(f"Fecha entrega esperada: {i["fechaEntregaEsperada"]}" )
        print(f"Fecha devolucion real: {i["fechaDevolucionReal"]}")
        print(f"Estado solicitud: {i["estadoSolicitud"]}")
        print(f"Penalizacion: ${i.get("penalizacion", 0)}")
        print("---------------o---------------")


def revisarSolicitudes():
    data = actualizarAtrasos()
    for i in data:
        if i["estadoSolicitud"] == "Solicitud Realizada":
            nombreHerramienta = busqueda(leerHerramientas(),"id",i["idHerramienta"])
            print(f"Id Reserva: {i["idReserva"]}" )
            print(f"Id Herramienta: {i["idHerramienta"]}" )
            print(f"Nombre herramienta: {nombreHerramienta["nombre"]}")
            print(f"Rut solicitante: {i["rutSolicitante"]}")
            print(f"Fecha Solicitud: {i["fecha"]}")
            print("---------------o---------------")
  

def modificarSolicitudes(idSolicitud, modificacion, tipo):
    data = leerReservas()
    encontrado = False
    for i in data:
        if i["idReserva"] == idSolicitud:
            i[tipo] = modificacion ##se puede modificar fecha y estado
            encontrado = True
            break
    if encontrado:
        guardarJson("datos/bookings.json", data)
        logging.info(f"Reserva con ID {idSolicitud} modificada exitosamente")
    else:
        logging.warning(f"No se encontró la reserva con ID {idSolicitud} para modificar")



def mostrarReservasPersonales(rut):
    data = actualizarAtrasos()
    reservasUsuario=[]
    for i in data:
        if i["rutSolicitante"] == rut:
            reservasUsuario.append(i)
    if not reservasUsuario:
        logging.info(f"No hay reservas registradas para el usuario con RUT: {rut}")
        return
    
    for i in reservasUsuario:
        nombreHerramienta = busqueda(leerHerramientas(),"id",i["idHerramienta"])
        print(f"Id Reserva: {i["idReserva"]}" )
        print(f"Id Herramienta: {i["idHerramienta"]}" )
        print(f"Nombre herramienta: {nombreHerramienta["nombre"]}")
        print(f"Rut solicitante: {i["rutSolicitante"]}")
        print(f"Fecha reserva: {i["fecha"]}")
        print(f"Fecha entrega esperada: {i["fechaEntregaEsperada"]}" )
        print(f"Fecha devolucion real: {i["fechaDevolucionReal"]}")
        print(f"Estado solicitud: {i["estadoSolicitud"]}")
        print(f"Penalizacion: ${i.get("penalizacion", 0)}")
        print("---------------o---------------")



def registrarReserva(fechaReserva, fechaEntrega ,usuario, herramienta):
    reservasActuales = leerReservas()
    nuevoId = reservasActuales[-1]["idReserva"] + 1
    nuevaReserva = {"idReserva": nuevoId, "idHerramienta":herramienta,"rutSolicitante":usuario, "fecha":fechaReserva,"fechaEntregaEsperada":fechaEntrega,"fechaDevolucionReal": None , "estadoSolicitud":"Solicitud Realizada","penalizacion":0}
    reservasActuales.append(nuevaReserva)
    if guardarJson("datos/bookings.json", reservasActuales):
        logging.info(f"Reserva registrada exitosamente con el id: {nuevoId}")
    else:
        logging.error("Error al registrar la reserva")

def cambiarEstadoSolicitud(idSolicitud, estadoNuevo):
    data = leerReservas()
    encontrado = False
    for i in data:
        if str(i["idReserva"]) == str(idSolicitud):
            i["estadoSolicitud"] = estadoNuevo
            if estadoNuevo == "Devuelto":
                i["fechaDevolucionReal"] = datetime.now().strftime("%d-%m-%Y")
            encontrado = True
            break
    if encontrado:
        guardarJson("datos/bookings.json",data)
        logging.info(f"Reserva ID {idSolicitud} actualizada a estado {estadoNuevo}")
    else:
        logging.warning(f"No se encontro la reserva con ID {idSolicitud}")

#utilidades

def busqueda(valores, campo ,porEncontrar):
    for k in valores:
        if str(k[campo]) == str(porEncontrar):
            return k
    logging.warning("Lo siento, esa informacion no se encuentra en la base de datos")
    return None

def inicioSesion():
    data = leerUsuarios()
    rut = input("Por favor ingresa tu rut: ")
    password = input("Por favor ingresa tu password: ")
    dataUsuario = busqueda(data,"rut",rut)
    if dataUsuario and dataUsuario["password"] == password:
        logging.info("Inicio de sesión exitoso")
        return(dataUsuario)
    logging.warning(f"Intento de inicio de sesión fallido para RUT: {rut}")
    print("Credenciales incorrectas")
    return None


def bienvenida():
    print("-------------------------------------------------- \n")
    print("Bienvenido al Software de prestamo de equipos \n")
    print("-------------------------------------------------- \n")
            

    



def main():
    bienvenida()
    dataUsuario = inicioSesion()
    if not dataUsuario:
        logging.error("No se pudo iniciar sesión. Terminando el programa.")
        return
    while True:
        if dataUsuario["tipoUsuario"] == "encargado":
            print("+++++++++++++++++++++++++++++++++++++ \n")
            print("Bienvenido encargado " + dataUsuario["nombre"] + "\n")
            print("+++++++++++++++++++++++++++++++++++++ \n")
            print("¿Que te gustaria hacer?")
            print("\n 1.- Registrar usuarios \n 2.-Registrar equipo nuevo \n 3.-Consultar equipos \n 4.- Consultar prestamos \n 5.- Revisar Solicitudes \n 6.- Registrar entregas, devoluciones o cancelaciones \n 7.- Salir")
            seleccion = input("\n Ingrese una opción: ")

            if seleccion == "1":
                nombre = input("Nombre: ").strip()
                rut = input("RUT (sin puntos ni guión): ").strip()
                apellido = input("Apellido: ").strip()
                password = input("Password: ").strip()
                while True:
                    tipo = input("Tipo de usuario (encargado/solicitante): ").lower().strip()
                    if tipo in ["encargado", "solicitante"]:
                        tipoUsuario = tipo
                        break
                    logging.warning("Tipo no válido. Favor escriba encargado o solicitante")

                agregarUsuario(nombre, rut, apellido, password, tipoUsuario)
                input("\nPresiona Enter para continuar...")

            elif seleccion == "2":
                nombre = input("Nombre de la herramienta: ").strip()
                tipo = input("tipo de la herramienta: ").strip()

                agregarHerramienta(nombre, tipo)
                input("\nPresiona Enter para continuar...")


            elif seleccion == "3":
                mostrarHerramientas()
                input("\nPresiona Enter para continuar...")

            elif seleccion == "4":
                mostrarReservas()
                input("\nPresiona Enter para continuar...")


            elif seleccion == "5":
                revisarSolicitudes()
                input("\nPresiona Enter para continuar...")


            elif seleccion == "6": #Los estados pueden ser:  aprobado, rechazado, entregado (equipo entregado al usuario), devuelto (equipo fue devuelto) o cancelado
                idSolicitud = input("favor ingrese la ID de la reserva a modificar")
                print("Seleccione el nuevo estado:")
                print("\n 1.- Aprobado \n 2.- Rechazado \n 3.- Entregado (equipo entregado al usuario) \n 4.- Devuelto (equipo fue devuelto) \n 5.- Cancelado")
                opcionEstado = input("Opcion: ").strip()

                if opcionEstado == "1":
                    cambiarEstadoSolicitud(idSolicitud,"Aprobado")
                elif opcionEstado == "2":
                    cambiarEstadoSolicitud(idSolicitud,"Rechazado")
                elif opcionEstado == "3":
                    cambiarEstadoSolicitud(idSolicitud,"Entregado")
                elif opcionEstado == "4":
                    cambiarEstadoSolicitud(idSolicitud,"Devuelto")
                elif opcionEstado == "5":
                    cambiarEstadoSolicitud(idSolicitud,"Cancelado")
                else:
                    print("opcion no valida, reintente \n")
                input("\nPresiona Enter para continuar...")

            elif seleccion == "7":
                logging.info("Sesión finalizada por el usuario")
                break
        else:
            print("+++++++++++++++++++++++++++++++++++++ \n")
            print("Bienvenido " + dataUsuario["nombre"])
            print("+++++++++++++++++++++++++++++++++++++ \n")
            print("¿Que te gustaria hacer?")
            print("\n 1.- Ver mis reservas \n 2.- Realizar una reserva \n 3.- Salir")
            seleccion = input("\n Ingrese una opción: ")
            if seleccion == "1":
                print("mis reservas")
                mostrarReservasPersonales(dataUsuario["rut"])
                input("\nPresiona Enter para continuar...")

            elif seleccion == "2":
                fechaReserva = input("Para realizar una reserva ingresa la fecha (dd-mm-yy): ").strip()
                fechaEntrega = input("Ingrese la fecha de devolución(dd-mm-yy): ").strip()
                disponibles = herramientasDisponibles(fechaReserva)
                if disponibles  is not None:
                    idHerramienta = input("Indique el Id de la herramienta a reservar: ")
                    registrarReserva(fechaReserva,fechaEntrega,dataUsuario["rut"], idHerramienta)
            
                input("\nPresiona Enter para continuar...")
            elif seleccion == "3":
                logging.info("Sesión finalizada por el usuario")
                break


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        logging.critical(f"Error fatal no controlado: {e}")
    finally:
        sentry_sdk.flush(timeout=2.0)

