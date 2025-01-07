from flask import Flask, jsonify
from flask_cors import CORS
from backend.extensions import db
from backend.routes.api_routes import api
from sqlalchemy import text
from flask_session import Session

app = Flask(__name__)

# Configure a secret key for session handling
app.config['SECRET_KEY'] = '82992505'  # Replace with a strong, unique value

# Configure CORS with specific origin
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/dabroskii/Downloads/insurance-flask/backend/insurance_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Configure session handling
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['SESSION_COOKIE_DOMAIN'] = None
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Correctly set Samesite attribute
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions in files
app.config['SESSION_PERMANENT'] = False    # Make sessions non-permanent
app.config['SESSION_USE_SIGNER'] = True    # Sign the session ID cookie
Session(app)

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

@app.errorhandler(Exception)
def handle_exception(e):
    response = jsonify({"error": str(e)})
    response.status_code = 500
    return response

if __name__ == '__main__':
    app.run(debug=True)
