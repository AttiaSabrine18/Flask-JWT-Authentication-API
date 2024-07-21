from flask import Flask ,request, jsonify, make_response, current_app
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os
import jwt
import datetime
import uuid
from functools import wraps
from models import db, init_db
from models.user import User

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# Configuration
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# Initialiser la base de données
init_db(app)

# Initialiser bcrypt
bcrypt = Bcrypt(app)
# Initialiser marshmallow
ma = Marshmallow(app)



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid !!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated
#Ajout du paramètre current_user: La fonction get_all_users doit accepter 
#current_user comme argument pour correspondre à la signature de la fonction retournée par le décorateur token_required.
@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()
    output = [{'public_id': user.public_id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify({'users': output})

@app.route('/login', methods=['POST'])
def login():
    auth = request.form
    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm ="Login required !!"'})
    
    user = User.query.filter_by(email=auth.get('email')).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'})
    
    if bcrypt.check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
        return make_response(jsonify({'token': token}), 201)
    
    return make_response('Could not verify', 403, {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Vérifiez que les champs requis sont présents
    if not name or not email or not password:
        return make_response('Missing name, email or password', 400)

    # Vérifiez si l'utilisateur existe déjà
    user = User.query.filter_by(email=email).first()
    if not user:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(public_id=str(uuid.uuid4()), name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return make_response('Successfully registered.', 201)
    
    return make_response('User already exists. Please Log in.', 202)

  
# Enable CORS for all domains
CORS(app)


if __name__ == "__main__":
    app.run(debug=True)
