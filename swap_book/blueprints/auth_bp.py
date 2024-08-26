from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models.User_model import db, User

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        try:
            first_name = request.json['first_name']
            last_name = request.json['last_name']
            pen_name = request.json.get('pen_name')
            password = generate_password_hash(request.json['password'], method='sha256')
            dob = datetime.strptime(request.json['dob'], '%Y-%m-%d')
            email = request.json['email']
            phone_number = request.json['phone_number']

            new_user = User(first_name=first_name, last_name=last_name, pen_name=pen_name, 
                            password=password, dob=dob, email=email, phone_number=phone_number)

            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "Registration successful! Please log in."}), 201
        
        except KeyError as e:
            return jsonify({"error": f"Missing required field: {str(e)}"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            email_or_phone = request.json['email_or_phone']
            password = request.json['password']

            user = User.query.filter((User.email == email_or_phone) | (User.phone_number == email_or_phone)).first()

            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return jsonify({"message": "Login successful!", "user_id": user.id}), 200
            else:
                return jsonify({"error": "Invalid credentials. Please try again."}), 401

        except KeyError as e:
            return jsonify({"error": f"Missing required field: {str(e)}"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@auth_bp.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()

        if user:
            return jsonify({"user_id": user.id}), 200
        else:
            return jsonify({"error": "User not found."}), 404
    else:
        return jsonify({"error": "Please log in first."}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "You have been logged out."}), 200
