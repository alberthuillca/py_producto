from flask import Flask, request, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['MYSQL_HOST'] = 'birvxmqrxnbzpdvm0ogz-mysql.services.clever-cloud.com'
    app.config['MYSQL_USER'] = 'uysv9t18xsovpgmn'
    app.config['MYSQL_PASSWORD'] = 'lqXoWZythDxqtkIJbcOp'
    app.config['MYSQL_DB'] = 'birvxmqrxnbzpdvm0ogz'
else:
    app.debug = False


mysql = MySQL(app)

@app.route('/', methods=['GET'])
def listar_productos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto')
    data = cur.fetchall()
    allData = []
    print(data)
    for i in range(len(data)):
            idp = data[i][0]
            name = data[i][1]
            precio = data[i][2]
            cantidad = data[i][3]
            idc = data[i][4]
            dataDict = {
                "idproducto": idp,
                "nom_producto": name,
                "precio": precio,
                "cantidad": cantidad,
                "idcategoria": idc
            }
            allData.append(dataDict)

    return jsonify(allData)


@app.route('/categoria', methods=['GET'])
def listar_categoria():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM categoria')
    data = cur.fetchall()
    Data = []
    print(data)
    for i in range(len(data)):
            idc = data[i][0]
            name = data[i][1]
            datades = {
                "idcategoria": idc,
                "nom_categoria": name,
            }
            Data.append(datades)

    return jsonify(Data)

@app.route('/categoria/<id>', methods=['GET'])
def listar_categoria_id(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto WHERE idcategoria = %s', (id,))
    data = cur.fetchall()
    alData = []
    print(data)
    for i in range(len(data)):
            idp = data[i][0]
            name = data[i][1]
            precio = data[i][2]
            cantidad = data[i][3]
            idc = data[i][4]
            datadesc = {
                "idproducto": idp,
                "nom_producto": name,
                "precio": precio,
                "cantidad": cantidad,
                "idcategoria": idc
            }
            alData.append(datadesc)

    return jsonify(alData)


@app.route('/<id>', methods=['GET'])
def listar_producto_id(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto WHERE idproducto = %s', (id,))
    data = cur.fetchall()
    allData = []
    print(data)
    for i in range(len(data)):
            idp = data[i][0]
            name = data[i][1]
            precio = data[i][2]
            cantidad = data[i][3]
            idc = data[i][4]
            dataDict = {
                "idproducto": idp,
                "nom_producto": name,
                "precio": precio,
                "cantidad": cantidad,
                "idcategoria": idc
            }
            allData.append(dataDict)

    return jsonify(allData)

@app.route('/add', methods=['POST'])
def registrar_producto():
    body = request.json
    nom_producto = body['nom_producto']
    precio = body['precio']
    cantidad = body['cantidad']
    idcategoria = body['idcategoria']

    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO producto VALUES(null, %s, %s, %s, %s)', (nom_producto, precio, cantidad, idcategoria,))
    mysql.connection.commit()
    cur.close()
    return jsonify({
        'status': 'Data is posted to MySQL!',
        'nom_producto': nom_producto,
        'precio': precio,
        'cantidad': cantidad,
        'idcategoria': idcategoria
    })

@app.route('/<id>', methods=['PUT'])
def modificar_producto(id):
    body = request.json
    name = body['nom_producto']
    precio = body['precio']
    cantidad = body['cantidad']
    idc = body['idcategoria']
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE producto SET nom_producto = %s, precio = %s, cantidad = %s, idcategoria = %s WHERE idproducto = %s', (name, precio, cantidad, idc, id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'status': 'Data '+ id +' is updated on MySQL!'})

@app.route('/<id>', methods=['DELETE'])
def eliminar_producto(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM producto WHERE idproducto = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'status': 'Data '+ id +' is deleted on MySQL!'})


if __name__ == '__main__':
    app.debug = True
    app.run()