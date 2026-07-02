import apiClient from "../../../api/client";

export function getProcesses() {
  return apiClient.get("/admin/processes");
}

export function getDocumentTypes(processId) {
  return apiClient.get(`/admin/document-types?process_id=${processId}`);
}

export function createDocumentType(payload) {
  return apiClient.post("/admin/document-types", payload);
}
