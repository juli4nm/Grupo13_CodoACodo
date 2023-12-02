

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

#--------------------------------------------------------------------
class Catalogo:
    #----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
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
            codigo INT NOT NULL,
            nombre VARCHAR (60) NOT NULL,
            Apellido VARCHAR (60) NOT NULL,
            dni INT NOT NULL,
            FeIng DATE NOT NULL,
            FeEgr DATE NOT NULL,
            Hus INT NOT NULL,
            email email
            Mensaje VARCHAR(255)
                                ''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
    #----------------------------------------------------------------
    def agregar_producto(self, codigo, nombre, Apellido, dni, FeIng, FeEgr, Hus, email, Mensaje):
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