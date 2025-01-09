from flask import Flask, jsonify
from flask_cors import CORS
from backend.extensions import db
from backend.routes.api_routes import api
from sqlalchemy import text
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

# Configure a secret key for JWT Token
app.config["JWT_SECRET_KEY"] = "82992505"  # Ensure this is strong and consistent
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_ALGORITHM"] = "HS256"  # Use HS256 for consistency
jwt = JWTManager(app)


# Configure CORS with specific origin
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/dabroskii/Downloads/insurance-flask/backend/insurance_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Inspect database tables before running the app
with app.app_context():
    result = db.session.execute(text('SELECT name FROM sqlite_master WHERE type="table";')).fetchall()
    print(f"Tables in the database: {result}")  # Print available tables

# Register the API blueprint
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def home():
    return "Check logs for table names!"

# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    response = jsonify({"error": str(e)})
    response.status_code = 500
    return response

# Handle expired tokens
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Session expired, please log in again"}), 401

if __name__ == '__main__':
    app.run(debug=True)