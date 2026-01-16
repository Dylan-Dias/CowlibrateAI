import { authFetch } from "../AuthenticationAPI/AuthFetchAPI";

export async function fetchBreedData() {
  return authFetch("/api/analytics/breed");
}
