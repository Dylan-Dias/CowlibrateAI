import { authFetch } from "../AuthenticationAPI/AuthFetchAPI";

export async function fetchWaterData() {
  return authFetch("/api/analytics/water-intake");
}
