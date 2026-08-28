# Tarea 1
Sección del repositorio destinada para la tarea 1 de la asignatura pruebas de software (INF331)
* Nicolás Muñoz Ramírez Rol: 202104641-0
* Sergio Rojas Rol: 202273619-4
* Hans Toledo Rol: 201704591-4


## WIKI
Puede acceder a la Wiki mediante el siguiente [enlace](https://github.com/HanstoC/Entregas-pruebas-software/wiki)


## Requisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- [Python](https://www.python.org/)(última version)


## Instalación

Clona el repositorio:
```
git clone https://github.com/HanstoC/Entregas-pruebas-software.git
```
Luego visualizaras las carpetas correspondientes a cada una de las tareas, en este caso Tarea 1
```
cd Tarea 1

```
ejecuta el archivo llamado "booking.py"

```
py booking.py

```

## Dentro del programa

Dento del programa, se encuentran dos usuarios creados y dos herramientas de forma base (ambos con la id 0 y 1) para poder utilizar sus funciones dejamos a continuación sus credenciales

- Encargado:
  ```
  rut: 12345
  contraseña: asd123

  ```
- solicitante:
  ```
  rut: 678910
  contraseña: asd456

  ```
## Consideraciones:
- El usuario solo podrá solicitar una herramienta a la vez, si es que solicita alguna otra herramienta teniendo alguna solicitud activa está no se podrá realizar.
- El usuario puede cancelar su propia solicitud en cualquiero momento.
- Las reservas solo podrán ser de un solo día
- la opción consultar prestamos entrega la lista historica de prestamos que han ocurrido en el departamento
- la opcion revisar solicitudes, solo muestra solicitudes que tienen fecha superior o igual a la de hoy para poder gestionarlas.
- cada reserva puede tener 3 estados:
    - Activa: la reserva esta correctamente realizada y esta esperando a que se concrete el prestamo
    - Cancelada: La máquina no estaba disponible por lo que se cancela automaticamente
    - enEjecucion: La maquina reservada se encuentra prestada por lo que la reserva se encuentra en ejecución

## Dependencias utilizadas:

- json ( integrada en las librerias por defecto )
- datetime ( integrada en las librerias por defecto )

