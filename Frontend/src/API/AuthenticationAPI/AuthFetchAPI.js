import { safeFetch } from "./SafeFetchAPI";

import { API_URL } from "../config";

export async function authFetch(endpoint, options = {}) {
  if (!endpoint.startsWith("/")) endpoint = `/${endpoint}`;
  const fullUrl = `${API_URL}${endpoint}`;
  return safeFetch(fullUrl, options);
}
