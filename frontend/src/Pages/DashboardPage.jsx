import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

export default function DashboardPage() {
  const { user } = useAuth();
  const [ads, setAds] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.listAdvertisementsForUser(user.id)
      .then(setAds)
      .catch((err) => setError(err.message));
  }, [user.id]);

  return (
    <div className="stack">
      <div>
        <h1>Dashboard</h1>
        <p className="muted">Submit a new advertisement for analysis, or review your recent results.</p>
      </div>

      <div className="panel">
        <div className="panel-header">
          <h2 style={{ fontSize: "1.1rem", margin: 0 }}>Quick actions</h2>
        </div>
        <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
          <Link to="/analyse" className="btn">Analyse a new advertisement</Link>
          <Link to="/history" className="btn secondary">View analysis history</Link>
        </div>
      </div>

      <div className="panel">
        <div className="panel-header">
          <h2 style={{ fontSize: "1.1rem", margin: 0 }}>Recent submissions</h2>
          <span className="meta">Most recent first</span>
        </div>
        {error && <p className="muted">Could not load recent submissions ({error}).</p>}
        {!error && ads === null && <p className="muted">Loading…</p>}
        {!error && ads !== null && ads.length === 0 && (
          <p className="muted">No submissions yet. <Link to="/analyse">Analyse your first advertisement</Link>.</p>
        )}
        {!error && ads !== null && ads.length > 0 && ads.slice(0, 5).map((ad) => (
          <div className="indicator" key={ad.id}>
            <span>{ad.title}</span>
            <span className="muted">{new Date(ad.created_at).toLocaleDateString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
