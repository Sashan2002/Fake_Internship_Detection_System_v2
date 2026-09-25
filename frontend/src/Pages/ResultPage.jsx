import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api/client";

function Bar({ value, className = "" }) {
  const pct = Math.round((value ?? 0) * 100);
  return (
    <div className="bar-track">
      <div className={`bar-fill ${className}`} style={{ width: `${pct}%` }} />
    </div>
  );
}

function verdictClass(predictedClass) {
  if (predictedClass === "Potentially Legitimate") return "legitimate";
  if (predictedClass === "Potentially Fraudulent") return "fraudulent";
  return "review";
}

function formatLabel(key) {
  return key.replace(/_/g, " ").replace("present", "").trim().replace(/^\w/, (c) => c.toUpperCase());
}

export default function ResultPage() {
  const { predictionId } = useParams();
  const [prediction, setPrediction] = useState(null);
  const [credibility, setCredibility] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const pred = await api.getPrediction(predictionId);
        if (cancelled) return;
        setPrediction(pred);

        const ad = await api.getAdvertisement(pred.advertisement);
        if (cancelled) return;

        const cred = await api.analyseCredibility({ ...ad, advertisement_id: ad.id });
        if (cancelled) return;
        setCredibility(cred);

        const exp = await api.getExplanation(pred.id);
        if (cancelled) return;
        setExplanation(exp);
      } catch (err) {
        if (!cancelled) setError(err.message);
      }
    }

    load();
    return () => { cancelled = true; };
  }, [predictionId]);

  if (error) {
    return <p className="muted">Could not load result: {error}</p>;
  }

  if (!prediction) {
    return <p className="muted">Loading result…</p>;
  }

  const cls = verdictClass(prediction.predicted_class);
  const presenceEntries = credibility
    ? Object.entries(credibility.feature_vector).filter(([k]) => k.endsWith("_present"))
    : [];

  return (
    <div className="stack">
      <h1>Analysis result</h1>

      <div className={`verdict ${cls}`}>
        <div>
          <p className="label">{prediction.predicted_class}</p>
          <p className="sub">
            {cls === "review"
              ? "The model's confidence was too low for a clear prediction. Human review is recommended."
              : "This is the model's prediction, not confirmed fact."}
          </p>
        </div>
      </div>

      <div className="panel">
        <div className="panel-header">
          <h2 style={{ fontSize: "1.1rem", margin: 0 }}>Prediction detail</h2>
          <span className="meta">
            Model {prediction.model_version} · {new Date(prediction.created_at).toLocaleString()}
          </span>
        </div>
        <div className="metric-row">
          <span>Fraud probability</span>
          <Bar value={prediction.fraud_probability} className="fraud" />
          <span>{Math.round(prediction.fraud_probability * 100)}%</span>
        </div>
        <div className="metric-row">
          <span>Confidence</span>
          <Bar value={prediction.confidence} />
          <span>{Math.round(prediction.confidence * 100)}%</span>
        </div>
        <div className="metric-row">
          <span>Uncertainty</span>
          <Bar value={prediction.uncertainty ?? 0} className="legit" />
          <span>{Math.round((prediction.uncertainty ?? 0) * 100)}%</span>
        </div>
      </div>

      <div className="panel">
        <div className="panel-header">
          <h2 style={{ fontSize: "1.1rem", margin: 0 }}>Employer / advertisement credibility indicators</h2>
        </div>
        {!credibility && <p className="muted">Loading…</p>}
        {credibility && (
          <>
            <div className="indicator-grid">
              {presenceEntries.map(([key, val]) => (
                <div className="indicator" key={key}>
                  <span>{formatLabel(key)}</span>
                  <span className={`value ${val ? "present" : "absent"}`}>{val ? "Present" : "Absent"}</span>
                </div>
              ))}
            </div>
            <p className="notice">{credibility.disclaimer}</p>
          </>
        )}
      </div>

      <div className="panel">
        <div className="panel-header">
          <h2 style={{ fontSize: "1.1rem", margin: 0 }}>Influential factors (explanation)</h2>
        </div>
        {!explanation && <p className="muted">Loading…</p>}
        {explanation && !explanation.available && (
          <p className="muted">{explanation.reason || "Not available."}</p>
        )}
        {explanation && explanation.available && (
          <ul className="evidence-list">
            {(explanation.top_factors || []).map((f, i) => (
              <li className="evidence-item" key={i}>
                <span className="token">{f.token || f.feature}</span>
                <span className={`direction ${f.direction}`}>
                  {f.direction === "increases_fraud_signal" ? "↑ fraud signal" : "↓ fraud signal"}
                </span>
              </li>
            ))}
            {(explanation.top_factors || []).length === 0 && (
              <li className="evidence-item"><span className="muted">No strongly influential factors identified.</span></li>
            )}
          </ul>
        )}
        {explanation && <p className="notice">{explanation.disclaimer}</p>}
      </div>

      <p className="notice">
        "Potentially Legitimate" and "Potentially Fraudulent" describe this model's prediction, not
        proof of an organisation's legitimacy or fraud. Treat this result as decision support and use
        independent judgement, particularly for "Requires Review" outcomes.
      </p>
    </div>
  );
}
