import apiClient from "../../api/client";

export function getDashboardSummary() {
  return apiClient.get("/dashboard/summary");
}

export function getDashboardCritical() {
  return apiClient.get("/dashboard/critical");
}
