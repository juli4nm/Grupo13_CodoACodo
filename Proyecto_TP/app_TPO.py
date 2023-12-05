
#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify
from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------


app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

#--------------------------------------------------------------------
class Catalogo:
    #----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, port, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            port= 3307,
            user=user,
            password=password,
            #database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Reserva (
            Codigo INT AUTO_INCREMENT primary key,
            Nombre VARCHAR (60) NOT NULL,
            Apellido VARCHAR (60) NOT NULL,
            dni INT NOT NULL,
            FeIng DATE NOT NULL,
            FeEgr DATE NOT NULL,
            Hus INT NOT NULL,
            Email  VARCHAR(60) NOT NULL,
            Mensaje VARCHAR(255))''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
    #----------------------------------------------------------------
    def agregar_reserva(self, Codigo, Nombre, Apellido, dni, FeIng, FeEgr, Hus, Email, Mensaje):
        # Verificamos si ya existe una Reserva con el mismo código
        self.cursor.execute(f"SELECT * FROM Reserva WHERE codigo = {Codigo}")
        Reserva_existe = self.cursor.fetchone()
        if Reserva_existe:
            return False

        sql = "INSERT INTO Reserva Codigo, Nombre, Apellido, dni, FeIng, FeEgr, Hus, Email, Mensaje) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)"
        valores = ({Codigo}, {Nombre}, {Apellido}, {dni}, {FeIng}, {FeEgr}, {Hus}, {Email}, {Mensaje}
        )

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return True
    #---------------------------------------------------------------
    #consultamos reserva
    def consultar_reserva(self, Codigo):
        self.cursor.execute(f"SELECT * FROM Reserva WHERE codigo = {Codigo}")
        return self.cursor.fetchone()
    
    #---------------------------------------------------------------
    def listar_reserva(self):
        self.cursor.execute("SELECT * FROM Reserva")
        catalogo = self.cursor.fetchall()
        return catalogo
    

 #----------------------------------------------------------------
    def eliminar_Reserva(self, Codigo):
        # Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM Reserva WHERE codigo = {Codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def modificar_reserva(self, Codigo, Nombre, Apellido, dni, FeIng, FeEgr, Hus, Email, Mensaje):
        sql = f"UPDATE Reserva SET codigo = {Codigo}, Nombre = '{Nombre}', Apellido = {Apellido}, dni = {dni}, FeIng = {FeIng}, FeEgr = {FeEgr}, Hus = {Hus}, Email = {Email}, Mensaje = {Mensaje}, WHERE codigo = {Codigo}"
    

        self.cursor.execute(sql)        
        self.conn.commit()
        return True








# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Catalogo

catalogo = Catalogo(host='localhost', port='3307', user='root', password='', database='app_tpo')
#catalogo = Catalogo(host='arielfsp.mysql.pythonanywhere-services.com', user='arielfsp', password='1234qw12', database='arielfsp$miapp')

#catalogo.agregar_reserva(123, "Miguel","Suarez", 25785123 , '2023-12-1', '2023-12-4', 1, 'MiguelSuarez@hotmial.com', 'desayuno incluido')
#catalogo.consultar_reserva(1)
# catalogo.agregar_producto(3, "Mouse tres botones",11, 3400, "mouse.jpg",1)
#catalogo.eliminar_Reserva (13)
#print (catalogo.consultar_reserva(123))





#--------------------------------------------------------------------
#--------------------------------------------------------------------
@app.route("/Reserva", methods=["POST"])
def agregar_reserva():
    #Recojo los datos del form
    Codigo = request.form['Codigo']
    Nombre = request.form['Nombre']
    Apellido = request.form['Apellido']
    dni = request.form['dni']
    FeIng = request.form['FeIng']
    FeEgr = request.form['FeEgr']
    Hus = request.form['Hus']
    Email = request.form['Email']
    Mensaje = request.form['Mensaje']  
    #imagen = request.files['imagen']
    # nombre_imagen = ""

    if catalogo.agregar_reserva(Codigo, Nombre, Apellido, dni, FeIng, FeEgr, Hus, Email, Mensaje):
        #imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
        return jsonify({"Mensaje": "Reserva realizada"}), 201
    else:
        return jsonify({"Mensaje": "Error reserva ya existente"}), 400



#--------------------------------------------------------------------
@app.route("/reserva", methods=["GET",])
def consultar_reserva():
    reserva = catalogo.consultar_reserva()
    return jsonify(catalogo)

#--------------------------------------------------------------------
@app.route("/reserva/<int:codigo>", methods=["GET"])
def listar_reserva(Codigo):
    reserva = catalogo.listar_reserva(Codigo)
    if reserva:
        return jsonify(catalogo), 201
    else:
        return "Reserva no encontrada", 404

#--------------------------------------------------------------------


@app.route("/Reserva/<int:codigo>", methods=["DELETE"])
def eliminar_reserva(Codigo):
    # Busco el producto guardado
    #producto = producto = catalogo.consultar_producto(codigo)
    # if producto: # Si existe el producto...
    #     imagen_vieja = producto["imagen_url"]
    #     # Armo la ruta a la imagen
    #     ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

    #     # Y si existe la borro.
    #     if os.path.exists(ruta_imagen):
    #         os.remove(ruta_imagen)

    # Luego, elimina el producto del catálogo
    if catalogo.eliminar_reserva(Codigo):
        return jsonify({"mensaje": "Reserva Cancelada"}), 200
    else:
        return jsonify({"mensaje": "Error al Cancelar la Reserva"}), 500
    


