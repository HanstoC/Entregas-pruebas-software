import json
from datetime import datetime

def leerUsuarios():
    with open("datos/users.json", "r") as file:
        data = json.load(file)
    return data

def agregarUsuario(nombre, rut, apellido, contrasena, tipoUsuario):
    usuariosActuales=leerUsuarios()
    nuevoId = usuariosActuales[-1]["id"] + 1
    nuevoUsuario = {"id": nuevoId, "rut":rut, "nombre":nombre, "apellido":apellido, "password":contrasena,"tipoUsuario":tipoUsuario}
    usuariosActuales.append(nuevoUsuario)
    with open("datos/users.json","w") as file:
        json.dump(usuariosActuales,file,indent=4,ensure_ascii=False)
    print("Usuario registrado exitosamente con el id: " + str(nuevoId))

def leerHerramientas():
    with open("datos/tools.json", "r") as file:
        data = json.load(file)
    return data


def mostrarHerramientas():
    with open("datos/tools.json", "r") as file:
        data = json.load(file)
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
        with open("datos/tools.json","w") as file:
            json.dump(herramientasActuales,file,indent=4,ensure_ascii=False)
        print("Herramienta registrada exitosamente con el id: " + str(nuevoId))

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

    print("A continuacion se presentan las herramienta disponibles para prestamo en la fecha seleccionada: ")
    if not disponibles:
        print("No existe disponibilidad de herramientas para la fecha seleccionada")
        return None
    else:
        for herramienta in disponibles:
            print(f"Id herramienta: {herramienta["id"]}" )
            print(f"Nombre herramienta: {herramienta["nombre"]}")
            print(f"Tipo herramienta: {herramienta["tipo"]}")
            print("---------------o---------------")
    return disponibles


def leerReservas():
    with open("datos/bookings.json","r") as file:
        data = json.load(file)
    return data

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
        if datetime.strptime(i["fecha"],"%d-%m-%Y") >= hoy:
            nombreHerramienta = busqueda(leerHerramientas(),"id",i["idHerramienta"])
            print(f"Id Reserva: {i["idReserva"]}" )
            print(f"Id Herramienta: {i["idHerramienta"]}" )
            print(f"Nombre herramienta: {nombreHerramienta["nombre"]}")
            print(f"Fecha Solicitud: {i["fecha"]}")
            print("---------------o---------------")
        else:
            continue

def modificarSolicitudes(idSolicitud, modificacion, tipo):
    data = leerReservas()
    for i in data:
        if i["idReserva"] == idSolicitud:
            i[tipo] = modificacion ##se puede modificar fecha y estado
    



def mostrarReservasPersonales(rut):
    data = leerReservas()
    for i in data:
        if i["rutSolicitante"] == rut:
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
    with open("datos/bookings.json","w") as file:
        json.dump(reservasActuales,file,indent=4,ensure_ascii=False)
    print("Reserva registrada exitosamente con el id: " + str(nuevoId))



def busqueda(valores, campo ,porEncontrar):
    for k in valores:
        if k[campo] == porEncontrar:
            return k
    print("Lo siento, esa informacion no se encuentra en la base de datos, reintentelo")
    return None

def inicioSesion():
    data = leerUsuarios()
    rut = input("Por favor ingresa tu rut: ")
    password = input("Por favor ingresa tu password: ")
    dataUsuario = busqueda(data,"rut",rut)
    if dataUsuario["password"] == password:
        print("Password correcto")
        return(dataUsuario)
    print("Password incorrecto")


def bienvenida():
    print("-------------------------------------------------- \n")
    print("Bienvenido al Software de prestamo de equipos \n")
    print("-------------------------------------------------- \n")
            

    



def main():
    bienvenida()
    dataUsuario = inicioSesion()
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
                    print("Tipo no válido. Favor escriba encargado o solicitante")

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
                fechaReserva = input("Para realizar una reserva ingresa la fecha (dd-mm-yy): ")
                estado = herramientasDisponibles(fechaReserva)
                if estado  is not None:
                    idHerramienta = input("Indique el Id de la herramienta a reservar: ")
                    registrarReserva(fechaReserva,dataUsuario["rut"], idHerramienta)
            
                input("\nPresiona Enter para continuar...")
            elif seleccion == "3":
                break


if __name__ == "__main__":
    main()