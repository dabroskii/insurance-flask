from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from backend.models.models import User, InsuranceClaim, InsurancePolicy
from backend.extensions import db
from datetime import datetime, timedelta

# Initialize JWT
jwt = JWTManager()

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

    user = User.query.filter_by(employee_id=username, password=password).first()

    if user:
        # Ensure employee_id is passed as a string
        access_token = create_access_token(
            identity=str(user.employee_id),  # Convert employee_id to string
            expires_delta=timedelta(hours=1),
            additional_claims={"roles": "ROLE_USER"}
        )
        return jsonify({"access_token": access_token, "message": f"Welcome, {user.first_name}!"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401



# --------------------------------
# Dashboard Route
# --------------------------------

@api.route('/claims/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    try:
        # Retrieve the logged-in user's ID from the JWT
        user_id = get_jwt_identity()
        print(f"Retrieved user_id from token: {user_id}")

        if not user_id:
            print("Error: No user_id found in token.")
            return jsonify({"error": "Unauthorized"}), 401

        # Step 1: Fetch user to ensure they exist
        user = db.session.query(User).filter_by(employee_id=user_id).first()
        if not user:
            print(f"No user found with employee_id: {user_id}")
            return jsonify({"error": "User not found"}), 404

        # Step 2: Fetch insurance policies for the user
        policies = db.session.query(InsurancePolicy).filter(InsurancePolicy.employee_id == user_id).all()
        policy_ids = [policy.insurance_id for policy in policies]
        print(f"Policy IDs for user_id {user_id}: {policy_ids}")

        if not policy_ids:
            # No policies, return empty claims
            return jsonify({"pending": [], "approved": [], "rejected": []}), 200

        # Step 3: Fetch claims associated with the policies
        claims = db.session.query(InsuranceClaim).filter(InsuranceClaim.insurance_id.in_(policy_ids)).all()
        print(f"Claims fetched for user_id {user_id}: {claims}")

        # Step 4: Organize claims into categories
        result = {"pending": [], "approved": [], "rejected": []}
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

    except Exception as e:
        print(f"Error in /claims/dashboard: {e}")
        return jsonify({"error": "Failed to process the request"}), 422

# --------------------------------
# Manage Claims (Create, Update, Delete)
# --------------------------------

@api.route('/claims', methods=['POST'])
@jwt_required()
def create_claim():
    user_id = get_jwt_identity()
    print(f"User ID from token: {user_id}")  # Debugging

    data = request.get_json()
    required_fields = ['insurance_id', 'first_name', 'last_name', 'expense_date', 'amount', 'purpose', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 422

    new_claim = InsuranceClaim(
        insurance_id=data['insurance_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        expense_date=data['expense_date'],
        amount=data['amount'],
        purpose=data['purpose'],
        follow_up=data.get('follow_up', False),
        previous_claim_id=data.get('previous_claim_id'),
        status=data['status'],
        last_edited_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    db.session.add(new_claim)
    db.session.commit()
    return jsonify({"message": "Claim created successfully!", "claim_id": new_claim.claim_id}), 201

@api.route('/claims/<int:claim_id>', methods=['PUT'])
@jwt_required()
def update_claim(claim_id):
    user_id = get_jwt_identity()  # Retrieve the logged-in user's ID from the JWT
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
@jwt_required()
def delete_claim(claim_id):
    user_id = get_jwt_identity()  # Retrieve the logged-in user's ID from the JWT

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

@api.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logged out successfully!"}), 200

