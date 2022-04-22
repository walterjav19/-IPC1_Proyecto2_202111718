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


if __name__=="__main__":
    app.run(port=3004,debug=True)

 