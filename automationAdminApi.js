import apiClient from "../../../api/client";

export function getProcesses() {
  return apiClient.get("/admin/processes");
}

export function getAutomationRules(processId) {
  return apiClient.get(`/admin/processes/${processId}/automation-rules`);
}

export function createAutomationRule(payload) {
  return apiClient.post("/admin/automation-rules", payload);
}

export function getAutomationConditions(ruleId) {
  return apiClient.get(`/admin/automation-rules/${ruleId}/conditions`);
}

export function createAutomationCondition(payload) {
  return apiClient.post("/admin/automation-conditions", payload);
}

export function getAutomationActions(ruleId) {
  return apiClient.get(`/admin/automation-rules/${ruleId}/actions`);
}

export function createAutomationAction(payload) {
  return apiClient.post("/admin/automation-actions", payload);
}
