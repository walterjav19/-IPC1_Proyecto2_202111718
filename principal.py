from datetime import datetime
from flask import Flask, jsonify, request

app=Flask(__name__)

usuarios=[]
libros=[]
prestamos=[]
id_usuarios=[]
id_libros=[]
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
    name= data.get('name')
    nickname=data.get('nickname')
    password=data.get('password')
    rol=data.get('rol')
    
    for i in range(len(usuarios)):
        if id==usuarios[i].get('id'):
            return jsonify({
                "msg": 'Error id de usuario Repetido',
                "status": 405
            })
        elif id=="" or name=="" or nickname=="" or password=="" or rol=="":
           return jsonify({
                "msg": 'Error campos minimos vacios',
                "status": 405                
            })                    
    usuarios.append(data)
    id_usuarios.append(id)
    print(usuarios)
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

@app.route("/books",methods=["POST"])
def crear_libros():
    data_libros= request.get_json()
    for i in range(len(libros)):        
         if data_libros[i]['book_available_copies']<0 or data_libros[i]['book_unavailable_copies']<0 or data_libros[i]['book_copies']<0 :
             return jsonify({
                 "msg": "numero de copias invalido",
                 "status": 406
             })
         elif data_libros[i]['book_author']=="" or  data_libros[i]['book_title']=="":   
             return jsonify({
                 "msg":'campos minimos vacios',
                 "status": 406
             })
         elif data_libros[i]['book_year']<0:
             return jsonify({
                 "msg":'año incorrecto',
                 "status": 406                 
             })     
         elif data_libros[i]['id_book']==libros[i].get('id_book'):
             return jsonify({
                 "msg": "id del libro repetido",
                 "status": 406
             })
         elif data_libros[i]['book_edition']<0:
             return jsonify({
                 "msg": "edicion no permitida",
                 "status": 406
             })
                                
    for libro in data_libros:
        libros.append(libro)
        id_libros.append(libro.get('id_book'))
    print(id_libros)    
    return jsonify({
        "msg": "Libros Creados Correctamente",
        "status": 204
    })
        
    

@app.route("/books/actualizar",methods=["PUT"])
def actualizar_libros():
    data=request.get_json()
    id= data.get('id_book')
    author=data.get('book_author')
    title=data.get('book_title')
    edition=data.get('book_edition')
    editorial=data.get('book_editorial')
    year=data.get('book_year')
    description=data.get('book_description')
    available=data.get('book_available_copies')
    unvailable=data.get('book_unavailable_copies')
    copies=data.get('book_copies')

    for i in range(len(libros)):
        if libros[i].get('id_book')== id:
            libros[i]['book_author']=author
            libros[i]['book_title']=title
            libros[i]['book_edition']=edition
            libros[i]['book_editorial']=editorial
            libros[i]['book_year']=year
            libros[i]['book_description']=description
            libros[i]['book_available_copies']=available
            libros[i]['book_unavailable_copies']=unvailable
            libros[i]['book_copies']=copies
            return jsonify({
                "msg": 'Libro actualizado',
                "status": 205
            }
            )

    return jsonify({
        "msg": 'Libro no encontrado',
        "status": 404
    })
    
@app.route("/books/<string:id>",methods=["DELETE"])
def eliminar_libros(id):
    for i in range(len(libros)):
        if libros[i].get('id_book')==id:
            libros.pop(i)
            return jsonify({
                "msg": 'Libro Eliminado',
                "status": 206
            }
            )
    return jsonify({
        "msg": 'Libro no encontrado',
        "status": 404
    })


@app.route("/books/buscar",methods=["GET"])
def obtener_libros():
    libros_mostrar=[]
    author=request.args.get('Autor')
    title=request.args.get('Titulo')


    for libro in libros:
        if libro.get('book_author')==author or libro.get('book_title')==title:
            libros_mostrar.append(libro)

    print(libros_mostrar)        
    if len(libros_mostrar)>0:
        return jsonify(libros_mostrar)
        
    return jsonify({
        "msg": "Error no existe el titulo o el autor",
        "status": 404
    })
retorno=False
@app.route("/borrow",methods=["POST"])
def crear_prestamos():
    data_prestamos = request.get_json()
    
    id_libro=data_prestamos.get('id_book')
    id_usuario=data_prestamos.get('id_user')
    if id_usuario not in id_usuarios:
            return jsonify({
            "msg": 'prestamo no realizado id del usuario inexistente',
            "status": 404
            })           

    if id_libro not in id_libros:
            return jsonify({
            "msg": 'prestamo no realizado id del libro inexistente',
            "status": 404
            })             
    global retorno
    id_prestamo= len(prestamos)
    
    date=str(datetime.today())
    for i in range (len(usuarios)):
        if usuarios[i].get('id')==id_usuario:
            if usuarios[i].get('available')==False:
                return jsonify({
                    'msg': 'Usuario no habilitado para prestamos',
                    'status':500
                })
            

    for i in range (len(libros)):
        if libros[i].get('id_book')==id_libro:
            if int(libros[i].get('book_available_copies'))==0:
                return jsonify({
                    'msg': 'Copias Disponibles 0 intente mas tarde',
                    'status':500                    
                }) 
            prestamos.append({'id_borrow':id_prestamo+1, 'Date': date,'Returned': retorno, 'Book': 
            {'id_borrow':libros[i]['book_author'],
             'book_title':libros[i]['book_title'],
             'book_edition':libros[i]['book_edition'],
             'book_editorial':libros[i]['book_editorial'],
             'book year':libros[i]['book_year'],
             'book_description':libros[i]['book_description'],
             'book_available_copies':int(libros[i]['book_available_copies'])-1,
             'book_unavailable_copies':int(libros[i]['book_unavailable_copies'])+1,
             'book_copies':libros[i]['book_copies']}})

    return jsonify({
        "msg": 'Prestamo realizado',
        "status": 201
    })

@app.route("/borrow/<string:id>",methods=["GET"])
def obtener_prestamos(id):

    for i in range(len(prestamos)):
        if int(prestamos[i].get('id_borrow'))==int(id):
            return jsonify({
                "id_borrow": prestamos[i]['id_borrow'],
                "Date": prestamos[i]['Date'],
                "Returned": prestamos[i]['Returned'],
                "Book": prestamos[i]['Book']
            })

    return jsonify({
        "msg": "Error no existe el id del Prestamo",
        "status": 404
    })

@app.route("/borrow/<string:idd>",methods=["PUT"])
def actualizar_prestamos(idd):
    for i in range(len(prestamos)):
        if int(prestamos[i].get('id_borrow'))!=int(idd):
            return jsonify({
            "msg": "id del prestamo no existe",
            "status": 409                
            })
        if prestamos[i].get('Returned')==True:
            return jsonify({
            "msg": "El libro ya fue devuelto",
            "status": 409                
            })            
        if int(prestamos[i].get('id_borrow'))==int(idd):
            prestamos[i]['Book']['book_available_copies']=int(prestamos[i]['Book']['book_available_copies'])+1
            prestamos[i]['Book']['book_unavailable_copies']=int(prestamos[i]['Book']['book_unavailable_copies'])-1
            prestamos[i]['Returned']=True
    print(int(prestamos[i]['Book']['book_available_copies'])+1)        
    return jsonify({
        "msg": "Libro devuelto correctamente",
        "status": 200
    })







if __name__=="__main__":
    app.run(port=3004,debug=True)