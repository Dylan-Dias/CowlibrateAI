

const API_URL = "https://cowlibrate.onrender.com";

function authHeaders() {
  const token = localStorage.getItem("token");
  return {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "",
  };
}

export async function getHealthChartData() {
  const res = await fetch(`${API_URL}/health-distribution`, {
    method: "GET",
    headers: authHeaders(),
    credentials: "include"
  });
  return await res.json();
}

export async function getBreedChartData() {
  const res = await fetch(`${API_URL}/breed-distribution`, {
    method: "GET",
    headers: authHeaders(),
    credentials: "include"
  });
  return await res.json();
}

export async function getMilkYieldChartData() {
  const res = await fetch(`${API_URL}/MilkYield-distribution`, {
    method: "GET",
    headers: authHeaders(),
    credentials: "include"
  });
  return await res.json();
}

export async function getWaterIntakeChartData() {
  const res = await fetch(`${API_URL}/water-intake`, {
    method: "GET",
    headers: authHeaders(),
    credentials: "include"
  });
  return await res.json();
}
