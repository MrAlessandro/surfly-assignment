import { defineStore } from "pinia";

// generate random

export const useUserStore = defineStore("user", {
  state: () => ({
    username: localStorage.getItem("username") || "guest", // Initialize from localStorage if available
  }),
  actions: {
    setUsername(newUsername) {
      this.username = newUsername;
      localStorage.setItem("username", newUsername); // Persist to localStorage
    },
  },
});
