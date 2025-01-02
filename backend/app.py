from flask import Flask
from backend.extensions import db
from backend.routes.api_routes import api
from sqlalchemy import text

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/dabroskii/Downloads/insurance-flask/backend/insurance_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure a secret key for session handling
app.config['SECRET_KEY'] = '82992505'  # Replace with a strong, unique value

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

if __name__ == '__main__':
    app.run(debug=True)
