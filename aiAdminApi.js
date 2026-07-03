import apiClient from "../../../api/client";

export function getProcesses() {
  return apiClient.get("/admin/processes");
}

export function getDocumentTypes(processId) {
  return apiClient.get(`/admin/document-types?process_id=${processId}`);
}

export function getAIConfigurations(params = {}) {
  return apiClient.get("/admin/ai-configurations", { params });
}

export function createAIConfiguration(payload) {
  return apiClient.post("/admin/ai-configurations", payload);
}
