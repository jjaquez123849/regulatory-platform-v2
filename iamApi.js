import apiClient from "../../../api/client";

export function getUsers() {
  return apiClient.get("/auth/users");
}

export function createUser(payload) {
  return apiClient.post("/auth/users", payload);
}

export function getRoles() {
  return apiClient.get("/iam/roles");
}

export function createRole(payload) {
  return apiClient.post("/iam/roles", payload);
}

export function getPermissions() {
  return apiClient.get("/iam/permissions");
}

export function createPermission(payload) {
  return apiClient.post("/iam/permissions", payload);
}

export function getCapabilities() {
  return apiClient.get("/iam/capabilities");
}

export function createCapability(payload) {
  return apiClient.post("/iam/capabilities", payload);
}

export function getAreas() {
  return apiClient.get("/iam/areas");
}

export function createArea(payload) {
  return apiClient.post("/iam/areas", payload);
}

export function getTeams() {
  return apiClient.get("/iam/teams");
}

export function createTeam(payload) {
  return apiClient.post("/iam/teams", payload);
}

export function assignRoleToUser(payload) {
  return apiClient.post("/iam/users/roles", payload);
}

export function assignTeamToUser(payload) {
  return apiClient.post("/iam/users/teams", payload);
}

export function assignPermissionToRole(payload) {
  return apiClient.post("/iam/roles/permissions", payload);
}

export function assignCapabilityToRole(payload) {
  return apiClient.post("/iam/roles/capabilities", payload);
}

export function getMyEffectiveAccess() {
  return apiClient.get("/iam/me/effective-access");
}
