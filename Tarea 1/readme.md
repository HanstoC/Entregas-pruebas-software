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
Para la correcta ejecución del programa es necesario instalar "sentry-sdk":

1. Crear el entorno virtual de python:
```bash
python3 -m venv venv
````
2. Activar el entorno:
```bash
source venv/bin/activate
````
3. Instalar librerías dentro del entorno:
```
pip install "sentry-sdk"
```
## Ejecución
Ejecutar el archivo llamado "booking.py"
```
python3 booking.py
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
- El usuario puede cancelar su propia solicitud en cualquier momento mientras no se haya concretado el préstamo.
- Cada reserva cuenta con una fecha de inicio, una fecha de entrega esperada definida al momento del préstamo y una fecha de devolucion real al finalizar.
- la opción consultar prestamos entrega la lista historica de prestamos que han ocurrido en el departamento
- la opcion revisar solicitudes, solo muestra solicitudes que tienen fecha superior o igual a la de hoy para poder gestionarlas.
- Si un préstamo en estado Entregado supera su fecha de entrega esperada, pasa automáticamente a estado Atraso generando una multa acumulativa por día vencido ($5.000 / día).
- cada reserva puede tener 7 estados:
  - Solicitud Realizada: Estado inicial cuando un usuario realiza la reserva. Se encuentra a la espera de ser revisada y gestionada por el Encargado.
  - Aprobado: La solicitud fue aceptada por el Encargado del departamento y queda lista para el retiro o entrega de la herramienta.
  - Entregado: La herramienta fue físicamente prestada al usuario y la reserva se encuentra actualmente en curso.
  - Atraso: Estado automático asignado por el sistema cuando la herramienta no ha sido devuelta y la fecha de entrega esperada ya venció. En este estado se calcula una penalización monetaria por cada día de retraso.
  - Devuelto: La herramienta fue restituida con éxito por el usuario. Registra la fechaDevolucionReal y finaliza la reserva.
  - Cancelado: La solicitud fue anulada por el propio usuario o cancelada por el encargado.
  - Rechazado: La solicitud fue denegada por el Encargado durante el proceso de revisión.

## Dependencias utilizadas:


- sentry (Necesario instalar)
- json ( integrada en las librerias por defecto )
- datetime ( integrada en las librerias por defecto )

