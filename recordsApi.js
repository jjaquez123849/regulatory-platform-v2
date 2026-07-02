import apiClient from "../../api/client";

export function getProcesses() {
  return apiClient.get("/admin/processes");
}

export function getProcessFields(processId) {
  return apiClient.get(`/admin/processes/${processId}/fields`);
}

export function createRecord(payload) {
  return apiClient.post("/records/", payload);
}

export function getRecords(processId) {
  const query = processId ? `?process_id=${processId}` : "";
  return apiClient.get(`/records/${query}`);
}
