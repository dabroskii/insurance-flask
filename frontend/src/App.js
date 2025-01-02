import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

const App = () => {
  const [loggedInUser, setLoggedInUser] = useState("");

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login setLoggedInUser={setLoggedInUser} />} />
        <Route path="/dashboard" element={<Dashboard loggedInUser={loggedInUser} />} />
      </Routes>
    </Router>
  );
};

export default App;
