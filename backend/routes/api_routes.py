from flask import Blueprint, request, jsonify, session, current_app
from backend.models.models import User, InsuranceClaim, InsurancePolicy
from backend.extensions import db
from datetime import datetime

# Create a Blueprint for API routes
api = Blueprint('api', __name__)

# --------------------------------
# Login Route
# --------------------------------

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')  # Assuming username maps to EmployeeID
    password = data.get('password')  # Assuming password maps to Password

    # Debugging to confirm app context and query execution
    with current_app.app_context():
        print(f"App context active: {current_app.app_context() is not None}")
        user = User.query.filter_by(employee_id=username, password=password).first()

    if user:
        session['user_id'] = user.employee_id
        return jsonify({"message": f"Welcome, {user.first_name}!"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# --------------------------------
# Dashboard Route
# --------------------------------

@api.route('/claims/dashboard', methods=['GET'])
def get_dashboard():
    # Retrieve the logged-in user's ID from the session
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Query claims related to the logged-in employee
    claims = db.session.query(InsuranceClaim).join(InsurancePolicy).filter(InsurancePolicy.employee_id == user_id).all()

    result = {
        "pending": [],
        "approved": [],
        "rejected": []
    }

    for claim in claims:
        claim_data = {
            "claim_id": claim.claim_id,
            "insurance_id": claim.insurance_id,
            "first_name": claim.first_name,
            "last_name": claim.last_name,
            "expense_date": claim.expense_date,
            "amount": claim.amount,
            "purpose": claim.purpose,
            "status": claim.status
        }
        if claim.status.lower() == "pending":
            result["pending"].append(claim_data)
        elif claim.status.lower() == "approved":
            result["approved"].append(claim_data)
        elif claim.status.lower() == "rejected":
            result["rejected"].append(claim_data)

    return jsonify(result), 200

# --------------------------------
# Manage Claims (Create, Update, Delete)
# --------------------------------

@api.route('/claims', methods=['POST'])
def create_claim():
    data = request.get_json()
    new_claim = InsuranceClaim(
        insurance_id=data['insurance_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        expense_date=data['expense_date'],
        amount=data['amount'],
        purpose=data['purpose'],
        follow_up=data['follow_up'],  # Added follow_up mapping
        previous_claim_id=data.get('previous_claim_id'),
        status=data['status'],
        last_edited_date=data['last_edited_date']
    )
    db.session.add(new_claim)
    db.session.commit()
    return jsonify({"message": "Claim created successfully!", "claim_id": new_claim.claim_id}), 201

@api.route('/claims/<int:claim_id>', methods=['PUT'])
def update_claim(claim_id):
    # Get the logged-in user's ID
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Retrieve the claim and validate it belongs to the logged-in user
    claim = db.session.query(InsuranceClaim).join(InsurancePolicy).filter(
        InsuranceClaim.claim_id == claim_id,
        InsurancePolicy.employee_id == user_id
    ).first()

    if not claim:
        return jsonify({"error": "Claim not found or not authorized"}), 404

    # Check if the claim is pending or rejected
    if claim.status.lower() not in ['pending', 'rejected']:
        return jsonify({"error": "Only pending or rejected claims can be updated"}), 403

    # Update the claim
    data = request.get_json()
    claim.insurance_id = data.get('insurance_id', claim.insurance_id)
    claim.first_name = data.get('first_name', claim.first_name)
    claim.last_name = data.get('last_name', claim.last_name)
    claim.expense_date = data.get('expense_date', claim.expense_date)
    claim.amount = data.get('amount', claim.amount)
    claim.purpose = data.get('purpose', claim.purpose)
    claim.follow_up = data.get('follow_up', claim.follow_up)
    claim.previous_claim_id = data.get('previous_claim_id', claim.previous_claim_id)
    claim.status = data.get('status', claim.status)

    # Auto-populate `last_edited_date`
    claim.last_edited_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    db.session.commit()
    return jsonify({"message": "Claim updated successfully!"}), 200


@api.route('/claims/<int:claim_id>', methods=['DELETE'])
def delete_claim(claim_id):
    # Get the logged-in user's ID
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Retrieve the claim and validate it belongs to the logged-in user
    claim = db.session.query(InsuranceClaim).join(InsurancePolicy).filter(
        InsuranceClaim.claim_id == claim_id,
        InsurancePolicy.employee_id == user_id
    ).first()

    if not claim:
        return jsonify({"error": "Claim not found or not authorized"}), 404

    # Check if the claim is pending or rejected
    if claim.status.lower() not in ['pending', 'rejected']:
        return jsonify({"error": "Only pending or rejected claims can be deleted"}), 403

    # Delete the claim
    db.session.delete(claim)
    db.session.commit()
    return jsonify({"message": "Claim deleted successfully!"}), 200
