from flask import Flask, jsonify, request

app=Flask(__name__)

usuarios=[]

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
    usuarios.append(data)
    return jsonify(data)

@app.route("/usuario/list",methods=["GET"])
def obtener_usuarios():
    return jsonify(
        usuarios
    )

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

 