from flask import Flask, jsonify, request
from markupsafe import escape

from flask_mysqldb import MySQL
from person import Person
import jwt  # para las claves de usuario
import datetime

from functools import wraps 


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] ='admin'
app.config['MYSQL_DB'] = 'ejemplo'

app.config['SECRET_KEY'] = 'app_123'

mysql = MySQL(app)

#------------------------------------------LOGIN -------------------------------------
@app.route('/login', methods = ['POST'])
def login():
    auth = request.authorization
    print(auth)

    # control:  que se hallan cargado datos para autenticacion
    if not auth or not auth.username or not auth.password:
        return jsonify({"message":"Faltan Datos"},401)

    # Control: exite y coincide el usuario en la BD
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE username=%s and password=%s' , (auth.username,auth.password))
    row = cur.fetchone() # obtengo el id nombre y pass

    if not row:
        return jsonify({"message":"Noi autorizado"},401)
    
    # ese token es el que depues se solicitara
    token = jwt.encode({'id': row[0],
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, app.config['SECRET_KEY']  )    
    # consultar fecha para darle un tiempo de vida a la seccion antes que tenga que volver a loguearse
                        
                        
    

    # Hasta aca el usuario esta bien logueado
    return jsonify({"TOKEN":token, "username": auth.username})


# ----------------------------------------------------------------------------------------------------------------
#                                 VERIFICADOR DE TOKEN
# uso del WRAPS  

def token_requiered(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        print(kwargs)
        token= None
        # id = kwargs['id']
        # if id < 10:
        #     return jsonify({"messaje": "el id debe ser mayor a 10"})
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({ "message": "Falta el Token"}), 401
        
        try:
            data = jwt.decode(token , app.config['SECRET_KEY'], algorithms=['HS256'])
        except Exception as e:
            print(e)
            return jsonify({"message": str(e)}),401

        

        return func(*args, **kwargs)
    return decorated

@app.route('/test/<int:id>')
@token_requiered
def test(id):
    return jsonify({"messsage":"Test"})

# ------------------------------------------------------------------------------------------------------

@app.route('/')
def index():
    return 'index'

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/ping2')
def ping2():
    return jsonify({'messaje': 'pong'})

@app.route('/usuarios/<nombre>')
def usuarios(nombre):
    return jsonify({'name': nombre})

@app.route('/usuarios/<int:id>')
def usuarios_by_id(id):
    return jsonify({'id': id})

# @app.route('/<nombre>')
# def no_hacer(nombre):
#     return nombre

app.route('/<pach:nombre>')
def no_hacer(nombre):
    return escape(nombre)

# GET  todos los recursos
@app.route('/recurso', methods = ['GET'])
def get_recursos():
    return jsonify({'data': 'lista de todos los recursos'})

#POST nuevo 'recurso?
@app.route('/recurso', methods = ['POST'])
def post_recursos():
    return jsonify({'data': 'lista de todos los recursos'})

# colocaremos las conexiones con la BD
@app.route('/persons',methods = ['GET'])
def get_all_persons():
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM person')
    data = cur.fetchall()
    print(cur.rowcount)

    print(data)

    personlist=[]
    for row in data:
        objPerson = Person(row)
        personlist.append(objPerson.to_json())
    """ acceso a BD SELECT * FROM"""
    return jsonify(personlist)

@app.route('/persons', methods = ['POST'])
def create_persons():
    name = request.get_json()["name"]
    surname = request.get_json()["surname"]
    dni = request.get_json()["dni"]
    email = request.get_json()["email"]

    # consulta si esxite ese email

    # conexion con la BD
    cur = mysql.connection.cursor()


    cur.execute('SELECT * FROM person WHERE email = %s',(email,))
    # cur.execute('SELECT * FROM person WHERE dni = {0}'.format(dni))
    row = cur.fetchone()
    
    if row:
        return jsonify({"message": "email ya registrado"})


    """ INSERT INTO """
    # cursor
    cur = mysql.connection.cursor()
    
    # formateada con %s
    cur.execute('INSERT INTO person (name, surname,dni,email) VALUES (%s, %s, %s, %s)',(name, surname, dni, email))
    
    #aca graba en la BD
    mysql.connection.commit()

    """ OBTENER EL ID DEL REGISTRO CREADO """
    # no se mostraba el id porque era automatico
    cur.execute('SELECT LAST_INSERT_ID()')
    row = cur.fetchone()
    print(row[0])
    # guardo el id en una vrable entonce4s lo puede mostrar en la api con el id que le puso
    id = row[0]

    return jsonify({"name":name ,"surname":surname ,"dni":dni ,"email":email, "id": id})

# consultar una personal en particular
@app.route('/persons/<int:id>',methods =['GET'])
def get_person_by_id(id):
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM person WHERE id={0}'.format(id))
    data = cur.fetchall()
    print(cur.rowcount)

    print(data)
    objPerson= Person(data[0])
      
    return jsonify(objPerson.to_json())





# actualizar datos de una persona por i
@app.route('/persons/<int:id>',methods = ['PUT'])
def update_persons(id):
    name = request.get_json()["name"]
    surname = request.get_json()["surname"]
    dni = request.get_json()["dni"]
    email = request.get_json()["email"]

    """ update where modoficar los datos """
    cur = mysql.connection.cursor()
    cur.execute('UPDATE  person SET name = %s, surname = %s, dni = %s, email = %s WHERE id = %s',(name, surname, dni, email, id))

    # esta sentencia ejecuta en la BD
    mysql.connection.commit()

    return jsonify({"name":name ,"surname":surname ,"dni":dni ,"email":email})


# borrar un registro por id

@app.route('/persons/<int:id>',methods = ['DELETE'])
def remove_persons(id):
    
    """ delete bd"""
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM person WHERE id = {0}'.format(id))
    
    # esta sentencia ejecuta en la BD
    mysql.connection.commit()

    
    return jsonify ({"messaje":"borrado", "id":id})

if __name__ =="__main__":   # solo se ejecute desde el archivo app.py y no s epueda importar y debe ser lo ultimo
    app.run(debug=True, port=5000)  # esta en modo desarrollo por debug