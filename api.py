from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity




app = Flask(__name__)  
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['JWT_SECRET_KEY'] = 'super-secret-key-change-this-in-production'
jwt = JWTManager(app)
db = SQLAlchemy(app)
api = Api(app)
CORS(app)
bcrypt = Bcrypt(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80), unique=True, nullable = False)
    email = db.Column(db.String(80), unique=True, nullable = False)
    password_hash = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User(name = {self.name}, email = {self.email})"  
    

'''

#user_args = reqparse.RequestParser()
#user_args.add_argument('name', type= str, required= True, help= 'Name cannot be blank')
#user_args.add_argument('email', type= str, required= True, help= 'Email cannot be blank')
'''


auth_args = reqparse.RequestParser()
auth_args.add_argument('name', type=str)
auth_args.add_argument('email', type=str, required=True, help='Email cannot be blank')
auth_args.add_argument('password', type=str, required=True, help='Password cannot be blank')

userFields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String,
}


class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
   
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201

class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        return user    
   
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        if args["name"]:
            user.name = args["name"]    
        if args["email"]:
            user.email = args["email"]    
        db.session.commit()
        return user    
   
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)    
        db.session.commit()
        return {'message': 'User deleted'}, 200

class Signup(Resource):
    def post(self):
        args = auth_args.parse_args()
        if UserModel.query.filter_by(email=args['email']).first():
            abort(409, "Email already registered")
        if args['name'] and UserModel.query.filter_by(name=args['name']).first():
            abort(409, "Name already taken")

        user = UserModel(name=args['name'], email=args['email'])
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully"}, 201
    

class Login(Resource):
    def post(self):
        args = auth_args.parse_args()
        user = UserModel.query.filter_by(email=args['email']).first()
        if user and user.check_password(args['password']):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
        abort(401, "Invalid credentials")

class ForgotPassword(Resource):
    def post(self):
        # In a real app, send email with reset link/token
        # Here: just return a message (extend later with flask-mail)
        args = reqparse.RequestParser()
        args.add_argument('email', type=str, required=True)
        data = args.parse_args()
        user = UserModel.query.filter_by(email=data['email']).first()
        if user:
            # Generate a temporary token (similar to login)
            reset_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=15))
            return {"message": "Reset token generated (in real app: check email)", "reset_token": reset_token}
        return {"message": "If email exists, a reset link was sent"}, 200


api.add_resource(Signup, '/api/auth/signup')
api.add_resource(Login, '/api/auth/login')
api.add_resource(ForgotPassword, '/api/auth/forgot-password')
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')


'''
class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = USerModel.query.all()
        return users
    
    @marshal_with(userFields)
    def post(self):
        args = auth_args.parse_args()
        user= USerModel(name=args["name"], email= args["email"])
        db.session.add(user)
        db.session.commit()
        users = USerModel.query.all()
        return users, 201

class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = USerModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        return user    
    
    @marshal_with(userFields)
    def patch(self, id):
        args = auth_args.parse_args()
        user = USerModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        user.name = args["name"]    
        user.email = args["email"]    
        db.session.commit()
        return user    
    
    @marshal_with(userFields)
    def delete(self, id):
        user = USerModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)     
        db.session.commit()
        users = USerModel.query.all()
        return users


api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')
'''


@app.route('/')
def home_page():
    return '<h1>Flask REST API <h1>'

    
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True)




