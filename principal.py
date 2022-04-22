from flask import Flask, jsonify, request

app=Flask(__name__)

usuarios=[]
libros=[]

@app.route('/')
def home():
    diccionario_envio={
        "msg": 'server funcionando',
        "status": 200
    }
    return jsonify(diccionario_envio)

@app.route("/usuario",methods=["POST"])
def crear_usuarios():
    data = request.get_json()
    id = data.get('id')
    for i in range(len(usuarios)):
        if id==usuarios[i].get('id'):
            return jsonify({
                "msg": 'Error id de usuario Repetido',
                "status": 405
            })
    usuarios.append(data)
    return jsonify({
        "msg": 'Usuario creado',
        "status": 201
    })
    

@app.route("/usuario/<string:id>",methods=["GET"])
def obtener_usuarios(id):
    for i in range(len(usuarios)):
        if usuarios[i].get('id')==id:
            return jsonify({
                "id_user": usuarios[i]['id'],
                "user_name": usuarios[i]['name'],
                "user_nickname": usuarios[i]['nickname'],
                "user_password": usuarios[i]['password'],
                "user_rol": usuarios[i]['rol'],
                "available": usuarios[i]['available'],
            })
    return jsonify({
        "msg": "Error no existe el Id",
        "status": 404
    })

@app.route("/usuario/actualizar",methods=["PUT"])
def actualizar_usuarios():
    data=request.get_json()
    id= data.get('id')
    name=data.get('name')
    nickname=data.get('nickname')
    password=data.get('password')
    rol=data.get('rol')
    available=data.get('available')

    for i in range(len(usuarios)):
        if usuarios[i].get('id')== id:
            usuarios[i]['name']=name
            usuarios[i]['nickname']=nickname
            usuarios[i]['password']=password
            usuarios[i]['rol']=rol
            usuarios[i]['available']=available

            return jsonify({
                "msg": 'Usuario actualizado',
                "status": 202
            }
            )

    return jsonify({
        "msg": 'Usuario no encontrado',
        "status": 404
    })


@app.route("/usuario/<string:id>",methods=["DELETE"])
def eliminar_usuarios(id):
    for i in range(len(usuarios)):
        if usuarios[i].get('id')== id:
            usuarios.pop(i)
            return jsonify({
                "msg": 'Usuario eliminado',
                "status": 203
            }
            )

    return jsonify({
        "msg": 'Usuario no encontrado',
        "status": 404
    })



if __name__=="__main__":
    app.run(port=3004,debug=True)

 