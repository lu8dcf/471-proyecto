from flask import Flask, jsonify, request
from markupsafe import escape

from flask_mysqldb import MySQL
from person import Person

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] ='admin'
app.config['MYSQL_DB'] = 'ejemplo'

mysql = MySQL(app)

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
    """ INSERT INTO """
    return jsonify({"name":name ,"surname":surname ,"dni":dni ,"email":email})

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

    """ update where"""
    return jsonify({"name":name ,"surname":surname ,"dni":dni ,"email":email})


# borrar un registro por id

@app.route('/persons/<int:id>',methods = ['DELETE'])
def remove_persons(id):
    """ delete bd"""
    return jsonify ({"messaje":"borrado"})

if __name__ =="__main__":   # solo se ejecute desde el archivo app.py y no s epueda importar y debe ser lo ultimo
    app.run(debug=True, port=5000)  # esta en modo desarrollo por debug