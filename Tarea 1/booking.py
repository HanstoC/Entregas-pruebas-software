import json
from datetime import datetime
import logging
import sentry_sdk

sentry_sdk.init(
    dsn="https://83f8a0c480c3c0d7cf76ce8db73c4278@o4511974951550976.ingest.us.sentry.io/4511974976782336",
    send_default_pii=True,
    enable_logs=True,
    traces_sample_rate=1.0,
    profile_session_sample_rate=1.0,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

sentry_sdk.profiler.start_profiler()

division_by_zero = 1 / 0

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
        logging.info("Usuario registrado exitosamente con el id: " + str(nuevoId))

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

    for i in listaReservas:
        if i["fecha"] == fechaConsulta:
            if i["estadoSolicitud"]=="Activa":
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

def mostrarReservas():
    data = leerReservas()
    for i in data:
        nombreHerramienta = busqueda(leerHerramientas(),"id",i["idHerramienta"])
        print(f"Id Reserva: {i["idReserva"]}" )
        print(f"Id Herramienta: {i["idHerramienta"]}" )
        print(f"Nombre herramienta: {nombreHerramienta["nombre"]}")
        print(f"Fecha Solicitud: {i["fecha"]}")
        print(f"Estado solicitud: {i["estadoSolicitud"]}")
        print("---------------o---------------")


def revisarSolicitudes():
    data = leerReservas()
    hoy = datetime.now()
    for i in data:
        try:
            fechaReserva = datetime.strptime(i["fecha"], "%d-%m-%Y")
            if fechaReserva >= hoy:
                nombreHerramienta = busqueda(leerHerramientas(),"id",i["idHerramienta"])
                print(f"Id Reserva: {i["idReserva"]}" )
                print(f"Id Herramienta: {i["idHerramienta"]}" )
                print(f"Nombre herramienta: {nombreHerramienta["nombre"]}")
                print(f"Fecha Solicitud: {i["fecha"]}")
                print("---------------o---------------")
        except ValueError:
            logging.error(f"Formato de fecha inválido para la reserva con ID: {i['idReserva']}")
            continue

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
    data = leerReservas()
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
        print(f"Fecha Solicitud: {i["fecha"]}")
        print("---------------o---------------")



def registrarReserva(fecha,usuario, herramienta):
    reservasActuales = leerReservas()
    nuevoId = reservasActuales[-1]["idReserva"] + 1
    nuevaReserva = {"idReserva": nuevoId, "idHerramienta":herramienta, "fecha":fecha, "rutSolicitante":usuario, "estadoSolicitud":"Activa"}
    reservasActuales.append(nuevaReserva)
    if guardarJson("datos/bookings.json", reservasActuales):
        logging.info(f"Reserva registrada exitosamente con el id: {nuevoId}")
    else:
        logging.error("Error al registrar la reserva")


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


            elif seleccion == "6": #Los estados pueden ser: activa, cancelada, enEjecucion. 
                idSolicitud = input("favor ingrese la ID de la reserva a modificar")
                parametro = input("¿qué parámetro te gustaria modificar? (fecha o estado)").lower().strip()
                if parametro == "fecha":
                    ##verificar que la fecha sea mayor o igual ala de hoy
                    fecha = input("Ingrese la nueva fecha (dd-mm-yy): ")
                    while fecha < datetime.now():
                        print("favor ingrese una fecha válida ")
                        fecha = input("Ingrese la nueva fecha (dd-mm-yy): ")
                    
                    modificarSolicitudes(idSolicitud,fecha,"fecha")

                if parametro == "estado":
                    estado = input("Seleccione un número para el estado de la solicitud: \n 1.- Activa \n 2,- Cancelada \n 3.-en Ejecucion")
                    if estado == "1":
                        modificarSolicitudes(idSolicitud,"Activa","estadoSolicitud")
                    elif estado == "2":
                        modificarSolicitudes(idSolicitud,"Cancelada","estadoSolicitud")
                    elif estado == "3":
                        modificarSolicitudes(idSolicitud,"enEjecucion","estadoSolicitud")

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
                disponibles = herramientasDisponibles(fechaReserva)
                if disponibles  is not None:
                    idHerramienta = input("Indique el Id de la herramienta a reservar: ")
                    registrarReserva(fechaReserva,dataUsuario["rut"], idHerramienta)
            
                input("\nPresiona Enter para continuar...")
            elif seleccion == "3":
                logging.info("Sesión finalizada por el usuario")
                break


if __name__ == "__main__":
    main()

sentry_sdk.profiler.stop_profiler()