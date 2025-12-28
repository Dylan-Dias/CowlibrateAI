import { writable } from "svelte/store";
import { browser } from "$app/environment";

function createAuthStore() {
  // If running in the browser, hydrate from localStorage
  const stored = browser ? JSON.parse(localStorage.getItem("auth") || "null") : null;

  const { subscribe, set, update } = writable(stored || {
    isAuthenticated: false,
    token: null,
    user: null
  });

  return {
    subscribe,
    setAuth: (token, user) => {
      const authData = { isAuthenticated: true, token, user };
      set(authData);

      if (browser) {
        localStorage.setItem("auth", JSON.stringify(authData));
      }
    },
    clearAuth: () => {
      const empty = { isAuthenticated: false, token: null, user: null };
      set(empty);

      if (browser) {
        localStorage.removeItem("auth");
      }
    }
  };
}

export const authStore = createAuthStore();
