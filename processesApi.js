import apiClient from "../../../api/client";

export function getProcesses() {
  return apiClient.get("/admin/processes");
}

export function createProcess(payload) {
  return apiClient.post("/admin/processes", payload);
}

export function updateProcess(processId, payload) {
  return apiClient.put(`/admin/processes/${processId}`, payload);
}

export function seedRegulatoryRequests() {
  return apiClient.post("/seed/regulatory-requests");
}
