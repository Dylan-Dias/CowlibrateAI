import { API_URL } from "../config";

export async function requestPasswordReset(email) {
  const res = await fetch(`${API_URL}/forgot-password`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data?.error || "Failed to send reset instructions");
  return data;
}
