import apiClient from "../../../api/client";

export function getProcesses() {
  return apiClient.get("/admin/processes");
}

export function getWorkflowStates(processId) {
  return apiClient.get(`/admin/processes/${processId}/workflow-states`);
}

export function createWorkflowState(payload) {
  return apiClient.post("/admin/workflow-states", payload);
}

export function getWorkflowTransitions(processId) {
  return apiClient.get(`/admin/processes/${processId}/workflow-transitions`);
}

export function createWorkflowTransition(payload) {
  return apiClient.post("/admin/workflow-transitions", payload);
}
