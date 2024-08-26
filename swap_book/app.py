from flask import Flask
from models.User_model import db, User
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # Best practice is to set this to False

# Initialize the database with the app
db.init_app(app)

# Import and register the blueprint
from blueprints.auth_bp import auth_bp
app.register_blueprint(auth_bp)

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
