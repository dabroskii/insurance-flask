import React, { useEffect, useState } from "react";
import axiosInstance from "../services/axios";
import { useNavigate } from "react-router-dom";

const Dashboard = ({ loggedInUser, setLoggedInUser }) => {
  const [claims, setClaims] = useState({ pending: [], approved: [], rejected: [] });
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showUpdateForm, setShowUpdateForm] = useState(false);
  const [currentClaimId, setCurrentClaimId] = useState(null);
  const [formData, setFormData] = useState({
    insurance_id: "",
    first_name: "",
    last_name: "",
    expense_date: "",
    amount: "",
    purpose: "",
    follow_up: false, // Ensure this key exists
    status: "pending",
  });

  const navigate = useNavigate();

  // Fetch claims
  const fetchClaims = async () => {
    try {
      const response = await axiosInstance.get("/claims/dashboard");
      setClaims(response.data);
    } catch (err) {
      console.error("Failed to fetch claims", err);
    }
  };

  useEffect(() => {
    fetchClaims();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleCreateClaim = async () => {
    try {
      await axiosInstance.post("/claims", formData);
      alert("Claim created successfully!");
      fetchClaims(); // Refresh claims without reloading the page
      setShowCreateForm(false); // Close the create form
    } catch (err) {
      console.error("Failed to create claim", err);
      alert("Failed to create claim");
    }
  };

  const handleUpdateClaim = async () => {
    try {
      await axiosInstance.put(`/claims/${currentClaimId}`, formData);
      alert("Claim updated successfully!");
      fetchClaims(); // Refresh claims without reloading the page
      setShowUpdateForm(false); // Close the update form
    } catch (err) {
      console.error("Failed to update claim", err);
      alert("Failed to update claim");
    }
  };

  const handleDeleteClaim = async (claimId) => {
    try {
      await axiosInstance.delete(`/claims/${claimId}`);
      alert("Claim deleted successfully!");
      fetchClaims(); // Refresh claims without reloading the page
    } catch (err) {
      console.error("Failed to delete claim", err);
      alert("Failed to delete claim");
    }
  };

  const handleLogout = async () => {
    try {
      await axiosInstance.post("/logout");
      setLoggedInUser(null); // Clear user state
      localStorage.removeItem("loggedInUser"); // Clear from localStorage
      alert("Logged out successfully!");
      navigate("/"); // Redirect to login page
    } catch (err) {
      console.error("Failed to log out", err);
      alert("Failed to log out");
    }
  };

  if (!loggedInUser) {
    return <p>Please log in to view the dashboard.</p>;
  }

  return (
    <div>
      <h2>Welcome, {loggedInUser}</h2>
      <button onClick={handleLogout} style={{ marginBottom: "20px" }}>Logout</button>
      <button onClick={() => setShowCreateForm(true)}>Create Claim</button>
      {showCreateForm && (
        <div>
          <h3>Create New Claim</h3>
          <form>
            <input name="insurance_id" placeholder="Insurance ID" onChange={handleInputChange} />
            <input name="first_name" placeholder="First Name" onChange={handleInputChange} />
            <input name="last_name" placeholder="Last Name" onChange={handleInputChange} />
            <input name="expense_date" type="date" onChange={handleInputChange} />
            <input name="amount" placeholder="Amount" onChange={handleInputChange} />
            <input name="purpose" placeholder="Purpose" onChange={handleInputChange} />
            <select name="status" onChange={handleInputChange}>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
            </select>
            <button type="button" onClick={handleCreateClaim}>
              Submit
            </button>
            <button type="button" onClick={() => setShowCreateForm(false)}>
              Cancel
            </button>
          </form>
        </div>
      )}

      <h3>Pending Claims</h3>
      <ul>
        {claims.pending.map((claim) => (
          <li key={claim.claim_id}>
            {claim.purpose}: ${claim.amount} - {claim.status}
            <button onClick={() => {
              setCurrentClaimId(claim.claim_id);
              setFormData(claim);
              setShowUpdateForm(true);
            }}>
              Update
            </button>
            <button onClick={() => handleDeleteClaim(claim.claim_id)}>Delete</button>
          </li>
        ))}
      </ul>

      <h3>Approved Claims</h3>
      <ul>
        {claims.approved.map((claim) => (
          <li key={claim.claim_id}>
            {claim.purpose}: ${claim.amount} - {claim.status}
          </li>
        ))}
      </ul>

      <h3>Rejected Claims</h3>
      <ul>
        {claims.rejected.map((claim) => (
          <li key={claim.claim_id}>
            {claim.purpose}: ${claim.amount} - {claim.status}
            <button onClick={() => {
              setCurrentClaimId(claim.claim_id);
              setFormData(claim);
              setShowUpdateForm(true);
            }}>
              Update
            </button>
            <button onClick={() => handleDeleteClaim(claim.claim_id)}>Delete</button>
          </li>
        ))}
      </ul>

      {showUpdateForm && (
        <div>
          <h3>Update Claim</h3>
          <form>
            <input name="insurance_id" placeholder="Insurance ID" value={formData.insurance_id} onChange={handleInputChange} />
            <input name="first_name" placeholder="First Name" value={formData.first_name} onChange={handleInputChange} />
            <input name="last_name" placeholder="Last Name" value={formData.last_name} onChange={handleInputChange} />
            <input name="expense_date" type="date" value={formData.expense_date} onChange={handleInputChange} />
            <input name="amount" placeholder="Amount" value={formData.amount} onChange={handleInputChange} />
            <input name="purpose" placeholder="Purpose" value={formData.purpose} onChange={handleInputChange} />
            <select name="status" value={formData.status} onChange={handleInputChange}>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
            </select>
            <button type="button" onClick={handleUpdateClaim}>
              Submit
            </button>
            <button type="button" onClick={() => setShowUpdateForm(false)}>
              Cancel
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
