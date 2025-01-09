import React, { useEffect, useState, useCallback } from "react";
import axiosInstance from "../services/axios";

const Dashboard = ({ loggedInUser, handleLogout }) => {
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
    follow_up: false,
    status: "pending",
  });

  // Fetch claims
  const fetchClaims = useCallback(async () => {
    try {
      const response = await axiosInstance.get("/claims/dashboard");
      setClaims(response.data);
    } catch (err) {
      console.error("Failed to fetch claims:", err.response?.data || err.message);
      if (err.response?.status === 401) {
        alert("Session expired. Please log in again.");
        handleLogout();
      }
    }
  }, [handleLogout]);

  useEffect(() => {
    fetchClaims();
  }, [fetchClaims]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    // Adjust the date format to match the database format
    if (name === "expense_date") {
      const formattedDate = new Date(value).toISOString(); // Converts to "YYYY-MM-DDTHH:mm:ss.sssZ"
      const offset = "+08:00"; // Set timezone offset
      setFormData({ ...formData, [name]: formattedDate.replace("Z", offset) });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleCreateClaim = async () => {
    try {
      await axiosInstance.post("/claims", formData);
      alert("Claim created successfully!");
      fetchClaims();
      setShowCreateForm(false);
    } catch (err) {
      console.error("Failed to create claim:", err.response?.data || err.message);
      alert("Failed to create claim");
    }
  };

  const handleUpdateClaim = async () => {
    try {
      await axiosInstance.put(`/claims/${currentClaimId}`, formData);
      alert("Claim updated successfully!");
      fetchClaims();
      setShowUpdateForm(false);
    } catch (err) {
      console.error("Failed to update claim:", err.response?.data || err.message);
      alert("Failed to update claim");
    }
  };

  const handleDeleteClaim = async (claimId) => {
    try {
      await axiosInstance.delete(`/claims/${claimId}`);
      alert("Claim deleted successfully!");
      fetchClaims();
    } catch (err) {
      console.error("Failed to delete claim:", err.response?.data || err.message);
      alert("Failed to delete claim");
    }
  };

  const openCreateForm = () => {
    setFormData({
      insurance_id: "Default Insurance ID",
      first_name: loggedInUser.split(" ")[0],
      last_name: loggedInUser.split(" ")[1] || "",
      expense_date: "",
      amount: "",
      purpose: "",
      follow_up: false,
      status: "pending",
    });
    setShowCreateForm(true);
  };

  const openUpdateForm = (claim) => {
    setFormData(claim);
    setCurrentClaimId(claim.claim_id);
    setShowUpdateForm(true);
  };

  if (!loggedInUser) {
    return <p>Please log in to view the dashboard.</p>;
  }

  return (
    <div className="p-6 bg-gray-100 min-h-screen flex justify-center">
      <div className="w-full max-w-4xl bg-white rounded shadow-md p-4">
        <h2 className="text-2xl font-bold mb-6 text-center">Welcome, {loggedInUser}</h2>
        <div className="flex justify-between mb-4">
          <button
            onClick={openCreateForm}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Create Claim
          </button>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          >
            Logout
          </button>
        </div>

        {showCreateForm && (
          <div className="border border-gray-300 rounded p-4 mb-6">
            <h3 className="text-lg font-bold mb-4">Create New Claim</h3>
            <form className="space-y-2">
              <input
                name="insurance_id"
                placeholder="Insurance ID"
                value={formData.insurance_id}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              />
              <input
                name="first_name"
                placeholder="First Name"
                value={formData.first_name}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              />
              <input
                name="last_name"
                placeholder="Last Name"
                value={formData.last_name}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              />
              <input
                name="expense_date"
                type="date"
                value={formData.expense_date.split("T")[0]} // Only show the date part in the input
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              />
              <input
                name="amount"
                placeholder="Amount"
                value={formData.amount}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              />
              <input
                name="purpose"
                placeholder="Purpose"
                value={formData.purpose}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              />
              <select
                name="status"
                value={formData.status}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              >
                <option value="pending">Pending</option>
                <option value="approved">Approved</option>
                <option value="rejected">Rejected</option>
              </select>
              <div className="flex justify-between mt-4">
                <button
                  type="button"
                  onClick={handleCreateClaim}
                  className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                >
                  Submit
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="px-4 py-2 bg-gray-300 text-black rounded hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {showUpdateForm && (
          <div className="border border-gray-300 rounded p-4 mb-6">
            <h3 className="text-lg font-bold mb-4">Update Claim</h3>
            <form className="space-y-2">
              <input
                name="insurance_id"
                placeholder="Insurance ID"
                value={formData.insurance_id}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              />
              <input
                name="first_name"
                placeholder="First Name"
                value={formData.first_name}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              />
              <input
                name="last_name"
                placeholder="Last Name"
                value={formData.last_name}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              />
              <input
                name="expense_date"
                type="date"
                value={formData.expense_date.split("T")[0]}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              />
              <input
                name="amount"
                placeholder="Amount"
                value={formData.amount}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              />
              <input
                name="purpose"
                placeholder="Purpose"
                value={formData.purpose}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              />
              <select
                name="status"
                value={formData.status}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              >
                <option value="pending">Pending</option>
                <option value="approved">Approved</option>
                <option value="rejected">Rejected</option>
              </select>
              <div className="flex justify-between mt-4">
                <button
                  type="button"
                  onClick={handleUpdateClaim}
                  className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                  Update
                </button>
                <button
                  type="button"
                  onClick={() => setShowUpdateForm(false)}
                  className="px-4 py-2 bg-gray-300 text-black rounded hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {["pending", "approved", "rejected"].map((status) => (
          <div key={status} className="border border-gray-300 rounded p-4 mb-6">
            <h3 className="text-xl font-bold mb-4 capitalize">{status} Claims</h3>
            {claims[status].length === 0 ? (
              <p className="text-gray-500">No {status} claims available.</p>
            ) : (
              <table className="w-full table-auto border-collapse">
                <thead>
                  <tr>
                    <th className="border border-gray-300 px-4 py-2">Purpose</th>
                    <th className="border border-gray-300 px-4 py-2">Amount</th>
                    <th className="border border-gray-300 px-4 py-2">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {claims[status].map((claim) => (
                    <tr key={claim.claim_id} className="hover:bg-gray-100">
                      <td className="border border-gray-300 px-4 py-2">{claim.purpose}</td>
                      <td className="border border-gray-300 px-4 py-2">${claim.amount}</td>
                      <td className="border border-gray-300 px-4 py-2 text-center">
                        {status === "approved" ? (
                          <span className="text-gray-500">No Actions Allowed</span>
                        ) : (
                          <>
                            <button
                              onClick={() => openUpdateForm(claim)}
                              className="px-2 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600 mr-2"
                            >
                              Update
                            </button>
                            <button
                              onClick={() => handleDeleteClaim(claim.claim_id)}
                              className="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600"
                            >
                              Delete
                            </button>
                          </>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
