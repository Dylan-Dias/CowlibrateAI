import { authFetch } from "../AuthenticationAPI/AuthFetchAPI";

export async function fetchMilkYieldData() {
  return authFetch("/api/analytics/milk-yield");
}
