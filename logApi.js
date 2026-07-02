import apiClient from "../../api/client";

export function getProcesses() {
  return apiClient.get("/admin/processes");
}

export function getProcessLog(processId) {
  return apiClient.get(`/log/process/${processId}`);
}
