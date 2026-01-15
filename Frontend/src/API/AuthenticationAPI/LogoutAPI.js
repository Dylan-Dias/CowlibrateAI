import { authStore } from "$lib/stores/auth";
import { browser } from "$app/environment";

export function logout() {
  if (browser) {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }
  authStore.clearAuth();
}
