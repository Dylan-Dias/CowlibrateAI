import { authFetch } from "../AuthenticationAPI/AuthFetchAPI";

export async function fetchHealthData() {
  return authFetch("/api/analytics/health");
}
