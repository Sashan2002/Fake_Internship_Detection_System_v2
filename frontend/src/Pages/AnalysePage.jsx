import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

const initialForm = {
  title: "", description: "", requirements: "", benefits: "",
  location: "", salary_range: "", employer_name: "", company_profile: "",
  industry: "", employment_type: "", has_company_logo: false, has_questions: false,
};

export default function AnalysePage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState(initialForm);
  const [errors, setErrors] = useState([]);
  const [submitting, setSubmitting] = useState(false);

  function update(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setErrors([]);
    setSubmitting(true);

    const payload = { ...form, user: user.id };

    try {
      const { advertisement_id } = await api.createAdvertisement(payload);
      const prediction = await api.predict({ ...payload, advertisement_id });

      if (prediction.prediction_id) {
        navigate(`/result/${prediction.prediction_id}`);
      } else {
        setErrors(["Prediction completed but could not be linked to a saved record."]);
      }
    } catch (err) {
      setErrors([err.message]);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <h1>Analyse an internship advertisement</h1>
      <p className="muted">
        Paste the advertisement text and any employer details you have. The more fields you
        complete, the more complete the credibility indicators will be.
      </p>

      {errors.length > 0 && <div className="error-list">{errors.join(", ")}</div>}

      <form onSubmit={handleSubmit}>
        <fieldset>
          <legend>Advertisement</legend>
          <div className="field">
            <label htmlFor="title">Job title</label>
            <input id="title" type="text" required placeholder="e.g. Marketing Intern"
                   value={form.title} onChange={(e) => update("title", e.target.value)} />
          </div>
          <div className="field">
            <label htmlFor="description">Description</label>
            <textarea id="description" required placeholder="Paste the full advertisement description here"
                      value={form.description} onChange={(e) => update("description", e.target.value)} />
          </div>
          <div className="field">
            <label htmlFor="requirements">Requirements</label>
            <textarea id="requirements" placeholder="Optional"
                      value={form.requirements} onChange={(e) => update("requirements", e.target.value)} />
          </div>
          <div className="field">
            <label htmlFor="benefits">Benefits</label>
            <textarea id="benefits" placeholder="Optional"
                      value={form.benefits} onChange={(e) => update("benefits", e.target.value)} />
          </div>
          <div className="field-row">
            <div className="field">
              <label htmlFor="location">Location</label>
              <input id="location" type="text" value={form.location} onChange={(e) => update("location", e.target.value)} />
            </div>
            <div className="field">
              <label htmlFor="salary_range">Salary range</label>
              <input id="salary_range" type="text" placeholder="e.g. $18,000 - $22,000"
                     value={form.salary_range} onChange={(e) => update("salary_range", e.target.value)} />
            </div>
          </div>
        </fieldset>

        <fieldset>
          <legend>Employer information</legend>
          <div className="field">
            <label htmlFor="employer_name">Employer name</label>
            <input id="employer_name" type="text" value={form.employer_name} onChange={(e) => update("employer_name", e.target.value)} />
          </div>
          <div className="field">
            <label htmlFor="company_profile">Company profile</label>
            <textarea id="company_profile" placeholder="Optional description of the employer"
                      value={form.company_profile} onChange={(e) => update("company_profile", e.target.value)} />
          </div>
          <div className="field-row">
            <div className="field">
              <label htmlFor="industry">Industry</label>
              <input id="industry" type="text" value={form.industry} onChange={(e) => update("industry", e.target.value)} />
            </div>
            <div className="field">
              <label htmlFor="employment_type">Employment type</label>
              <input id="employment_type" type="text" placeholder="e.g. Internship"
                     value={form.employment_type} onChange={(e) => update("employment_type", e.target.value)} />
            </div>
          </div>
          <div className="checkbox-field">
            <input id="has_company_logo" type="checkbox" checked={form.has_company_logo}
                   onChange={(e) => update("has_company_logo", e.target.checked)} />
            <label htmlFor="has_company_logo">Advertisement displays a company logo</label>
          </div>
          <div className="checkbox-field">
            <input id="has_questions" type="checkbox" checked={form.has_questions}
                   onChange={(e) => update("has_questions", e.target.checked)} />
            <label htmlFor="has_questions">Application includes screening questions</label>
          </div>
        </fieldset>

        <button type="submit" className="btn" disabled={submitting}>
          {submitting ? "Analysing…" : "Run analysis"}
        </button>
      </form>

      {submitting && (
        <div className="panel" style={{ marginTop: "1.25rem" }}>
          <h3 style={{ marginBottom: "0.5rem" }}>Analysing submission…</h3>
          <p className="muted" style={{ margin: 0 }}>
            Running NLP analysis and employer credibility checks. This is usually quick.
          </p>
        </div>
      )}
    </div>
  );
}
