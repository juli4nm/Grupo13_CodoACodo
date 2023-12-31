
#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify
from flask import request, render_template

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#------------------------------------------P--------------------------


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
            database=database
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
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reserva (
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
        self.cursor.execute(f"SELECT * FROM reserva WHERE Codigo = {Codigo}")
        Reserva_existe = self.cursor.fetchone()
        if Reserva_existe:
            return False

        sql = "INSERT INTO reserva (Codigo, Nombre, Apellido, dni, FeIng, FeEgr, Hus, Email, Mensaje) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)"
        valores = (Codigo, Nombre, Apellido, dni, FeIng, FeEgr, Hus, Email, Mensaje)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return True
    #---------------------------------------------------------------
    #consultamos reserva
    def consultar_reserva(self, Codigo):
        self.cursor.execute(f"SELECT * FROM reserva WHERE Codigo = {Codigo}")
        return self.cursor.fetchone()
    
    #---------------------------------------------------------------
    def listar_reserva(self):
        self.cursor.execute("SELECT * FROM reserva")
        reserva = self.cursor.fetchall()
        return reserva
    

#----------------------------------------------------------------
    def eliminar_Reserva(self, Codigo):
        # Eliminamos un producto de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM reserva WHERE Codigo = {Codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

#----------------------------------------------------------------


    def modificar_reserva(self, Codigo, nueva_Nombre, nueva_Apellido, nueva_dni, nueva_FeIng, nueva_FeEgr, nueva_Hus, nueva_Email, nueva_Mensaje):
        sql = "UPDATE reserva SET Nombre = %s, Apellido = %s, dni = %s, FeIng = %s, FeEgr = %s, Hus = %s, Email = %s, Mensaje = %s  WHERE Codigo = %s"
        valores = (nueva_Nombre, nueva_Apellido, nueva_dni, nueva_FeIng, nueva_FeEgr, nueva_Hus, nueva_Email, nueva_Mensaje, Codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

#----------------------------------------------------------------
    def mostrar_reserva(self, Codigo):
        # Mostramos los datos de un producto a partir de su código
        reserva = self.consultar_reserva(Codigo)
        if reserva:
            print("-" * 40)
            print(f"Codigo.....: {reserva['Codigo']}")
            print(f"Nombre.....: {reserva['Nombre']}")
            print(f"Apellido...: {reserva['Apellido']}")
            print(f"dni.....: {reserva['dni']}")
            print(f"FeIng.....: {reserva['FeIng']}")
            print(f"FeEgr.....: {reserva['FeEgr']}")
            print(f"Hus..: {reserva['Hus']}")
            print(f"Email..: {reserva['Email']}")
            print(f"Mensaje..: {reserva['Mensaje']}")
            print("-" * 40)
        else:
            print("Reserva no encontrada.")



# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Catalogo

catalogo = Catalogo(host='localhost', port='3307', user='root', password='', database='app_tpo')
#catalogo = Catalogo(host='arielfsp.mysql.pythonanywhere-services.com', user='arielfsp', password='1234qw12', database='arielfsp$miapp')

#catalogo.agregar_reserva(116, "Julio","Torres", 11785125 , '2023-02-10', '2023-02-21', 9, 'torres_julio@hotmial.com', 'desayuno incluido')
#catalogo.consultar_reserva(123)
# catalogo.agregar_producto(3, "Mouse tres botones",11, 3400, "mouse.jpg",1)
#catalogo.eliminar_Reserva (123)
#catalogo.modificar_reserva (118, "Julia","Torres", 9785125 , '2023-07-10', '2023-07-21', 2, 'torresjulia@hotmial.com', 'primer piso')
#print (catalogo.consultar_reserva(123))

catalogo.modificar_reserva (120, "Tomas","Aguiler", 35001025 , '2023-12-01', '2023-12-5', 2, 'aquinotomas00@hotmial.com', 'desayuno')



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

    # Me aseguro que el producto exista
    catalogo.consultar_producto(Codigo)

    if catalogo.agregar_reserva(Codigo, Nombre, Apellido, dni, FeIng, FeEgr, Hus, Email, Mensaje):
        #imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
        return jsonify({"Mensaje": "Reserva realizada"}), 201
    else:
        return jsonify({"Mensaje": "Error reserva ya existente"}), 400



#--------------------------------------------------------------------
@app.route("/DetalleReserva", methods=["GET",])
def listar_reserva():
    DetalleReserva = Catalogo.listar_reserva()
    return jsonify(reserva)

#--------------------------------------------------------------------
@app.route("/Reserva/<int:Codigo>", methods=["GET"])
def mosrtar_reserva(Codigo):
    reserva = Catalogo.consultar_reserva(Codigo)
    if reserva:

        return jsonify(reserva), 201

        return "Reserva no encontrada", 404
    

#--------------------------------------------------------------------
@app.route("/Reserva/<int:codigo>", methods=["PUT"])
def modificar_reserva(codigo):
    #Recojo los datos del form
    nueva_Nombre = request.form.get("Nombre")
    nueva_Apellido = request.form.get("Apellido")
    nuevo_dni = request.form.get("dni")
    nuevo_FeIng = request.form.get("FeIng")
    nuevo_FeEgr = request.form.get("FeEgr")
    nuevo_Hus = request.form.get("Huspedes")
    nuevo_Email = request.form.get("Email")
    nuevo_Mensaje = request.form.get("Mensaje")
    #imagen = request.files['imagen']
    #nombre_imagen = ""


    # Procesamiento de la imagen
    # nombre_imagen = secure_filename(imagen.filename)
    # nombre_base, extension = os.path.splitext(nombre_imagen)
    # nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    # imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

    # Busco el producto guardado
    reserva = catalogo.consultar_producto(codigo)
    # if producto: # Si existe el producto...
    #     imagen_vieja = producto["imagen_url"]
    #     # Armo la ruta a la imagen
    #     ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

    #     # Y si existe la borro.
    #     if os.path.exists(ruta_imagen):
    #         os.remove(ruta_imagen)
    
    if catalogo.modificar_reserva(codigo, nueva_Nombre, nueva_Apellido, nueva_dni, nueva_FeIng, nueva_FeEgr, nueva_Hus, nueva_Email, nueva_Mensaje):
        return jsonify({"mensaje": "Reserva modificada"}), 200
    else:
        return jsonify({"mensaje": "Reserva no encontrada"}), 403


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
    
#--------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)