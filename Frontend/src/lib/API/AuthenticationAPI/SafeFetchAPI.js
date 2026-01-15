import { browser } from "$app/environment";

export async function safeFetch(url, options = {}) {
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
      credentials: "include", // <-- Add this line
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
