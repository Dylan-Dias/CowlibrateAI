import { authStore } from "$lib/stores/auth";
import { browser } from "$app/environment";

const API_URL = "https://cowlibrate.onrender.com"; // your actual backend URL

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
   Protected API Calls
------------------------------------------------- */
async function fetchHealthData() {
  const res = await fetch("https://cowlibrate.onrender.com/health-distribution", {
    headers: { "Authorization": `Bearer ${token}` }
  });
  if (!res.ok) {
    console.error("Failed to fetch health data:", res.status);
    return { labels: [], series: [] };
  }
  return await res.json();
}

async function fetchBreedData() {
  const res = await fetch("https://cowlibrate.onrender.com/breed-distribution", {
    headers: { "Authorization": `Bearer ${token}` }
  });
  if (!res.ok) return { labels: [], series: [] };
  return await res.json();
}

async function fetchMilkYieldData() {
  const res = await fetch("https://cowlibrate.onrender.com/MilkYield-distribution", {
    headers: { "Authorization": `Bearer ${token}` }
  });
  if (!res.ok) return { labels: [], series: [] };
  return await res.json();
}

async function fetchWaterData() {
  const res = await fetch("https://cowlibrate.onrender.com/water-intake", {
    headers: { "Authorization": `Bearer ${token}` }
  });
  if (!res.ok) return { labels: [], series: [] };
  return await res.json();
}

export async function submitOptimization(data) {
  return authFetch("/api/optimize", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

// src/lib/services/auth.js

export async function requestPasswordReset(email) {
  const res = await fetch(
    'https://cowlibrate.onrender.com/forgot-password',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email })
    }
  );

  let data;
  try {
    data = await res.json();
  } catch {
    throw new Error('Invalid server response');
  }

  if (!res.ok) {
    throw new Error(
      data?.error || 'Failed to send reset instructions'
    );
  }

  return data;
}

// Reset password via API
export async function resetPassword(token, newPassword, confirmPassword) {
  try {
    const res = await fetch(`https://cowlibrate.onrender.com/reset-password/${encodeURIComponent(token)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password: newPassword })
  });


    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || 'Failed to reset password.');
    }

    return data; // success response
  } catch (err) {
    throw new Error(err.message || 'Network error. Please try again.');
  }
}
