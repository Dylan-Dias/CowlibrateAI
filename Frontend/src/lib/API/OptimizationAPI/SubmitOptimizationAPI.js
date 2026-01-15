import { authFetch } from "../AuthenticationAPI/AuthFetchAPI";

export async function submitOptimization(data) {
  return authFetch("/api/optimize", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
