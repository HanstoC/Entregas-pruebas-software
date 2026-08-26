import json

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

def agregarHerramienta(nombre, tipo):
        herramientasActuales=leerHerramientas()
        nuevoId = herramientasActuales[-1]["id"] + 1
        nuevaHerramienta = {"id": nuevoId, "nombre":nombre, "tipo":tipo}
        herramientasActuales.append(nuevaHerramienta)
        print(nuevoId)
        with open("datos/tools.json","w") as file:
            json.dump(herramientasActuales,file,indent=4,ensure_ascii=False)
        print("Herramienta registrada exitosamente con el id: " + str(nuevoId))


def registrarUso(id,fecha,usuario):
    with open("datos/bookings.json","w") as file:
        print("pianola")

def busqueda(valores, campo ,porEncontrar):
    for k in valores:
        if k[campo] == porEncontrar:
            return k
    print("Lo siento, usted no registra en la base de datos, reintentelo")
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
            if seleccion == "2":
                nombre = input("Nombre de la herramienta: ").strip()
                tipo = input("tipo de la herramienta: ").strip()
                agregarHerramienta(nombre, tipo)

            if seleccion == "3":
                print(leerHerramientas())


            if seleccion == "7":
                break
        else:
            print("Bienvenido " + dataUsuario["nombre"])

if __name__ == "__main__":
    main()