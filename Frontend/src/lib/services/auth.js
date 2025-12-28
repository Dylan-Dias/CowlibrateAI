import { authStore } from "$lib/stores/auth";
import { browser } from "$app/environment";

const API_URL = "https://cowlibrate-backend.onrender.com"; // your actual backend URL

/* -------------------------------------------------
    Helper: Fetch Wrapper with Automatic Token
------------------------------------------------- */
async function safeFetch(url, options = {}) {
  const token = browser ? localStorage.getItem("token") : null;

  let res;
  try {
    res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Authorization: token ? `Bearer ${token}` : undefined, // ✅ always include if exists
        ...(options.headers || {}),
      },
    });
  } catch (err) {
    throw new Error("Network error: Failed to connect to backend");
  }

  let data;
  try {
    data = await res.json();
  } catch {
    throw new Error("Invalid response from server");
  }

  if (!res.ok) {
    throw new Error(data.error || data.message || "Request failed");
  }

  return data;
}

/* -------------------------------------------------
    Helper: Save Auth Data (Store + localStorage)
------------------------------------------------- */
function saveAuth(token, user) {
  if (browser) {
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));
  }
  authStore.setAuth(token, user);
}

/* -------------------------------------------------
    AUTH FUNCTIONS
------------------------------------------------- */

// ✅ REGISTER
export async function register(username, email, password, role = "user") {
  const data = await safeFetch(`${API_URL}/register`, {
    method: "POST",
    body: JSON.stringify({ username, email, password, role }),
  });

  saveAuth(data.token, data.user);
  return data;
}

// ✅ LOGIN
export async function login(username, password) {
  const data = await safeFetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  const user = {
    id: data.user_id,
    username,
    role: data.role,
  };

  saveAuth(data.token, user);
  return data;
}

// ✅ LOGOUT
export function logout() {
  if (browser) {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }
  authStore.clearAuth();
}

/* -------------------------------------------------
    AUTHORIZED FETCH WRAPPER
------------------------------------------------- */
export async function authFetch(endpoint, options = {}) {
  if (!endpoint.startsWith("/")) endpoint = `/${endpoint}`;
  const fullUrl = `${API_URL}${endpoint}`;
  return safeFetch(fullUrl, options);
}

/* -------------------------------------------------
   Example Protected API Calls
------------------------------------------------- */
export async function getHealthDistribution() {
  return authFetch("/health-distribution");
}

export async function getBreedDistribution() {
  return authFetch("/breed-distribution");
}

export async function getWaterIntake() {
  return authFetch("/water-intake");
}

export async function getOptimizationResults() {
  return authFetch("/api/optimization-results");
}

export async function submitOptimization(data) {
  return authFetch("/api/optimize", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
