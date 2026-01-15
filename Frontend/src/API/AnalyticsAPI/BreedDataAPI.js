import { authFetch } from "../AuthenticationAPI/AuthFetchAPI";

export async function fetchBreedData() {
  return authFetch("/breed-distribution");
}