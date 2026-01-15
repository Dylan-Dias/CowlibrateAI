import { safeFetch } from "../AuthenticationAPI/SafeFetchAPI";
import { saveAuth } from "../AuthenticationAPI/SaveAuthAPI";

const API_URL = "https://cowlibrate.onrender.com";

export async function register(username, email, password, role = "user") {
  const data = await safeFetch(`${API_URL}/register`, {
    method: "POST",
    body: JSON.stringify({ username, email, password, role }),
  });

  saveAuth(data.token, data.user);
  return data;
}
