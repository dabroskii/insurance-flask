import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import axiosInstance from "../services/axios"; // Adjust the path based on your project structure

const Login = ({ setLoggedInUser }) => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate(); // Use navigate for redirection

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.post("/login", formData); // Use axiosInstance
      console.log("Login response headers:", response.headers);
      console.log("Backend Response:", response.data); // Debugging response
      setLoggedInUser(response.data.message); // Store logged-in user
      setError(""); // Clear any previous errors
      navigate("/dashboard"); // Redirect to the dashboard
    } catch (err) {
      console.error("Login Error:", err.response?.data || err.message); // Debugging error
      setError(err.response?.data?.error || "Invalid username or password");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
