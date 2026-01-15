import { authFetch } from "../AuthenticationAPI/AuthFetchAPI";

export async function fetchMilkYieldData() {
  return authFetch("/MilkYield-distribution");
}