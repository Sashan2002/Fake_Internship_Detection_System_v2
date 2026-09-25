import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Layout() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <div className="app-shell">
      <header className="topbar">
        <NavLink className="brand" to="/dashboard">
          <span className="mark"></span> Internship Advert Review
        </NavLink>
        <nav>
          <NavLink to="/dashboard" className={({ isActive }) => (isActive ? "active" : "")}>Dashboard</NavLink>
          <NavLink to="/analyse" className={({ isActive }) => (isActive ? "active" : "")}>Analyse</NavLink>
          <NavLink to="/history" className={({ isActive }) => (isActive ? "active" : "")}>History</NavLink>
          <NavLink to="/about" className={({ isActive }) => (isActive ? "active" : "")}>About</NavLink>
          {isAuthenticated && (
            <a href="#" onClick={(e) => { e.preventDefault(); logout(); window.location.href = "/"; }}>
              Sign out
            </a>
          )}
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
      <footer>
        Decision-support tool. Predictions describe model output, not confirmed fact — see About / Methodology.
      </footer>
    </div>
  );
}
