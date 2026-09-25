import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const [mode, setMode] = useState("login"); // "login" | "register"
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState([]);
  const [submitting, setSubmitting] = useState(false);

  const navigate = useNavigate();
  const { login } = useAuth();

  const isRegister = mode === "register";

  async function handleSubmit(e) {
    e.preventDefault();
    setErrors([]);
    setSubmitting(true);
    try {
      const result = isRegister
        ? await api.register({ name, email, password })
        : await api.login({ email, password });
      login(result.token, result.user);
      navigate("/dashboard");
    } catch (err) {
      setErrors([err.message]);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="/"><span className="mark"></span> Internship Advert Review</a>
      </header>
      <main className="narrow">
        <div className="panel">
          <div className="panel-header">
            <h1 style={{ fontSize: "1.4rem", margin: 0 }}>{isRegister ? "Register" : "Sign in"}</h1>
            <a
              href="#"
              className="meta"
              onClick={(e) => { e.preventDefault(); setMode(isRegister ? "login" : "register"); setErrors([]); }}
            >
              {isRegister ? "Already have an account? Sign in" : "Need an account? Register"}
            </a>
          </div>

          {errors.length > 0 && <div className="error-list">{errors.join("<br>")}</div>}

          <form onSubmit={handleSubmit}>
            {isRegister && (
              <div className="field">
                <label htmlFor="name">Full name</label>
                <input id="name" type="text" value={name} onChange={(e) => setName(e.target.value)} required autoComplete="name" />
              </div>
            )}
            <div className="field">
              <label htmlFor="email">Email</label>
              <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required autoComplete="email" />
            </div>
            <div className="field">
              <label htmlFor="password">Password</label>
              <input
                id="password" type="password" value={password}
                onChange={(e) => setPassword(e.target.value)} required
                autoComplete={isRegister ? "new-password" : "current-password"}
              />
            </div>
            <button type="submit" className="btn" disabled={submitting}>
              {isRegister ? "Create account" : "Sign in"}
            </button>
          </form>

          <p className="notice">
            This tool provides decision support for reviewing internship advertisements.
            It does not replace independent verification of an employer.
          </p>
        </div>
      </main>
    </div>
  );
}
