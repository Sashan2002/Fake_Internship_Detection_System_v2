import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

export default function HistoryPage() {
  const { user } = useAuth();
  const [ads, setAds] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.listAdvertisementsForUser(user.id)
      .then(setAds)
      .catch((err) => setError(err.message));
  }, [user.id]);

  return (
    <div>
      <h1>Analysis history</h1>
      <p className="muted">Previously submitted advertisements and their most recent results.</p>

      <div className="panel">
        <table className="history-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Submitted</th>
              <th>Result</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {error && <tr><td colSpan={4} className="muted">Could not load history ({error}).</td></tr>}
            {!error && ads === null && <tr><td colSpan={4} className="muted">Loading…</td></tr>}
            {!error && ads !== null && ads.length === 0 && (
              <tr><td colSpan={4} className="muted">No submissions yet.</td></tr>
            )}
            {!error && ads !== null && ads.map((ad) => (
              <tr key={ad.id}>
                <td>{ad.title}</td>
                <td>{new Date(ad.created_at).toLocaleString()}</td>
                <td className="muted">Open to view</td>
                <td><Link to="/analyse" className="btn secondary" style={{ padding: "0.35rem 0.8rem", fontSize: "0.85rem" }}>Re-analyse</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
