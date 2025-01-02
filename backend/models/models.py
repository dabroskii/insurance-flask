from backend.extensions import db

class User(db.Model):
    __tablename__ = 'User'  # Match the table name exactly
    employee_id = db.Column('EmployeeID', db.Integer, primary_key=True)
    password = db.Column('Password', db.Text, nullable=False)
    first_name = db.Column('FirstName', db.Text, nullable=False)
    last_name = db.Column('LastName', db.Text, nullable=False)
    age = db.Column('Age', db.Integer, nullable=False)

    # Relationship with InsurancePolicies
    insurance_policies = db.relationship('InsurancePolicy', backref='user', cascade='all, delete-orphan', lazy=True)


class InsurancePolicy(db.Model):
    __tablename__ = 'InsurancePolicies'  # Match the table name exactly
    insurance_id = db.Column('InsuranceID', db.Integer, primary_key=True)
    employee_id = db.Column('EmployeeID', db.Integer, db.ForeignKey('User.EmployeeID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    insurance_type = db.Column('InsuranceType', db.Text, nullable=False)
    policy_start_date = db.Column('PolicyStartDate', db.Text, nullable=False)
    policy_term = db.Column('PolicyTerm', db.Text, nullable=False)
    policy_end_date = db.Column('PolicyEndDate', db.Text, nullable=False)
    claim_limit = db.Column('ClaimLimit', db.Float, nullable=False)
    remaining_claim_limit = db.Column('RemainingClaimLimit', db.Float, nullable=False)

    # Relationship with InsuranceClaims
    insurance_claims = db.relationship('InsuranceClaim', backref='policy', cascade='all, delete-orphan', lazy=True)


class InsuranceClaim(db.Model):
    __tablename__ = 'InsuranceClaims'  # Match the table name exactly
    claim_id = db.Column('ClaimID', db.Integer, primary_key=True)
    insurance_id = db.Column('InsuranceID', db.Integer, db.ForeignKey('InsurancePolicies.InsuranceID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    first_name = db.Column('FirstName', db.Text, nullable=False)
    last_name = db.Column('LastName', db.Text, nullable=False)
    expense_date = db.Column('ExpenseDate', db.Text, nullable=False)
    amount = db.Column('Amount', db.Float, nullable=False)
    purpose = db.Column('Purpose', db.Text, nullable=False)
    follow_up = db.Column('FollowUp', db.Boolean, nullable=False)
    previous_claim_id = db.Column('PreviousClaimID', db.Integer, nullable=True)
    status = db.Column('Status', db.Text, nullable=False)
    last_edited_date = db.Column('LastEditedClaimDate', db.Text, nullable=False)
