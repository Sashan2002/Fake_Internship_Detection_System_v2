/**
 * Small fetch wrapper for the Django REST API.
 *
 * Auth: DRF's TokenAuthentication. The token returned by /auth/login or
 * /auth/register is stored in localStorage and attached as
 * `Authorization: Token <token>` on every subsequent request.
 */
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";

function getToken() {
  return localStorage.getItem("token");
}

function getUser() {
  const raw = localStorage.getItem("user");
  return raw ? JSON.parse(raw) : null;
}

function setSession(token, user) {
  localStorage.setItem("token", token);
  localStorage.setItem("user", JSON.stringify(user));
}

function clearSession() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
}

async function apiRequest(path, options = {}) {
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Token ${token}` } : {}),
    ...options.headers,
  };

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    const message = (data.errors && data.errors.join(", ")) || `Request failed (${res.status})`;
    throw new Error(message);
  }
  return data;
}

export const api = {
  register: (payload) => apiRequest("/auth/register", { method: "POST", body: JSON.stringify(payload) }),
  login: (payload) => apiRequest("/auth/login", { method: "POST", body: JSON.stringify(payload) }),

  createAdvertisement: (payload) => apiRequest("/advertisements/", { method: "POST", body: JSON.stringify(payload) }),
  getAdvertisement: (id) => apiRequest(`/advertisements/${id}`),
  listAdvertisementsForUser: (userId) => apiRequest(`/advertisements/user/${userId}`),

  analyseCredibility: (payload) => apiRequest("/analyse-credibility", { method: "POST", body: JSON.stringify(payload) }),
  predict: (payload) => apiRequest("/predict", { method: "POST", body: JSON.stringify(payload) }),
  getPrediction: (id) => apiRequest(`/predictions/${id}`),
  getExplanation: (id) => apiRequest(`/explanations/${id}`),
  health: () => apiRequest("/health"),
};

export { getToken, getUser, setSession, clearSession };
