from flask import Flask ,jsonify ,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend
# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/tp_crud'
# desde el objeto app configuro la URI de la BBDD    user:clave@localhost/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db= SQLAlchemy(app)
ma=Marshmallow(app)

# defino la tabla
class Oferta_educativa(db.Model):   # la clase Oferta_educativa hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    carrera=db.Column(db.String(100))
    duracion=db.Column(db.String(100))
    tecnologias=db.Column(db.String(400))
    def __init__(self,carrera,duracion,tecnologias):   #crea el  constructor de la clase
        self.carrera=carrera   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.duracion=duracion
        self.tecnologias=tecnologias
with app.app_context():
    db.create_all()  # crea las tablas
#  ************************************************************
 
class Oferta_educativa_schema(ma.Schema):
    class Meta:
        fields=('id','carrera','duracion','tecnologias')
oferta_educativa_schema=Oferta_educativa_schema()            # para crear una oferta_educativa
ofertas_educativas_schema=Oferta_educativa_schema(many=True)  # multiples registros

# crea los endpoint o rutas (json)
@app.route('/ofertas',methods=['GET'])
def get_Ofertas():
    all_ofertas=Oferta_educativa.query.all()     # query.all() lo hereda de db.Model
    result=ofertas_educativas_schema.dump(all_ofertas)  # .dump() lo hereda de ma.schema
    return jsonify(result)
 
@app.route('/ofertas/<id>',methods=['GET'])
def get_oferta(id):
    oferta=Oferta_educativa.query.get(id)
    return oferta_educativa_schema.jsonify(oferta)
 


@app.route('/ofertas/<id>',methods=['DELETE'])
def delete_oferta(id):
    oferta=Oferta_educativa.query.get(id)
    db.session.delete(oferta)
    db.session.commit()
    return oferta_educativa_schema.jsonify(oferta)

@app.route('/ofertas', methods=['POST']) # crea ruta o endpoint
def create_oferta():
    print(request.json)  # request.json contiene el json que envio el cliente
    carrera=request.json['carrera']
    duracion=request.json['duracion']
    tecnologias=request.json['tecnologias']
    new_oferta=Oferta_educativa(carrera,duracion,tecnologias)
    db.session.add(new_oferta)
    db.session.commit()
    return oferta_educativa_schema.jsonify(new_oferta)

@app.route('/ofertas/<id>' ,methods=['PUT'])
def update_oferta(id):
    oferta=Oferta_educativa.query.get(id)
   
    carrera=request.json['carrera']
    duracion=request.json['duracion']
    tecnologias=request.json['tecnologias']
 
    oferta.carrera=carrera
    oferta.duracion=duracion
    oferta.tecnologias=tecnologias
    db.session.commit()
    return oferta_educativa_schema.jsonify(oferta)


# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)
    
#correr en src/app.py buscar hosting para subir servidor flask