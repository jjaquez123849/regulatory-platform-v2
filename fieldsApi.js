import apiClient from "../../../api/client";

export function getProcesses() {
  return apiClient.get("/admin/processes");
}

export function getProcessFields(processId) {
  return apiClient.get(`/admin/processes/${processId}/fields`);
}

export function createProcessField(payload) {
  return apiClient.post("/admin/fields", payload);
}

export function createFieldOption(payload) {
  return apiClient.post("/admin/field-options", payload);
}

export function getFieldOptions(fieldId) {
  return apiClient.get(`/admin/fields/${fieldId}/options`);
}
