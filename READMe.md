Insurance Management System
A web application for managing insurance claims and policies, built with Flask (backend) and React (frontend).

Features
User authentication with session management.
View and manage insurance claims:
Create, update, and delete claims.
Filter claims by status (Pending, Approved, Rejected).
Backend built with Flask, SQLAlchemy, and Flask-Session.
Frontend built with React.
Prerequisites
Python 3.10 or above
Node.js (LTS version recommended)
npm or Yarn
SQLite (for local development) or a database of your choice (PostgreSQL/MySQL)
Docker (optional, for shared development environments)
Installation
Backend
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/insurance-management.git
cd insurance-management/backend
Create and activate a virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the database:

For SQLite:
bash
Copy code
export DATABASE_URL="sqlite:///instance/local_database.db"
For MySQL/PostgreSQL, update the DATABASE_URL environment variable.
Initialize the database:

bash
Copy code
flask db upgrade
Start the backend server:

bash
Copy code
flask run
The backend server will run at http://127.0.0.1:5000.

Frontend
Navigate to the frontend folder:

bash
Copy code
cd ../frontend
Install dependencies:

bash
Copy code
npm install
Start the development server:

bash
Copy code
npm start
The frontend server will run at http://localhost:3000.

Environment Variables
Create a .env file in the backend directory to store sensitive information:

makefile
Copy code
DATABASE_URL=sqlite:///instance/local_database.db
SECRET_KEY=your-secret-key
FLASK_ENV=development
If using Docker, ensure the .env file is included in your Docker configuration.

Project Structure
csharp
Copy code
insurance-management/
│
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── config.py               # App configurations
│   ├── models/                 # SQLAlchemy models
│   ├── routes/                 # API route definitions
│   ├── extensions.py           # Flask extensions
│   ├── requirements.txt        # Backend dependencies
│   └── instance/               # SQLite database files
│
├── frontend/
│   ├── src/
│   │   ├── pages/              # React pages (Dashboard, Login)
│   │   ├── services/           # Axios instance
│   │   └── App.js              # Main React app
│   ├── package.json            # Frontend dependencies
│   └── public/                 # Static files
│
└── README.md                   # Project documentation
Usage
Login
Use preloaded accounts in the User table for authentication.

Example credentials:
makefile
Copy code
Username: 58001002
Password: DBSB#stB4nk
After logging in, the dashboard displays claims categorized by their status.

Claims Management
Create a Claim:
Use the "Create Claim" button to add a new claim.
Update a Claim:
Click "Update" next to a claim to edit its details.
Delete a Claim:
Click "Delete" to remove a claim.
Logout
Use the "Logout" button to end your session and return to the login page.
Running with Docker (Optional)
Build and run the Docker containers:

bash
Copy code
docker-compose up
Access the app:

Frontend: http://localhost:3000
Backend: http://127.0.0.1:5000
Testing
Backend
Run the tests using pytest:

bash
Copy code
pytest
Frontend
Run the tests using npm:

bash
Copy code
npm test
Contributing
Fork the repository and create a new branch:

bash
Copy code
git checkout -b feature-name
Commit your changes and push the branch:

bash
Copy code
git add .
git commit -m "Description of changes"
git push origin feature-name
Submit a pull request for review.

Troubleshooting
CORS Errors
Ensure the frontend runs on http://localhost:3000 and the backend on http://127.0.0.1:5000.
Verify that Flask-CORS is properly configured in app.py.
Database Errors
Check the DATABASE_URL and ensure the database exists.
For SQLite, ensure the instance folder is writable.
License
This project is licensed under the MIT License.