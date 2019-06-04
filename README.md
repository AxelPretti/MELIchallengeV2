# CHALLENGE MERCADO LIBRE

El challenge es armar un programa en Python que pueda acceder a una cuenta de Gmail, leer e identificar los emails que tengan la
palabra "DevOps" en el asunto o el cuerpo del email.
De estos correos se debe guardar en una base de datos MySQL los siguientes campos: fecha, from, subject.
La base de datos también debe ser creada.

-La base de datos que crea por defecto es "mailbox_devops" con una tabla "inbox"

-Modificar usaurio y password para realizar la conexion al MySQL en el archivo confg.py

-El script lee  los emails de la bandeja Inbox que están marcados como NO LEIDOS, si es necesario volver a importar un email en la base de datos hay que marcarlo como NO LEIDO antes.



# IMPORTANTE ANTES DE EJECUTAR 
El Script está desarrollado en Python3 y utiliza (QuickStart)  API de Google

Por lo tanto requiere los siguientes requisitos:

Tener instalado Python3, pip3 , google-api-python-client y mysql-connector. Tambien MySQL ya que graba en una Base de Datos.

ejemplo de instalacion de requerimientos en Ubuntu:

$ sudo apt install python3 python3-pip mysql-connector
$ sudo apt install mysql
$ pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib



# Archivo config.py
En este archivo se encuentra la configuración y es el seteo de variales que utiliza search_emails_wordV2.py para funcionar.

<b> <i>------ Variables para la conexion con MySQL ------</i> </b>

<b>MYSQL_HOST</b> = si el motor Mysql corre en el mismo equipo dejar por defecto localhost

<b>MYSQL_DB_USER</b> : Indicar un usuario con permisos para crear Bases de datos

<b>MYSQL_DB_PWD</b> : credenciales del usuario Mysql

MYSQL_DB_NAME : Nombre de base de datos

MYSQL_PORT: puerto para conectarse al Mysql



