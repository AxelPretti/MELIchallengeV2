import time
import email
import config
import datetime
import mysql.connector 
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import dateutil.parser as parser

##Conexion de base de datos en MySql
CONNECTION_INSTANCE = mysql.connector.connect(
    host=config.MYSQL_HOST,
    user=config.MYSQL_DB_USER,
    passwd=config.MYSQL_DB_PWD)


def login_gmail():
    try:
        SCOPES = 'https://www.googleapis.com/auth/gmail.modify' 
        store = file.Storage('storage.json') 
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
        return GMAIL
    except Exception as e:
        print(e)
        print('*** ERROR AL ACCEDER A LA CUENTA DE GMAIL ***')


def create_database_ifnot_exists(conexionDB):
    try:
        cursor = conexionDB.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS ' + config.MYSQL_DB_NAME)
        conexionDB.commit()
        print('\nConexion exitosa a Base de datos')
        #creo la Tabla por si no existe
        create_table_ifnot_exists()
    except Exception as e:
        print(e)
        print('*** ERROR AL INTENTAR CREAR LA BASE DE DATOS ***')


def create_table_ifnot_exists():
    try:
        conexion = mysql.connector.connect(host=config.MYSQL_HOST,user=config.MYSQL_DB_USER,passwd=config.MYSQL_DB_PWD,database=config.MYSQL_DB_NAME)
        cursor = conexion.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS inbox (id_email INT AUTO_INCREMENT, date_email DATE, from_email TEXT, subject_email TEXT, PRIMARY KEY (id_email))')
        conexion.commit()
    except Exception as e:
        print(e)
        print('*** ERROR AL INTENTAR CREAR EL ESQUEMA DE LA BASE DE DATOS ***')
     

def write_database(dateW,fromW,subjectW):
    try:
        conexion = mysql.connector.connect(host=config.MYSQL_HOST,user=config.MYSQL_DB_USER,passwd=config.MYSQL_DB_PWD,database=config.MYSQL_DB_NAME)
        cursor = conexion.cursor()
        query_sql = 'insert into inbox (id_email,date_email,from_email,subject_email) values(NULL,%s,%s,%s)'
        val = (dateW,fromW,subjectW)
        cursor.execute(query_sql,val)
        conexion.commit()
        #print('\nEmail importado con exito en DB: ' + config.MYSQL_DB_NAME )
        close_mysql(cursor,conexion)
    except Exception as e:
        print(e)
        print("***ERROR GUARDAR DATOS BASE DE DATOS***")


def close_mysql(cursor,connection_mysql):
    cursor.close()
    connection_mysql.close()
    pass


def  read_emails_API():
    try:
        GMAIL = login_gmail()

        unread_msgs = GMAIL.users().messages().list(userId='me',labelIds=[config.LABEL_ID_ONE, config.LABEL_ID_TWO]).execute()

        if unread_msgs['resultSizeEstimate'] == 0:
            print('\n*AVISO* NO HAY EMAILS NO LEIDOS PARA PROCESAR')
            exit()

        mssg_list = unread_msgs['messages']

        #Recorro cada email
        for mssg in mssg_list:
            temp_dict = { }
            #guardo el ID del email para luego marcarlo como Leido.
            m_id = mssg['id'] 
            message = GMAIL.users().messages().get(userId=config.USER_ID, id=m_id).execute() # fetch the message using API
         
            payld = message['payload']  
            headr = payld['headers']
            body_ = message['snippet']
            #marco el mail como Leido
            mark_as_read(GMAIL,m_id)

            #Fracciono las distintas partes del mensaje y las guardo en variables
            for one in headr: # getting the Subject
                if one['name'] == 'Subject':
                    subject_ = one['value']
                else:
                    pass
            #Obtengo la fecha
            for two in headr: 
                if two['name'] == 'Date':
                    msg_date = two['value']
                    date_parse = (parser.parse(msg_date))
                    date_ = (date_parse.date())
                else:
                    pass
            #Obtengo el FROM
            for three in headr:
                if three['name'] == 'From':
                    msg_from = three['value']
                else:
                    pass
            #Condición para filtrar emails con la palabra DevOps en Subject o Body
            if ( "devops" in subject_.lower() ) or ( "devops" in body_.lower() ) :
                #spliteo el form_ para guardar el mail sin el nombre, lo hago acá para que solo se ejectute si se va a importar a la DB
                from_splited = msg_from.split("<")
                from_= from_splited[1]
                from_splited = from_.split(">")
                from_ = from_splited[0]

                print('\nEmail para importar en DB = DATE: ' + str(date_) + ' | FROM: ' + from_ + ' | SUBJECT: ' + subject_)
                write_database(date_,from_,subject_)
    except Exception as e:
        print(e)
        print('*** ERROR AL LEER EL EMAIL ***')


def mark_as_read(GMAIL,m_id):
    try:
        GMAIL.users().messages().modify(userId=config.USER_ID, id=m_id,body={ 'removeLabelIds': ['UNREAD']}).execute() 
    except Exception as e:
        print(e)
        print('\n*** ERROR AL INTENTAR MARCAR MAIL COMO LEID0 ***')


if __name__ == '__main__':
        #Primero reviso que la base de datos exista y adentro tambien creo la tabla
        create_database_ifnot_exists(CONNECTION_INSTANCE)
        CONNECTION_INSTANCE.close()
        print('\nLeyendo emails en la casilla de correo')
        read_emails_API()
