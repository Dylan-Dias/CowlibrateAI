import { authStore } from "$lib/stores/auth";
import { browser } from "$app/environment";

const API_URL = "https://cowlibrate.onrender.com";

// -------------------------------------------------
// Helper: Fetch Wrapper with Automatic Token
// -------------------------------------------------
async function safeFetch(url, options = {}) {
  const token = browser ? localStorage.getItem("token") : null;

  let res;
  try {
    res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Authorization: token ? `Bearer ${token}` : undefined,
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

// -------------------------------------------------
// Helper: Save Auth Data (Store + localStorage)
// -------------------------------------------------
function saveAuth(token, user) {
  if (browser) {
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));
  }
  authStore.setAuth(token, user);
}

// -------------------------------------------------
// AUTH FUNCTIONS
// -------------------------------------------------

export async function register(username, email, password, role = "user") {
  const data = await safeFetch(`${API_URL}/register`, {
    method: "POST",
    body: JSON.stringify({ username, email, password, role }),
  });

  saveAuth(data.token, data.user);
  return data;
}

export async function login(username, password) {
  const data = await safeFetch(`${API_URL}/login`, {
    method: "POST",
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

export function logout() {
  if (browser) {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }
  authStore.clearAuth();
}

// -------------------------------------------------
// Protected API Calls (uses safeFetch)
// -------------------------------------------------
export async function authFetch(endpoint, options = {}) {
  if (!endpoint.startsWith("/")) endpoint = `/${endpoint}`;
  const fullUrl = `${API_URL}${endpoint}`;
  return safeFetch(fullUrl, options);
}

export async function fetchHealthData() {
  return authFetch("/health-distribution");
}

export async function fetchBreedData() {
  return authFetch("/breed-distribution");
}

export async function fetchMilkYieldData() {
  return authFetch("/MilkYield-distribution");
}

export async function fetchWaterData() {
  return authFetch("/water-intake");
}

export async function submitOptimization(data) {
  return authFetch("/api/optimize", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

// -------------------------------------------------
// Password Reset
// -------------------------------------------------
export async function requestPasswordReset(email) {
  const res = await fetch(`${API_URL}/forgot-password`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });

  let data;
  try {
    data = await res.json();
  } catch {
    throw new Error("Invalid server response");
  }

  if (!res.ok) {
    throw new Error(data?.error || "Failed to send reset instructions");
  }

  return data;
}

export async function resetPassword(token, newPassword) {
  const res = await fetch(`${API_URL}/reset-password/${encodeURIComponent(token)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password: newPassword }),
  });

  let data;
  try {
    data = await res.json();
  } catch {
    throw new Error("Invalid server response");
  }

  if (!res.ok) {
    throw new Error(data.error || "Failed to reset password.");
  }

  return data;
}
