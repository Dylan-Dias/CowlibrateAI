import { API_URL } from "$lib/config.js";

function authHeaders() {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Not authenticated");

  return {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json"
  };
}

/* ---------- HEALTH ---------- */
export async function getHealthChartData() {
  const res = await fetch(`${API_URL}/health-distribution`, {
    headers: authHeaders()
  });

  const { labels = [], series = [] } = await res.json();

  return labels.map((label, i) => ({
    group: label,
    value: series[i] ?? 0
  }));
}

/* ---------- BREED ---------- */
export async function getBreedChartData() {
  const res = await fetch(`${API_URL}/breed-distribution`, {
    headers: authHeaders()
  });

  const { labels = [], series = [] } = await res.json();

  return labels.map((label, i) => ({
    group: label,
    value: series[i] ?? 0
  }));
}

/* ---------- MILK YIELD ---------- */
export async function getMilkYieldChartData() {
  const res = await fetch(`${API_URL}/MilkYield-distribution`, {
    headers: authHeaders()
  });

  const { labels = [], series = [] } = await res.json();

  return labels.map((label, i) => ({
    group: "Milk Yield",
    key: label,
    value: series[i] ?? 0
  }));
}

/* ---------- WATER INTAKE ---------- */
export async function getWaterIntakeChartData() {
  const res = await fetch(`${API_URL}/water-intake`, {
    headers: authHeaders()
  });

  const { labels = [], series = [] } = await res.json();

  return labels.map((label, i) => ({
    group: "Water Intake",
    key: label,
    value: series[i] ?? 0
  }));
}
