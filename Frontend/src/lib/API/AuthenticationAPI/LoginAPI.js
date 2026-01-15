import { safeFetch } from "./SafeFetchAPI";
import { saveAuth } from "./SaveAuthAPI";

import { API_URL } from "../../config";

export async function login(username, password) {
  const data = await safeFetch(`${API_URL}/login`, {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });

  const user = {
    id: data.user_id,
    username,
    role: data.role,
  };

  saveAuth(data.token, user);
  return data;
}
