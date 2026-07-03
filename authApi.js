import apiClient from "../../api/client";

export function login(credentials) {
  return apiClient.post("/auth/login", credentials);
}

export function me() {
  return apiClient.get("/auth/me");
}

export function getUsers() {
  return apiClient.get("/auth/users");
}

export function createUser(payload) {
  return apiClient.post("/auth/users", payload);
}
