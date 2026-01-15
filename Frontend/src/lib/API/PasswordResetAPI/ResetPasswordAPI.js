import { API_URL } from "../config";

export async function resetPassword(token, newPassword) {
  const res = await fetch(`${API_URL}/reset-password/${encodeURIComponent(token)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password: newPassword }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error || "Failed to reset password.");
  }

  return data;
}
