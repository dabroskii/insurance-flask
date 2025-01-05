import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

const App = () => {
  const [loggedInUser, setLoggedInUser] = useState("");

  return (
    <Router>
      <Routes>
        {/* Pass setLoggedInUser to Login */}
        <Route path="/" element={<Login setLoggedInUser={setLoggedInUser} />} />

        {/* Pass both loggedInUser and setLoggedInUser to Dashboard */}
        <Route path="/dashboard" element={<Dashboard loggedInUser={loggedInUser} setLoggedInUser={setLoggedInUser} />} />
      </Routes>
    </Router>
  );
};

export default App;
