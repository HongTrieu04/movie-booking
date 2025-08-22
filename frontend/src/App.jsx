import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginForm from "./Login/LoginForm";
import RegisterForm from "./Login/RegisterForm";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
