import { authStore } from "$lib/stores/auth";
import { browser } from "$app/environment";

export function saveAuth(token, user) {
  if (browser) {
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));
  }
  authStore.setAuth(token, user);
}
