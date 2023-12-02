
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
            password=password
        )
        self.cursor = self.conn.cursor()

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
            codigo INT AUTO_INCREMENT primary key,
            nombre VARCHAR (60) NOT NULL,
            Apellido VARCHAR (60) NOT NULL,
            dni INT NOT NULL,
            FeIng DATETIME NOT NULL,
            FeEgr DATETIME NOT NULL,
            Hus INT NOT NULL,
            email  VARCHAR(60) NOT NULL,
            mensaje VARCHAR(255))''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
    #----------------------------------------------------------------
    def agregar_reserva(self, codigo, nombre, Apellido, dni, FeIng, FeEgr, Hus, email, Mensaje):
        # Verificamos si ya existe una Reserva con el mismo código
        self.cursor.execute(f"SELECT * FROM Reserva WHERE codigo = {codigo}")
        Reserva_existe = self.cursor.fetchone()
        if Reserva_existe:
            return False

        sql = "INSERT INTO Reserva (codigo, nombre, Apellido, dni, FeIng, FeEgr, Hus, email, Mensaje) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)"
        valores = (codigo, nombre, Apellido, dni, FeIng, FeEgr, Hus, email, Mensaje
        )

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return True
    #---------------------------------------------------------------
    #consultamos reserva
    def consultar_reserva(self, codigo):
        self.cursor.execute(f"SELECT * FROM catalogo WHERE codigo = {codigo}")
        return self.cursor.fetchone()
    
    #---------------------------------------------------------------
    def listar_reserva(self):
        self.cursor.execute("SELECT * FROM catalogo")
        catalogo = self.cursor.fetchall()
        return catalogo


# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Catalogo

catalogo = Catalogo(host='localhost', port='3307', user='root', password='', database='app_TPO')
#catalogo = Catalogo(host='arielfsp.mysql.pythonanywhere-services.com', user='arielfsp', password='1234qw12', database='arielfsp$miapp')

catalogo.agregar_reserva(1, "Juan","Gomez", 11345123 , '12/3/2023', '19/3/2023', 4, 'juangomez@hotmial.com', 'desayuno incluido')
# catalogo.agregar_producto(2, "Notebook",11, 740000, "compu.jpg",1)
# catalogo.agregar_producto(3, "Mouse tres botones",11, 3400, "mouse.jpg",1)


#--------------------------------------------------------------------
@app.route("/Reserva", methods=["POST"])
def agregar_reserva():
    #Recojo los datos del form
    codigo = request.form['codigo']
    nombre = request.form['nombre']
    Apellido = request.form['Apellido']
    dni = request.form['dni']
    FeIng = request.form['FeIng']
    FeEgr = request.form['FeEgr']
    Hus = request.form['Hus']
    email = request.form['email']
    Mensaje = request.form['Mensaje']  
    #imagen = request.files['imagen']
    # nombre_imagen = ""

    if catalogo.agregar_reserva(codigo, nombre, Apellido, dni, FeIng, FeEgr, Hus, email, Mensaje):
        #imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
        return jsonify({"mensaje": "Reserva realizada"}), 201
    else:
        return jsonify({"mensaje": "Reserva ya realidaza"}), 400

#--------------------------------------------------------------------
#--------------------------------------------------------------------
@app.route("/Reserva/<int:codigo>", methods=["DELETE"])
def eliminar_reserva(codigo):
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
    if catalogo.eliminar_reserva(codigo):
        return jsonify({"mensaje": "Reserva Cancelada"}), 200
    else:
        return jsonify({"mensaje": "Error al Cancelar la Reserva"}), 500
    


